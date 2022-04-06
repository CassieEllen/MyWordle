#!/usr/bin/python3
# This is a sample Python script.
### Information
"""
What do I know?
If it is yellow, then it cannot appear in that position, but must appear somewhere else.
If it is green, then it must appear in that position, but may appear somewhere else.
If it is black, then it must not appear.

REAMY
bygbb



"""

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import string
import copy
# from typing import List
import sys
from typing import List

wortle_words_filename = 'wordle_words.txt'


def str_to_codes(s: str) -> list:
    l = list(s)
    cl = []
    for c in list(s):
        cl.append(ord(c))
    return cl


class WordGuess:
    """

    """

    def __init__(self, letters: str, result: str) -> None:
        self.letters = letters
        self.result = result

    def __str__(self, label=None, end='\n'):
        s: str = ''
        if end:
            eol = end
        else:
            eol = ''
        if label:
            s += label + ' = '
        indent = '\t'
        s += '{' + eol
        s += indent + 'letters = ' + self.letters + eol
        s += indent + 'result = ' + self.result + eol
        s += '}' + eol
        return s


class WordFilter:
    """
    WordFilter docs

    Attributes
    ----------
    alphabet_string : string
    alphabet_list : list[string]

    Methods
    -------
    print_patterns():
        prints the attribute self.patterns

    """
    alphabet_string: str = string.ascii_lowercase
    alphabet_list = list(alphabet_string)
    debug = False

    def __init__(self):
        # print('doc = <doc>' + self.__doc__ + '</doc>')
        # print(self.__class__.__name__)
        # print(self.__class__.__str__(self))
        # print(self.__str__)

        self.must_have = []
        self.must_not_have = []
        self.patterns: list[list[str]] = []

        for i in range(0, 5):
            # Simple assignment just copies a reference to WordFilter.alphabet_list
            # so copy.copy() needs to be called.
            # self.patterns.append(WordFilter.alphabet_list)
            self.patterns.append(copy.copy(self.alphabet_list))

        if self.debug:
            print(self.__str__(label='WordFilter ctor', end='\n'))
            self.patterns[0].remove('a')
            print(self.get_pattern(WordFilter.alphabet_list))
            print(self.get_patterns(self.patterns))
            # print(self.__str__(label='WordFilter ctor', end='\n'))

    def get_pattern(self, pattern: list[str]) -> str:
        s: str = '[' + ''.join(pattern) + ']'
        return s

    def get_patterns(self, patterns, label=None, indent=None, end=None) -> str:
        if not indent:
            indent = ''
        # indent = '<' + indent + '>'
        if label:
            # print('label: ' + label)
            label = label + ': '
            # print('setting label to \'' + label + '\'')
        else:
            label = ''
            # print('setting label to \'' + label + '\'')
        eol: str = ''
        if end:
            eol = end
        # eol = '{' + eol + '}'
        s: str = ''
        s = label
        s += '[' + eol
        for v in patterns:
            s += indent + self.get_pattern(v)
        s += ']'
        return s

    def process_guess(self, guess: str, result: str):
        gl = list(guess)
        rl = list(result)
        must_have = []
        must_not_have = []
        if len(gl) != 5:
            raise Exception("guess must be 5 characters")
        if len(rl) != 5:
            raise Exception("result must be 5 characters")
        for i in range(5):
            letter = gl[i]
            color: str = rl[i]
            print(i, letter, color, end='')
            if 'b' == color:
                print(' black: ' + letter)
                self.must_not_have.append(letter)
                for j in range(5):
                    if letter in self.patterns[j]:
                        self.patterns[j].remove(letter)
                print(self.get_patterns(self.patterns, label='black' + ' ' + color), '\n')
            elif 'y' == color:
                print(' yellow: ' + letter)
                self.must_have.append(letter)
                if letter in self.patterns[i]:
                    self.patterns[i].remove(letter)
                print(self.get_patterns(self.patterns, label='yellow' + ' ' + color), '\n')
            elif 'g' == color:
                print(' green: ' + letter)
                self.patterns[i] = [letter]
                print(self.get_pattern(self.patterns[i]))
                print(self.get_patterns(self.patterns, label='green' + ' ' + color), '\n')
            else:
                print('Invalid color code', color)
                raise Exception("Invalid result color: " + color)

    def get_regex_pattern(self):
        s: string = ''
        for p in self.patterns:
            s += self.get_pattern(p)
        if self.debug:
            print('get_regex_pattern:', s)
        return s

    def __str__(self, label=None, end='\n'):
        print('WordFilter.class: ' + self.__class__.__name__)
        indent = ''
        if label:
            print(label + ' = ')
            indent = '\t'
        else:
            print('label not set')
        if not end:
            print('set eol to empty string: {}')
            eol = ''
        else:
            if self.debug:
                print('set eol to end: {' + end + '}')
                print('end codes:', str_to_codes(end))
            eol = end
        if self.debug:
            eol = '{' + eol + '}'
        else:
            eol = eol

        s: str = ''
        s = '{' + eol
        s += indent + 'alphabet_string: ' + WordFilter.alphabet_string + '\n'
        s += indent + self.get_patterns(WordFilter.alphabet_list, label='alphabet_list', indent='', end=None) + '\n'
        s += indent + 'must_have: [' + ''.join(self.must_have) + ']' + '\n'
        s += indent + 'must_not_have: [' + ''.join(self.must_not_have) + ']' + '\n'
        s += indent + self.get_patterns(self.patterns, label='patterns') + '\n'
        s += '}' + eol
        return s


