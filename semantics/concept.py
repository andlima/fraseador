class Concept:
    '''Defines a concept and its parents concepts.'''

    def __init__(self, index, parents=None):
        '''
        Attributes:
        - self.index: identifies a concept;
        - self.parents: this concept's parents.
        '''

        self.index = index
        self.parents = parents

def fromLine(elem):
    '''Obtains a concept from a line.'''

    data = elem.split(':') 
    index = data[0]
    parents = None
    if len(data) == 2:
        parents = data[1].split(',')
    return Concept(index, parents)
