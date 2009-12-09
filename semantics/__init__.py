import concept
import entity

knowledge = {}
table = {}

def initKnowledge(pwd='./data/knowledge'):
    '''Initialize the concepts' knowledge.'''

    f = file(pwd+'/concept.csv', 'r')
    for elem in map(lambda(s): s[:-1], f.readlines()):
        if elem != '' and elem[0] != '#':
            x = concept.fromLine(elem)
        knowledge[x.index] = x
    f.close()

def initCategory(category, pwd='./data/knowledge'):
    '''
    Initializes the association between concepts and entities of a
    given lexical category.
    '''
    
    table[category] = []

    f = file(pwd+'/'+category+'.csv', 'r')
    for elem in map(lambda(s): s[:-1], f.readlines()):
        if elem != '' and elem[0] != '#':
            table[category].append(entity.fromLine(category, elem))
    f.close()

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
