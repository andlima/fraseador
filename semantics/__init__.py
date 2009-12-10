import utils
import concept
import entity

knowledge = {}
table = {}

def initKnowledge(pwd):
    '''Initialize the concepts' knowledge.'''

    for elem in utils.runFile(pwd+'/concept.csv'):
        x = concept.fromLine(elem)
        knowledge[x.index] = x

def initCategory(category, pwd='./data/knowledge'):
    '''
    Initializes the association between concepts and entities of a
    given lexical category.
    '''
    
    table[category] = []

    for elem in utils.runFile(pwd+'/'+category+'.csv'):
        table[category].append(entity.fromLine(category, elem))

def _transitiveClosure(x):
    # Obtains, recursively, all the ancestors of a given concept.

    if knowledge[x].parents is None:
        return [x]
    return [x]+reduce(lambda p, q: p+q, map(_transitiveClosure,
                                            knowledge[x].parents))

def verifySemantics(general, particular):
    '''
    Verifies if a given general concept is compatible with a given
    particular concept, i.e., if the first belongs is among the
    latter's ancestors.
    '''
    
    if '*' in (general, particular):
        return True
    return general in _transitiveClosure(particular)
