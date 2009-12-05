class Tree:
    '''Defines an auxiliary tree type.'''

    def __init__(self, value, children=None, info=None):
        ''' 
        Attributes:
        - self.value: the root value;
        - self.children: a list of the children; None for leaves;
        - self.info: a dict for additional info.
        '''

        self.value = value
        self.children = children
        self.info = info or {}

    def left(self):
        '''Returns the leftmost child of the root node.'''

        if self.children is not None:
            return self.children[0].left()
        else:
            return self

    def right(self):
        '''Returns the rightmost child of the root node.'''

        if self.children is not None:
            return self.children[-1].right()
        else:
            return self

    def __repr__(self):
        '''
        If this a leaf, returns the value representation, otherwise
        returns the representation for each child, separated by
        space. If info contains a 'pos' item, postpones its
        representation.
        '''

        if self.children is None:
            phrase = self.value.__repr__()
        else:
            phrase = ' '.join(map(lambda z: z.__repr__(), self.children))
        if self.info.has_key("pos"):
            phrase += self.info["pos"]
        return phrase
