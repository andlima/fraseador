#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import dump_args, percent, aleatory, randomize
#from utils import use_debug as utils_use_debug
#utils_use_debug(True)

from semantics import verify_semantics
import word_factory as wf

from tree import Tree
#Tree.debug = True


class NounNotThirdPersonError(Exception):
    '''
    The noun() phrase method cannot handle something like a noun not
    in the third person.  Otherwise, it would return errors like "o
    menino [third person] beijei [first person] a menina", with the
    verb and the subject disagreeing.

    If you ask explicitly for a noun, it must be on the third person.
    '''
    pass


class NounPhraseKindError(Exception):
    '''Invalid kind for noun phrase.'''
    pass


@dump_args
def determiner(person=None, gender=None, number=None, function='S',
               kind=None, S=None):
    if percent(35):
        det = wf.getNominal('article', gender, number)
        next = (det.value.index, 'article')
    elif percent(50):
        det = wf.getAdjectivePronoun(gender, number, 'determiner')
        next = (det.value.index, 'adjective_pronoun')
    else:
        det = wf.getPossessivePronoun(
            gender, number, aleatory('person'), aleatory('number'))
        next = (det.value.index, 'possessive_pronoun')
    return Tree('determiner', [det], {'next': next})


@dump_args
def adnominalAdjunct(person=None, gender=None, number=None, function='S',
                     kind=None, S=None, position='pos'):
    L = []

    if kind == 'noun':
        if percent(20):
            if percent(50):
                # menino feio
                # bola feia
                adjective = wf.getNominal('adjective', gender, number, S)
                L.append(adjective)
            else:
                if percent(40):
                    # menino que correu
                    # bola que caiu
                    L = [wf.getRelativePronoun(gender, number, None),
                         verbPhrase(person, gender, number, S=S)]
                elif percent(50):
                    # menino que a mãe ama
                    # bola que o menino chutou
                    L = [wf.getRelativePronoun(gender, number, None),
                         clause(tran='vtd', OD=S)]
                else:
                    # menino de quem a mãe gosta
                    # bola da qual o menino gosta
                    that_clause = clause(tran='vti', OI=S)
                    preposition = wf.getPreposition(
                        that_clause.info['preposition'], gender,
                        number, None)
                    L = [
                        preposition,
                        wf.getRelativePronoun(
                            gender, number, S
                        ),
                        that_clause
                    ]

    elif kind == 'personal_pronoun' and function == 'S':
        if percent(20):
            # eu que corri
            L = [wf.getRelativePronoun(gender, number, None),
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
            raise NounNotThirdPersonError(
                'Phrase for noun not on the 3rd person: %s' % str(
                    (person, gender, number, function, kind, S)
                )
            )
        head = wf.getNominal('noun', gender, number, S)
        next = (head.value.index, 'noun')
    elif kind == 'personal_pronoun':
        tonic = 'a' if function == 'OD' else 't'
        head = wf.getPersonalPronoun(
            person, number, gender, function, tonic)
        next = (head.value.index, 'personal_pronoun')
    else:
        raise NounPhraseKindError(
            "Invalid argument `kind`=%s for noun(). Should be one of: "
            "['noun', 'personal_pronoun']. " % repr(kind)
        )
    return Tree('noun', [head], {'head': head, 'next': next})


@dump_args
@randomize('gender', 'number')
def nounBar(person=None, gender=None, number=None, function='S',
            kind=None, S=None):
    noun_ = noun(person, gender, number, function, kind, S)
    adn_adj = None
    if percent(50):
        adn_adj = adnominalAdjunct(person, gender, number, function, kind, S)
    if adn_adj:
        L = [noun_, adn_adj]
    else:
        L = [noun_, ]
    return Tree('noun-bar', L, {'head': noun_.info['head'],
                                'next': noun_.info['next']})


@dump_args
@randomize('gender', 'number')
def nounPhrase(person=None, gender=None, number=None, function='S',
               kind=None, S=None):

    if person is None:
        if S and verify_semantics(S, 'PESSOA'):
            person = aleatory('person')
        else:
            person = '3'
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
def prepositionalPhrase(preposition=None, person=None, gender=None,
                        number=None, function='S', kind=None, S=None):

    if person is None:
        if S and verify_semantics(S, 'PESSOA'):
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

    p = wf.getPreposition(preposition, gender, number, next)

    L = [Tree("preposition", [p])] + L

    return Tree('prepositional phrase', L, {'head': np.info['head']})


@dump_args
@randomize('person', 'gender', 'number', 'tense')
def verb(person=None, gender=None, number=None, tense=None,
         tran=None, S=None, OD=None, OI=None):

    head = wf.getVerb(person, number, tense, tran, S=S, OD=OD, OI=OI)
    L = [head]

    if tran is None:
        tran = head.info['entity'].transitivity

    if tran == 'vpi':
        L = [wf.getPersonalPronoun(person, number, gender, 'R', 'a')] + L
    if tran in ('vti', 'vtdi') and OI is None:
        xOI = prepositionalPhrase(function='OI',
                                  S=head.info['entity'].concept['OI'],
                                  preposition=head.info['entity'].preposition)
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
    np = nounPhrase(person, gender, number, 'S', S=obj_head.concept['base'])
    preposition = obj_head.preposition if OI else None

    return Tree('clause', [np, vp], {'preposition': preposition})
