# -*- coding: utf-8 -*-

import random

import grammar

def percent(n):
    return (random.randrange(100)<n)

def aleatory(s):
    if s == 'p':
        return random.choice('12333333')
    if s == 'g':
        return random.choice(grammar.GENDERS)
    if s == 'n':
        return random.choice(grammar.NUMBERS)
    if s == 't':
        return random.choice(grammar.TENSES)
    raise "aleatory('" + s + "') invalid"
