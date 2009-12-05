#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

import utils

import grammar
import semantics
import semantics.concept
import word_factory

from tree import Tree

def adjAdn(person=None, gender=None, number=None, S=None, posicao=None):
    if person is None:
        person = utils.aleatory('p')
    if gender is None:
        gender = utils.aleatory('g')
    if number is None:
        number = utils.aleatory('n')
    next = None
    if posicao == 'pre':
        if utils.percent(35):
            det = word_factory.getNominal('article', gender, number)
        elif utils.percent(50):
            det = word_factory.getAdjectivePronoun(gender, number, 'determinante')
        else:
            det = word_factory.getPossessivePronoun(
                gender, number, utils.aleatory('p'), utils.aleatory('n'))
        L = [Tree(det)]
        next = det
    elif posicao == 'pos':
        if utils.percent(50):
            L = [Tree(word_factory.getRelativePronoun(gender, number)),
                 sintagmaVerbal(person, gender, number, S=S)]
        elif utils.percent(50):
            L = [Tree(word_factory.getRelativePronoun(gender, number)),
                 oracaoSimples(tran='vtd', OD=S)]
        else:
            oracaoExpl = oracaoSimples(tran='vti', OI=S)
            prep = word_factory.getPreposition(oracaoExpl.info['prep'],
                                 gender, number, None)
            L = [Tree(prep),
                 Tree(word_factory.getRelativePronoun(gender, number)),
                 oracaoExpl]
    else:
        L = [Tree(word_factory.getNominal('adjective', gender, number, S))]
    return Tree('adjunto adnominal', L, {'next': next})

def sintagmaNominal(person=None, gender=None, number=None, funcao='S',
                    modo=None, prep=None, S=None):
    if person is None:
        if S is not None and \
                semantics.verifySemantics(S, 'PESSOA'):
            person = utils.aleatory('p')
        else: person = '3'
    if gender is None:
        gender = utils.aleatory('g')
    if number is None:
        number = utils.aleatory('n')
    if modo is None:
        if person != '3' or utils.percent(15):
            modo = 'personal_pronoun'
        else:
            modo = 'noun'
    if modo == 'noun':
        if person != '3':
            raise 'Sintagma nominal em modo substantivo ' \
                'deve estar na terceira pessoa'
        nucleo = word_factory.getNominal('noun', gender, number, S)
        L = [Tree(nucleo)]
        if number == 's' or utils.percent(15):
            adjAdnPre = adjAdn(person, gender, number, S, 'pre')
            next = (adjAdnPre.info['next'].value.index,
                    adjAdnPre.info['next'].category)
            L = [adjAdnPre] + L
        else:
            next = None
        if utils.percent(40):
            L = L + [adjAdn(person, gender, number, S)]
        if utils.percent(20):
            L = L + [adjAdn(person, gender, number, S, 'pos')]
    elif modo == 'personal_pronoun':
        if funcao == 'OD':
            nucleo = word_factory.getPersonalPronoun(
                person, number, gender, funcao, 'a')
        else:
            nucleo = word_factory.getPersonalPronoun(
                person, number, gender, funcao, 't')
        L = [Tree(nucleo)]
        next = (nucleo.value.index, nucleo.category)
    else:
        raise 'Modo invalido', modo
    if prep is not None:
        preposicao = word_factory.getPreposition(prep, gender, number, next)
        if preposicao.value.contracts(next):
            L = [Tree(preposicao)] + L[1:]
        else:
            L = [Tree(preposicao)] + L
    return Tree('sintagma nominal', L, {'nucleo': nucleo})

def sintagmaVerbal(person=None, gender=None, number=None, tense=None,
                   tran=None, S=None, OD=None, OI=None):
    if person is None:
        person = utils.aleatory('p')
    if gender is None:
        gender = utils.aleatory('g')
    if number is None:
        number = utils.aleatory('n')
    if tense is None:
        tense = utils.aleatory('t')

    # Núcleo do sintagma verbal é sempre um verbo
    nucleo = word_factory.getVerb(person, number, tense, tran, S=S, OD=OD, OI=OI)

    # tran (transitividade) depende do verbo escolhido
    if tran is None: tran = nucleo.info['entity'].transitivity

    # L será o vetor 'filhos' da raiz do sintagma nominal
    L = [Tree(nucleo)]

    if tran == 'vpi':
        L = [word_factory.getPersonalPronoun(person, number, gender, 'R', 'a')] + L
    if tran in ('vti', 'vtdi') and OI is None:
        xOI = sintagmaNominal(funcao='OI',
                              S=nucleo.info['entity'].concept['OI'],
                              prep=nucleo.info['entity'].prep)
        L = L + [xOI]
    if tran in ('vtd', 'vtdi') and OD is None:
        xOD = sintagmaNominal(funcao='OD',
                              S=nucleo.info['entity'].concept['OD'])
        if xOD.info['nucleo'].category == 'personal_pronoun':
            L = [xOD] + L
        else:
            L = L + [xOD]
    return Tree('sintagma verbal', L, {'nucleo':nucleo})

def oracaoSimples(person=None, gender=None, number=None, tense=None,
                  tran=None, S=None, OD=None, OI=None):
    if person is None:
        person = utils.aleatory('p')
    if gender is None:
        gender = utils.aleatory('g')
    if number is None:
        number = utils.aleatory('n')
    if tense is None:
        tense = utils.aleatory('t')

    sv = sintagmaVerbal(person, gender, number, tense, tran, S, OD, OI)
    obj_nucleo = sv.info['nucleo'].info['entity']
    sn = sintagmaNominal(person, gender, number, 'S',
                         S=obj_nucleo.concept['base'])

    if OI is None:
        prep = None
    else:
        prep = obj_nucleo.prep

    return Tree('oracao', [sn, sv], {'prep': prep})

def oracaoSemSujeito(tense=None, OD=None, OI=None):
    if tense is None:
        tense = utils.aleatory('t')

    if utils.percent(100):
        # 3a. pessoa do plural: fizeram, tentarão, etc.
        sv = sintagmaVerbal('3', 'm', 'p', tense, None,
                            'PESSOA', OD, OI)
        L = [sv]

    if OI is not None:
        prep = sv.info['nucleo'].info['entity'].prep
    else:
        prep = None

    return Tree('oracao', L, {'prep': prep})

def oracao(person=None, gender=None, number=None, tense=None):
    if utils.percent(20):
        return oracaoSemSujeito()
    return oracaoSimples(person, gender, number, tense)

if __name__ == '__main__':
    for i in range(20):
        print oracao()
