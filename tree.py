debug = False

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
        self.children = children or []
        self.info = info or {}

    def left(self):
        '''Returns the leftmost descendant of the tree.'''

        if self.children:
            if hasattr(self.children[0], 'left'):
                return self.children[0].left()
            else:
                return self
        else:
            return self

    def right(self):
        '''Returns the rightmost descendant of the tree.'''

        if self.children:
            if hasattr(self.children[-1], 'right'):
                return self.children[-1].right()
            else:
                return self
        else:
            return self

    def asList(self):
        words = []
        for z in self.children:
            if hasattr(z, 'asList'):
                words.extend(z.asList())
            else:
                words.append(z)
        return words

    def __repr__(self):
        '''
        If this a leaf, returns the value representation, otherwise
        returns the representation for each child, separated by
        space. If info contains a 'pos' item, postpones its
        representation.
        '''

        if debug:
            if self.children:
                phrase = '("' + str(self.value) + '" ' + ' '.join(
                    map(lambda z: z.__repr__(), self.children)) + ')'
            else:
                if hasattr(self.value, 'category'):
                    phrase = self.value.category + ":" + self.value.__repr__()
                else:
                    phrase = "<>:" + self.value.__repr__()
        else:
            words = self.asList()
            for i, word in enumerate(words[:-1]):
                if word.info.get('next', None):
                    words[i+1].info['hide'] = True

            words = [i for i in words \
                         if not i.info.get('hide', False)]

            if self.children:
                phrase = ' '.join(map(lambda z: z.__repr__(), words))
            else:
                phrase = self.value.__repr__()

        if self.info.has_key("pos"):
            phrase += self.info["pos"]

        return phrase
