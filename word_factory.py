#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

import utils

import grammar
from grammar.word import Word

from vocabulary import Vocabulary

import semantics
from semantics.concept import Concept

vocabulary = Vocabulary('./data/vocabulary')
knowledge = Concept('./data/knowledge')

semantics.initKnowledge('./data/knowledge')

for category in grammar.CONCEPTUAL_LIST:
    semantics.initCategory(category, './data/knowledge')

def _word(category, index):
    return vocabulary.data[category][index]

def getVerb(person, number, tense, tran=None,
             S=None, OD=None, OI=None):
    category = 'verb'
    lista = semantics.table[category]
    if S is not None:
        lista = filter(lambda x: x.includes(S), lista)
    if tran in ('vtd', 'vtdi') and OD is not None:
        lista = filter(lambda x: x.includes(OD, 'OD'), lista)
    if tran in ('vti', 'vtdi') and OI is not None:
        lista = filter(lambda x: x.includes(OI, 'OI'), lista)
    if tran is not None:
        lista = filter(lambda x: x.transitivity == tran, lista)
    if not lista:
        raise 'Error: no semantic compatibility:', (
            category, person, number, tense, tran, S, OD, OI)
    word = random.choice(lista)
    return Word(_word(category, word.index), category,
                     {'person': person, 'number': number,
                      'tense': tense, 'entity': word})

def getNominal(category, gender, number, S=None):
    if S is None:
        S = '*'
    lista = filter(
        lambda x: _word(category, x.index).validate(gender, number),
        semantics.table[category])
    if category in ('adjective'):
        lista = filter(lambda x: x.includes(S), lista)
    else:
        lista = filter(lambda x: x.belongs(S), lista)
    if not lista:
        raise 'Error: no semantic compatibility:', (
            category, gender, number, S)
    word = random.choice(lista)
    return Word(_word(category, word.index), category,
                     {'gender': gender, 'number': number,
                      'entity': word})

def getPreposition(prep, gender, number, next=None):
    category = 'preposition'
    if prep is None:
        prep = random.choice(vocabulary.data[category].keys())
    return Word(_word(category, prep), category,
                     {'gender': gender, 'number': number,
                      'next': next})

def getPersonalPronoun(person, number, gender,
                       function='S', ton='t'):
    category = 'personal_pronoun'
    lista = filter(
        lambda x: x.validate(person, number, gender,
                             function, ton),
        vocabulary.data[category].values())
    return Word(random.choice(lista), category,
                {'gender': gender, 'number': number,
                 'function': function, 'ton': ton})

def getPossessivePronoun(gender, number, idp, idn):
    category = 'possessive_pronoun'
    lista = filter(lambda x: x.validate(gender, number, idp, idn),
                   vocabulary.data[category].values())
    if not lista:
        raise 'Error:', (category, gender, number)
    word = random.choice(lista)
    return Word(_word(category, word.index), category,
                {'gender': gender, 'number': number})

def getRelativePronoun(gender, number, S=None):
    category = 'relative_pronoun'
    lista = filter(
        lambda x: _word(category, x.index).validate(gender, number),
        semantics.table[category])
    if S is None:
        lista = filter(lambda x: not x.belongs('PESSOA'), lista)
    else:
        lista = filter(lambda x: x.belongs('PESSOA'), lista)
    if not lista:
        raise 'Error: no semantic compatibility:', (
            category, gender, number, S)
    word = random.choice(lista)
    return Word(_word(category, word.index), category,
                     {'gender': gender, 'number': number,
                      'entity': word})

def getAdjectivePronoun(gender, number, use):
    category = 'adjective_pronoun'
    lista = filter(
        lambda x: _word(category, x.index).validate(gender, number) and \
            x.validateUse(use, gender, number),
        semantics.table[category])
    if not lista:
        raise 'Error: no semantic compatibility:', (
            gender, number, use)
    word = random.choice(lista)
    return Word(_word(category, word.index), category,
                {'gender': gender, 'number': number,
                 'entity': word})
