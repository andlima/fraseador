#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

import utils

from grammar import CONCEPTUAL_LIST
from grammar.word import Word

from vocabulary import Vocabulary

from semantics import init_knowledge, init_category
from semantics import table as semantics_table
from semantics.concept import Concept


vocabulary = Vocabulary('./data/vocabulary')
knowledge = Concept('./data/knowledge')


init_knowledge('./data/knowledge')

for category in CONCEPTUAL_LIST:
    init_category(category, './data/knowledge')


def _word(category, index):
    return vocabulary.data[category][index]


class SemanticCompatibilityError(Exception):
    pass

def getVerb(person, number, tense, tran=None, S=None, OD=None, OI=None):
    category = 'verb'
    lista = semantics_table[category]
    if S is not None:
        lista = [x for x in lista if x.includes(S)]
    if tran in ('vtd', 'vtdi') and OD is not None:
        lista = [x for x in lista if x.includes(OD, 'OD')]
    if tran in ('vti', 'vtdi') and OI is not None:
        lista = [x for x in lista if x.includes(OI, 'OI')]
    if tran is not None:
        lista = [x for x in lista if x.transitivity == tran]
    if not lista:
        raise SemanticCompatibilityError('No word found for %s' % str(
                (category, person, number, tense, tran, S, OD, OI)
              ))
    word = random.choice(lista)
    return Word(_word(category, word.index), category,
                {'person': person, 'number': number,
                 'tense': tense, 'entity': word})


def getNominal(category, gender, number, S=None):
    if S is None:
        S = '*'
    lista = [x for x in semantics_table[category]
             if _word(category, x.index).validate(gender, number)]

    if category in ('adjective'):
        lista = [x for x in lista if x.includes(S)]
    else:
        lista = [x for x in lista if x.belongs(S)]
    if not lista:
        raise SemanticCompatibilityError('No word found for %s' % str(
                (category, gender, number, S)
              ))
    word = random.choice(lista)
    return Word(_word(category, word.index), category,
                     {'gender': gender, 'number': number, 'entity': word})


def getPreposition(preposition, gender, number, next=None):
    category = 'preposition'
    if preposition is None:
        preposition = random.choice(vocabulary.data[category].keys())
    return Word(_word(category, preposition), category,
                {'gender': gender, 'number': number, 'next': next})


def getPersonalPronoun(person, number, gender, function='S', ton='t'):
    category = 'personal_pronoun'
    lista = [x for x in vocabulary.data[category].values()
             if x.validate(person, number, gender, function, ton)]
    return Word(random.choice(lista), category,
                {'gender': gender, 'number': number,
                 'function': function, 'ton': ton})


def getPossessivePronoun(gender, number, idp, idn):
    category = 'possessive_pronoun'
    lista = [x for x in vocabulary.data[category].values()
             if x.validate(gender, number, idp, idn)]
    if not lista:
        raise SemanticCompatibilityError('No word found for %s' % str(
                (category, gender, number)
              ))
    word = random.choice(lista)
    return Word(_word(category, word.index), category,
                {'gender': gender, 'number': number})


def getRelativePronoun(gender, number, S=None):
    category = 'relative_pronoun'
    lista = [x for x in semantics_table[category]
             if _word(category, x.index).validate(gender, number)]
    if S is None:
        lista = [x for x in lista if not x.belongs('PESSOA')]
    else:
        lista = [x for x in lista if x.belongs('PESSOA')]
    if not lista:
        raise SemanticCompatibilityError('No word found for %s' % str(
                (category, gender, number, S)
              ))
    word = random.choice(lista)
    return Word(_word(category, word.index), category,
                {'gender': gender, 'number': number, 'entity': word})


def getAdjectivePronoun(gender, number, use):
    category = 'adjective_pronoun'
    lista = [x for x in semantics_table[category]
             if (_word(category, x.index).validate(gender, number) and
                 x.validateUse(use, gender, number))]
    if not lista:
        raise SemanticCompatibilityError('No word found for %s' % str(
                (gender, number, use)
              ))
    word = random.choice(lista)
    return Word(_word(category, word.index), category,
                {'gender': gender, 'number': number, 'entity': word})
