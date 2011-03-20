class Preposition:
    '''Data model for prepositions.'''

    def __init__(self, index):
        '''
        Attributes:
        - self.index: identifies a preposition;
        - self.contractions: defines eventual contractions with
          following words.
        '''

        self.index = index
        self.contractions = {}

    def term(self, gender, number, next=None):
        '''
        Returns an instance of the preposition, contracting it with
        the following word if needed.
        '''

        if next is not None and next in self.contractions:
            return self.contractions[next].term(gender, number)
        else:
            return self.index

    def set_contraction(self, next, resulting_word):
        self.contractions[next] = resulting_word

    def contracts(self, next):
        return next in self.contractions

def from_line(line):
    return Preposition(line)
