class Contraction:
    '''
    Data model for contractions of preposition with following words.
    '''

    def __init__(self, index, rule, category, preposition, next, content):
        '''
        Attributes:
        - self.index: identifies the contraction;
        - self.rule: rule for declinations;
        - self.category: lexical category of next;
        - self.preposition: preposition to be contracted;
        - self.next: the word following the preposition;
        - self.content: root or list of the resulting contracted word.
        '''

        self.index = index
        self.rule = rule
        self.category = category
        self.preposition = preposition
        self.next = next
        self.content = content

    def term(self, gender, number):
        '''
        Returns an instance of the contraction, declining it according
        to the defined rule.
        '''

        return self.rule.apply(self.content, (gender, number))


def from_line(line, rules):
    '''Obtains a new Nominal instance from a line.'''

    data = line.split(',')
    rule = rules[data[0]]
    category = data[1]
    (preposition, next) = data[2].split('+')
    index = (preposition, next, category)
    content = data[3]
    return Contraction(index, rule, category, preposition, next, content)
