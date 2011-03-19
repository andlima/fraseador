class Verbal:
    '''Data model for verbs.'''

    def __init__(self, index, rule):
        '''
        Attributes:
        - self.index: identifies the verb;
        - self.rule: rule for the conjugation.
        '''

        self.index = index
        self.rule = rule

    def term(self, person, number, tense):
        '''
        Returns an instance of the verb, conjugating for given person,
        number and tense, using its rule.
        '''

        return self.rule.apply(self.index, tense, person + number)

def from_line(line, rules):
    '''Obtains a new Verbal instance from a line.'''

    rule, index = line.split(',')
    return Verbal(index, rules[rule])
