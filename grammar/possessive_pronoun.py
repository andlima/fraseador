import nominal

class PossessivePronoun(nominal.Nominal):
    '''Data model for possessive pronouns.'''

    def __init__(self, index, rule, gender, number, content,
                 ant_person, ant_number):
        '''
        Attributes:
        - (see Nominal and...)
        - self.ant_person: antecedent's person (in grammar.PERSONS or
          '*');
        - self.ant_number: antecedent's number (in grammar.NUMBERS or
          '*').
        '''

        self.index = index
        self.rule = rule 
        self.gender = gender
        self.number = number
        self.content = content
        self.ant_person = ant_person
        self.ant_number = ant_number

    def validate(self, gender, number, ant_person, ant_number):
        '''Verifies compatibility between word and suggested form.'''

        if not nominal.Nominal.validate(self, gender, number):
            return False
        if self.ant_person not in (ant_person, '*'):
            return False
        if self.ant_number not in (ant_number, '*'):
            return False
        return True

def from_line(line, rules):
    '''Obtains a new PersonalPronoun instance from a line.'''

    n = nominal.from_line(line, rules)
    tmp = line.split(',')[1].split('/')
    ant_person = tmp[2]
    ant_number = tmp[3]
    return PossessivePronoun(n.index, n.rule, n.gender, n.number,
                             n.content, ant_person, ant_number)
