import nominal

class Contraction:
    '''
    Data model for contractions of preposition with following words.
    '''

    def __init__(self, index, rule, category, prep, next,
                 content):
        '''
        Attributes:
        - self.index: identifies the contraction;
        - self.rule: rule for declinations;
        - self.category: lexical category of next;
        - self.prep: preposition to be contracted;
        - self.next: the word following the preposition;
        - self.content: root or list of the resulting contracted word.
        '''

        self.index = index
        self.rule = rule
        self.category = category
        self.prep = prep
        self.next = next
        self.content = content

    def term(self, gender, number):
        '''
        Returns an instance of the contraction, declinating it
        according to the defined rule.
        '''

        return self.rule.apply(self.content, (gender, number))

def from_line(line, rules):
    '''Obtains a new Nominal instance from a line.'''

    data = line.split(',')
    rule = rules[data[0]]
    category = data[1]
    (prep, next) = data[2].split('+')
    index = (prep, next, category)
    content = data[3]
    return Contraction(index, rule, category, prep, next,
                       content)

