import nominal

class PersonalPronoun(nominal.Nominal):
    '''Data model for personal pronouns.'''

    def __init__(self, index, rule, gender, number, content,
                 person, functions, tonic):
        '''
        Attributes:
        - (see Nominal and...)
        - self.person: grammatical person (in grammar.PERSONS or '*');
        - self.functions: S, DO, IO, R;
        - self.tonic: a for atonic, t for tonic.
        '''

        nominal.Nominal.__init__(self, index, rule, gender, number,
                                 content)

        self.person = person
        self.functions = functions
        self.tonic = tonic

    def validate(self, person, number, gender, function, tonic):
        '''Verifies compatibility between word and suggested form.'''

        if not nominal.Nominal.validate(self, gender, number):
            return False
        if self.person not in (person, '*'):
            return False
        if function not in self.functions:
            return False
        if self.tonic != tonic:
            return False
        return True

def from_line(line, rules):
    '''Obtains a new PersonalPronoun instance from a line.'''

    n = nominal.from_line(line, rules)
    tmp = line.split(',')[1].split('/')
    person = tmp[2]
    functions = tmp[3].split('|')
    tonic = tmp[4]
    return PersonalPronoun(n.index, n.rule, n.gender, n.number,
                           n.content, person, functions, tonic)
