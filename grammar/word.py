from grammar import NOMINAL_CATEGORY_LIST

class Word:
    '''A word, described as an instance of a lexical category.'''

    def __init__(self, value, category, info):
        '''
        Attributes:
        - self.value: an instance of a lexical category
        - self.category: the word's lexical category
        - self.info: a dict containing info about the word, like
          number, gender, etc., used to obtain the correct
          declination/conjugation.
        '''

        self.value = value
        self.category = category
        self.info = info

    def __repr__(self):
        '''
        Returns a representation for the word, obtained by means of
        its lexical category.
        '''
        
        person = self.info.get('person')
        gender = self.info.get('gender')
        number = self.info.get('number')
        tense = self.info.get('tense')
        next = self.info.get('next')

        if self.category in NOMINAL_CATEGORY_LIST:
            return self.value.term(gender, number)
        if self.category == 'verb':
            return self.value.term(person, number, tense)
        if self.category == 'preposition':
            return self.value.term(gender, number, next)
        if self.category == 'possessive_pronoun':
            return self.value.term(gender, number)
        if self.category == 'personal_pronoun':
            return self.value.term(gender, number)
        raise UnknownCategoryError(self.category)
