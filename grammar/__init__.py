from os.path import join as join_path
import utils

import nominal
import verbal
import preposition
import personal_pronoun
import possessive_pronoun
import contraction


GENDERS = ['m', 'f']
PERSONS = ['1', '2', '3']
NUMBERS = ['s', 'p']
TENSES = ['pi', 'ppi', 'fpi']
NOMINAL_FORMS = ['ms', 'fs', 'mp', 'fp']
VERBAL_FORMS = ['1s', '2s', '3s', '1p', '2p', '3p']
TRANSITIVITIES = ['vi', 'vtd', 'vti', 'vtdi', 'vpi']

NOMINAL_CATEGORY_LIST = [
    'article',
    'noun',
    'adjective',
    'adjective_pronoun',
    'relative_pronoun',
]

CATEGORY_LIST = NOMINAL_CATEGORY_LIST + [
    'verb',
    'preposition',
    'personal_pronoun',
    'possessive_pronoun',
]

EXTRA_LIST = CATEGORY_LIST + ['contraction']
CONCEPTUAL_LIST = NOMINAL_CATEGORY_LIST + ['verb']

TENSE_DICT = {'pi': 'present', 'ppi': 'past', 'fpi': 'future'}

class UnknownCategoryError(Exception):
    pass

def init(extra, dic, rules, pwd):
    if extra not in EXTRA_LIST:
        raise UnknownCategoryError(extra)
    for elem in utils.run_file(join_path(pwd, extra+'.csv')):
        if extra in NOMINAL_CATEGORY_LIST:
            item = nominal.from_line(elem, rules)
        elif extra == 'verb':
            item = verbal.from_line(elem, rules)
        elif extra == 'preposition':
            item = preposition.from_line(elem)
        elif extra == 'personal_pronoun':
            item = personal_pronoun.from_line(elem, rules)
        elif extra == 'possessive_pronoun':
            item = possessive_pronoun.from_line(elem, rules)
        elif extra == 'contraction':
            item = contraction.from_line(elem, rules)
        dic[item.index] = item