def load_wordle_words() -> list:
    filename: str = wortle_words_filename
    words = []
    with open(filename) as word_file:
        for line in word_file:
            # Skip Comment lines
            if '#' == line[0]:
                continue
            words.append(line[:-1])
    # sys.exit("here")
    with open('temp.txt', 'w') as temp:
        for w in words:
            temp.write(w + '\n')
            # print(w)
    return words


def find_matching_words(wf: WordFilter, words: list) -> list:
    """ Filter the words list using pattern

    :param pattern:
    :param words:
    :return:
    """

    pattern = wf.get_regex_pattern()
    print('find_matching_words', pattern)

    # new_words will contain the filtered word list
    new_words = []

    # Control debug printing
    # debugging = True
    debugging = False

    print('find_matching_words', len(words), pattern)
    exp = re.compile(pattern)

    # Uncomment to get everything
    # exp = re.compile('[a-z][a-z][a-z][a-z][a-z]')

    print('exp', exp)
    with open('temp.txt', 'w') as temp:
        print('original words:', len(words))
        for w in words:
            # if debugging:
            #    print('o', w)
            if exp.match(w):
                if debugging:
                    print('f', w)
                good = True
                for c in wf.must_have:
                    if not c in w:
                        good = False
                        continue
                if good:
                    new_words.append(w)
                    temp.write(w + '\n')
    print('remaining words:', len(new_words))
    return new_words


###############################################################################
# __main__
###############################################################################
if __name__ == '__main__':
    wortle_words = load_wordle_words()
    print('starting with wortle_words', len(wortle_words))
    # print('wortle_words: ' + ' '.join(wortle_words)[:75] + '...')

    wf = WordFilter()
    print(wf.get_pattern(wf.patterns[1]))

    guesses = [['adieu', 'bbygb'], ['build', 'bbybb'], ['vixen', 'bgbgy'], ['finer', 'ggggg']]
    guesses = [['adieu', 'bbbby'], ['brush', 'gyybb'], ['burly', 'gggbb'], ['burnt', 'ggggg']]
    start_words = wortle_words
    count = 0
    for guess in guesses:
        ++ count
        print(guess[0], guess[1])
        print(wf.__str__(label='guess ' + str(count)))
        wf.process_guess(guess[0], guess[1])
        new_words = find_matching_words(wf, start_words)
        start_words = new_words
        # If only one word left, the print it.
        if len(start_words) == 1:
            print(start_words)

    sys.exit('done')
    #################################################################
    #################################################################

    # Create must_not list based upon black letters
    must_not = wf.alphabet_list
    # must_not.remove('b')
    # must_not.remove('e')
    # must_not.remove('g')
    # must_not.remove('h')
    # must_not.remove('i')
    # must_not.remove('k')
    # must_not.remove('t')
    must_not.remove('u')
    # must_not.remove('w')
    print('\nmust_not: ' + wf.get_pattern(must_not), len(must_not))

    # Set initial patterns
    wf.patterns[0] = ['a']
    wf.patterns[1] = copy.copy(must_not)
    wf.patterns[2] = ['i']
    wf.patterns[3] = copy.copy(must_not)
    wf.patterns[4] = copy.copy(must_not)
    for p in wf.patterns:
        print('\t', len(p))
    print('\nmust_not: ' + wf.get_pattern(must_not), len(must_not))

    # Remove yellow characters
    # wf.patterns[0].remove('s')
    wf.patterns[1].remove('d')
    # wf.patterns[2].remove('o')
    wf.patterns[3].remove('e')
    # wf.patterns[4].remove('n')
    for p in wf.patterns:
        print('\t', len(p))
    print('\nmust_not: ' + wf.get_pattern(must_not), len(must_not))

    pattern = wf.get_regex_pattern()
    print('patterns:', pattern)
    exp = re.compile(pattern)
    print('exp', exp)
    print(wf.get_patterns(label='first try words'))
    word_list = find_matching_words(pattern, wortle_words)

    # Eliminage words not containing all required characters
    words1 = []
    must_have = ['d', 'e']
    for w in word_list:
        good = True
        for c in must_have:
            if not c in w:
                good = False
                continue
        if good:
            words1.append(w)
    for w in words1:
        print(w, end=' ')
    print()

    # sys.exit('debugging')
    exit(-1)
