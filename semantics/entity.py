import semantics

class Entity:
    '''
    Defines an entity, which relates a specific word to its
    corresponding concepts.
    '''

    def __init__(self, index, category, concept, gender=None,
                 number=None, preposition=None, transitivity=None):
        '''
        Attributes:
        - self.index: identifies the word;
        - self.category: the word's lexical category;
        - self.concept: the word's accepted concepts;
        - self.gender: for an adjective pronoun, its gender;
        - self.number: for an adjective pronoun, its number;
        - self.preposition: for a verb, its preposition, if any;
        - self.transitivity: for a verb, its transitivity.
        '''
        
        self.index = index
        self.category = category
        self.concept = concept
        self.gender = gender
        self.number = number
        self.preposition = preposition
        self.transitivity = transitivity

    def validateUse(self, use, gender, number):
        '''
        Validates whether the entity is compatible with a gender, a
        number and a use.
        '''

        if use != self.concept['use']:
            return False
        if self.gender not in (gender, '*'):
            return False
        if self.number not in (number, '*'):
            return False
        return True

    def includes(self, s, kind='base'):
        if kind not in self.concept.keys():
            return False
        return semantics.verify_semantics(self.concept[kind], s)

    def belongs(self, s, kind='base'):
        if kind not in self.concept.keys():
            return False
        return semantics.verify_semantics(s, self.concept[kind])

def from_line(category, line):
    '''Obtains an entity from a line.'''

    data = line.split(',')

    index = data[1]
    concept = {}
    concept['base'] = data[0]

    if category == 'adjective_pronoun':
        tmp = data[2].split('@')
        concept['use'] = tmp[0]
        if len(tmp) == 2:
            gender = tmp[1].split('/')[0]
            number = tmp[1].split('/')[1]
        else:
            gender = '*'
            number = '*'
            return Entity(index, category, concept, gender, number)

    if category == 'verb':
        # 0: subject concepts
        # 1: verb index
        # 2: verb transitivity
        transitivity = data[2]
        preposition = None
        if transitivity == 'vtd':
            # 3: direct object
            concept['OD'] = data[3]
        elif transitivity == 'vti':
            # 3: preposition / indirect object
            preposition = data[3].split('+')[0]
            concept['OI'] = data[3].split('+')[1]
        elif transitivity == 'vtdi':
            # 3: direct object
            # 4: preposition / indirect object
            concept['OD'] = data[3]
            preposition = data[4].split('+')[0]
            concept['OI'] = data[4].split('+')[1]
        return Entity(index, category, concept, preposition=preposition,
                      transitivity=transitivity)

    return Entity(index, category, concept)
