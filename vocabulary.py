import grammar
import rules

class Vocabulary:
    '''
    Class that centralizes the known words of different lexical
    categories.
    '''
    
    def __init__(self, pwd):
        '''
        Attribute:
        - self.data: dict of dicts; for each lexical category, maps
          each word's index to the instance of the word.
        '''

        self.rules = {}
        rules.init(self.rules)

        self.data = {}

        for category in grammar.EXTRA_LIST:
            self.data[category] = {}
            grammar.init(category, self.data[category], self.rules, pwd)

        # Associates contractions to corresponding prepositions
        for contraction in self.data['contraction'].values():
            prep = self.data['preposition'][contraction.prep]
            prep.set_contraction((contraction.next, contraction.category),
                                self.data['contraction'][contraction.index])
