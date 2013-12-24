class Nominal:
    '''
    Data model for noun-like words (nouns, adjectives, articles and
    pronouns).
    '''

    def __init__(self, index, rule, gender, number, content):
        '''
        Attributes:
        - self.index: identifies the nominal word;
        - self.rule: rule for declinations;
        - self.gender: * or in grammar.GENDERS;
        - self.number: * ou in grammar.NUMBERS;
        - self.content: word root or list.
        '''

        self.index = index
        self.rule = rule
        self.gender = gender
        self.number = number
        self.content = content

    def term(self, gender, number):
        '''
        Returns an instance of the word, declining it according to the
        defined rule.
        '''

        return self.rule.apply(self.content, (gender, number))

    def validate(self, gender, number):
        '''Verifies compatibility between word and suggested form.'''

        if self.gender not in (gender, '*'):
            return False
        if self.number not in (number, '*'):
            return False
        return True


def from_line(line, rules):
    '''Obtains a new Nominal instance from a line.'''

    data = line.split(',')
    index = data[2].split('/')[0]
    rule = rules[data[0]]
    tmp = data[1].split('/')
    gender = tmp[0]
    number = tmp[1]
    content = data[2]
    return Nominal(index, rule, gender, number, content)
