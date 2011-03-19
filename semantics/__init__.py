from utils import runFile
from os.path import join as join_path
import concept
import entity

knowledge = {}
table = {}

def init_knowledge(pwd):
    '''Initialize the concepts' knowledge.'''

    for elem in runFile(join_path(pwd, 'concept.csv')):
        x = concept.from_line(elem)
        knowledge[x.index] = x

def init_category(category, pwd=join_path('.', 'data', 'knowledge')):
    '''
    Initializes the association between concepts and entities of a
    given lexical category.
    '''
    
    table[category] = [
        entity.from_line(category, elem)
        for elem in runFile(join_path(pwd, category+'.csv'))
    ]

def ancestors_and_self(x):
    '''Obtains, recursively, all the ancestors of a given concept.'''

    if knowledge[x].parents is None:
        return [x]
    return [x] + reduce(lambda p, q: p+q,
                        [ancestors_and_self(p)
                         for p in knowledge[x].parents])

def verify_semantics(general, particular):
    '''
    Verifies if a given general concept is compatible with a given
    particular concept, i.e., if the first belongs is among the
    latter's ancestors.
    '''
    
    if '*' in (general, particular):
        return True
    return general in ancestors_and_self(particular)
