"""Fraseador

Usage:
  fraseador-cl.py [-N NUM] [-L]
  fraseador-cl.py (-h | --help)

Options:
  -h --help            Show this screen.
  -v --version         Show version and exit.
  -N NUM --number=NUM  Number of sentences to be generated [default: 20].
  -L --lines           Break line after each sentence.

"""
from __future__ import print_function

from docopt import docopt

from syntax import clause


def main():
    arguments = docopt(__doc__, version='1.0.0rc2')
    number = int(arguments.get('--number'))
    lines = bool(arguments.get('--lines'))
    end = '\n' if lines else ' '

    for i in xrange(number):
        sentence = repr(clause()).capitalize() + '.'
        print(sentence, end=end)

    if not lines:
        print()

if __name__ == '__main__':
    main()
