#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

from utils import dump_args, percent, aleatory, randomize
from utils import use_debug as utils_use_debug
#utils_use_debug(True)

import grammar
import semantics
import semantics.concept
import word_factory

from tree import Tree


@dump_args
def determiner(person=None, gender=None, number=None, function='S',
               kind=None, S=None):
    if percent(35):
        det = word_factory.getNominal('article', gender, number)
        next = (det.value.index, 'article')
    elif percent(50):
        det = word_factory.getAdjectivePronoun(
            gender, number, 'determiner')
        next = (det.value.index, 'adjective_pronoun')
    else:
        det = word_factory.getPossessivePronoun(
            gender, number, aleatory('person'), aleatory('number'))
        next = (det.value.index, 'possessive_pronoun')
    return Tree('determiner', [det], {'next': next})


@dump_args
def adnominalAdjunct(person=None, gender=None, number=None,
                     function='S', kind=None, S=None,
                     position='pos'):
    L = []

    if kind == 'noun':
        if percent(20):
            if percent(50):
                # menino feio
                # bola feia
                adjective = word_factory.getNominal(
                    'adjective', gender, number, S)
                L.append(adjective)
            else:
                if percent(40):
                    # menino que correu
                    # bola que caiu
                    L = [word_factory.getRelativePronoun(
                            gender, number, None),
                         verbPhrase(person, gender, number, S=S)]
                elif percent(50):
                    # menino que a mãe ama
                    # bola que o menino chutou
                    L = [word_factory.getRelativePronoun(
                            gender, number, None),
                         clause(tran='vtd', OD=S)]
                else:
                    # menino de quem a mãe gosta
                    # bola da qual o menino gosta
                    that_clause = clause(tran='vti', OI=S)
                    prep = word_factory.getPreposition(
                        that_clause.info['prep'], gender,
                        number, None)
                    L = [prep,
                         word_factory.getRelativePronoun(
                            gender,number, S),
                         that_clause]
                
    elif kind == 'personal_pronoun' and function == 'S':
        if percent(20):
            # eu que corri
            L = [word_factory.getRelativePronoun(gender, number, None),
                 verbPhrase(person, gender, number, S=S)]
        
    if L:
        return Tree('adnominal adjunct', L, {})
    else:
        return None


@dump_args
@randomize('gender', 'number')
def noun(person=None, gender=None, number=None, function='S',
         kind=None, S=None):

    if kind == 'noun':
        if person != '3':
            raise 'Noun phrase for NOUN kind must be on the 3rd person'
        head = word_factory.getNominal('noun', gender, number, S)
        next = (head.value.index, 'noun')
    elif kind == 'personal_pronoun':
        tonic = 'a' if function == 'OD' else 't'
        head = word_factory.getPersonalPronoun(
            person, number, gender, function, tonic)
        next = (head.value.index, 'personal_pronoun')
    else:
        raise 'Invalid kind for noun phrase', kind
    return Tree('noun', [head], {'head': head, 'next': next})


@dump_args
@randomize('gender', 'number')
def nounBar(person=None, gender=None, number=None, function='S',
            kind=None, S=None):
    n = noun(person, gender, number, function, kind, S)
    a = None
    if percent(50):
        a = adnominalAdjunct(person, gender, number, function, kind, S)
    if a:
        L = [n, a]
    else:
        L = [n]
    return Tree('noun-bar', L, {'head': n.info['head'], 'next': n.info['next']})


@dump_args
@randomize('gender', 'number')
def nounPhrase(person=None, gender=None, number=None, function='S',
               kind=None, S=None):

    if person is None:
        if S and semantics.verifySemantics(S, 'PESSOA'):
            person = aleatory('person')
        else: person = '3'
    if kind is None:
        if person != '3' or percent(15):
            kind = 'personal_pronoun'
        else:
            kind = 'noun'

    L = []
    next = None
    if kind == 'noun':
        det = determiner(person, gender, number, function, kind, S)
        L.append(det)
        next = det.info['next']
    n = nounBar(person, gender, number, function, kind, S)

    if not next:
        next = n.info['next']

    L.append(n)
    return Tree('noun phrase', L, {'head': n.info['head'], 'next': next})


@dump_args
@randomize('gender', 'number')
def prepositionalPhrase(prep=None, person=None, gender=None,
                        number=None, function='S', kind=None, S=None):

    if person is None:
        if S and semantics.verifySemantics(S, 'PESSOA'):
            person = aleatory('person')
        else:
            person = '3'
    if kind is None:
        if person != '3' or percent(15):
            kind = 'personal_pronoun'
        else:
            kind = 'noun'

    np = nounPhrase(person, gender, number, function, kind, S)
    next = np.info['next']
    L = [np]

    p = word_factory.getPreposition(prep, gender, number, next)

    L = [Tree("preposition", [p])] + L

    return Tree('prepositional phrase', L, {'head': np.info['head']})


@dump_args
@randomize('person', 'gender', 'number', 'tense')
def verb(person=None, gender=None, number=None, tense=None,
         tran=None, S=None, OD=None, OI=None):

    head = word_factory.getVerb(person, number, tense, tran, S=S, OD=OD, OI=OI)
    L = [head]

    if tran is None:
        tran = head.info['entity'].transitivity

    if tran == 'vpi':
        L = [word_factory.getPersonalPronoun(person, number, gender, 'R', 'a')] + L
    if tran in ('vti', 'vtdi') and OI is None:
        xOI = prepositionalPhrase(function='OI',
                                  S=head.info['entity'].concept['OI'],
                                  prep=head.info['entity'].prep)
        L = L + [xOI]
    if tran in ('vtd', 'vtdi') and OD is None:
        xOD = nounPhrase(function='OD',
                         S=head.info['entity'].concept['OD'])
        if xOD.info['head'].category == 'personal_pronoun':
            L = [xOD] + L
        else:
            L = L + [xOD]

    return Tree('verb', L, {'head': head})


@dump_args
@randomize('person', 'gender', 'number', 'tense')
def verbBar(person=None, gender=None, number=None, tense=None,
            tran=None, S=None, OD=None, OI=None):
    v = verb(person, gender, number, tense, tran, S, OD, OI)
    return Tree('verb-bar', [v], {'head': v.info['head']})


@dump_args
@randomize('person', 'gender', 'number', 'tense')
def verbPhrase(person=None, gender=None, number=None, tense=None,
                   tran=None, S=None, OD=None, OI=None):
    vb = verbBar(person, gender, number, tense, tran, S, OD, OI)
    L = [vb]

    return Tree('verb phrase', L, {'head': vb.info['head']})


@dump_args
@randomize('person', 'gender', 'number', 'tense')
def clause(person=None, gender=None, number=None, tense=None,
           tran=None, S=None, OD=None, OI=None):

    vp = verbPhrase(person, gender, number, tense, tran, S, OD, OI)
    obj_head = vp.info['head'].info['entity']
    np = nounPhrase(person, gender, number, 'S',
                    S=obj_head.concept['base'])

    prep = None

    if OI:
        prep = obj_head.prep

    return Tree('clause', [np, vp], {'prep': prep})


if __name__ == '__main__':
    n = 20
    lf = '\n'
    phrase_list = []
    for i in range(n):
        phrase_list.append(clause().__repr__().capitalize() + '.')
    print lf.join(phrase_list)
