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

NOMINAL_CLASS_LIST = [
    'article', 'noun', 'adjective', 'adjective_pronoun',
    'relative_pronoun']

CLASS_LIST = NOMINAL_CLASS_LIST + [
    'verb', 'preposition',
    'personal_pronoun',
    'possessive_pronoun']

EXTRA_LIST = CLASS_LIST + ['contraction']

CONCEPTUAL_LIST = NOMINAL_CLASS_LIST + ['verb']

TENSE_DICT = {'pi': 'present', 'ppi': 'past', 'fpi': 'future'}

def init(extra, dic, rules, pwd):
    for elem in utils.runFile(pwd+'/'+extra+'.csv'):
        if extra in NOMINAL_CLASS_LIST:
            tmp = nominal.fromLine(elem, rules)
        elif extra == 'verb':
            tmp = verbal.fromLine(elem, rules)
        elif extra == 'preposition':
            tmp = preposition.fromLine(elem)
        elif extra == 'personal_pronoun':
            tmp = personal_pronoun.fromLine(elem, rules)
        elif extra == 'possessive_pronoun':
            tmp = possessive_pronoun.fromLine(elem, rules)
        elif extra == 'contraction':
            tmp = contraction.fromLine(elem, rules)
        else:
            raise 'Unknown class: ' + extra
        dic[tmp.index] = tmp
