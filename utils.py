# -*- coding: utf-8 -*-

import random

import grammar

debug = False

def percent(n):
    '''Returns true for n percent of the calls.'''
    return (random.randrange(100) < n)

def aleatory(s):
    '''Return a random person/gender/number/tense element.'''

    if s == 'person':
        return random.choice('12333333')
    if s == 'gender':
        return random.choice(grammar.GENDERS)
    if s == 'number':
        return random.choice(grammar.NUMBERS)
    if s == 'tense':
        return random.choice(grammar.TENSES)
    raise "aleatory('" + s + "') invalid"


_depth = 0
def dump_args(func):
    '''A decorator for dumping a function's arguments.'''

    if not debug:
        return func

    argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
    fname = func.func_name
    def echo_func(*args, **kwargs):
        global _depth
        _depth += 1
        d = _depth * '  '
        print '\t$$', d, fname + ":", ', '.join(
            '%s=%r' % entry
            for entry in zip(argnames,args) + kwargs.items())
        x = func(*args, **kwargs)
        print '\t## ', d + '->', x
        _depth -= 1
        return x
    return echo_func

def randomize(*arg_list):
    '''A decorator for randomizing arguments provided as None.'''

    def randomize(func):
        argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
        def other_func(*args, **kwargs):
            tmp = {}
            for k, v in zip(argnames, args) + kwargs.items():
                tmp[k] = v
            for k in arg_list:
                if k not in tmp.keys():
                    tmp[k] = aleatory(k)
            return func(**tmp)
        return other_func
    return randomize

def runFile(filepath):
    '''A function for iterating over the data files.'''

    f = file(filepath, 'r')
    for elem in f:
        elem = elem[:-1]
        if elem != '' and elem[0] != '#':
            yield elem
    f.close()

