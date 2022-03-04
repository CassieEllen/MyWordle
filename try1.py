# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import string
import copy
#from typing import List
import sys


class WordFilter:
    ''' WordFilter docs

    '''
    alphabet_string: str = string.ascii_lowercase
    alphabet_list: list[list[int]] = list(alphabet_string)

    def __init__(self):
        print('{' + self.__doc__ + '\n}')
        print(self.__class__.__name__)
        print(self.__class__.__str__(self))
        print(self.__str__)
        self.must_have = []
        self.patterns: list = []
        for i in range(0, 5):
            self.patterns.append(WordFilter.alphabet_list)
        self.print_patterns()

    def print_patterns(self) -> None:
        print('[' + ''.join(WordFilter.alphabet_list) + ']')


def load_words():
    filename = '5_letter_words.txt'
    with open(filename) as word_file:
        valid_words = set(word_file.read().split())
    return valid_words

def load_wordle_words() -> list:
    filename = 'wordle_words.txt'
    words = []
    with open(filename) as word_file:
        for line in word_file:
            ### Skip Comment lines
            if '#' == line[0]:
                continue
            words.append(line[:-1])
    #sys.exit("here")
    with open('temp.txt', 'w') as temp:
        for w in words:
            temp.write(w + '\n')
            #print(w)
    return words

'''
def setup_patterns(wf: WordFilter) -> WordFilter:
    patterns = []
    for i in range(0, 5):
        patterns.append(copy.deepcopy(WordFilter.alphabet_list))
    wf = WordFilter
    wf.patterns = patterns
    return patterns
'''

def print_patterns(patterns, label=None) -> None:
    if label:
        print(label + ' = ')
    print('[')
    for item in patterns:
        print('\t', item)
    print(']')

def create_word_pattern(patterns):
    print('create_word_pattern', patterns)
    pattern = '[';
    for index in range(0,5):
        pattern += ''.join(patterns[index]) + ']['
    # Remove the final '['
    pattern = pattern[:-1]
    return pattern

def find_matching_words(pattern, words):
    ''' Filter the words list using pattern

    :param pattern:
    :param words:
    :return:
    '''

    print('find_matching_words', pattern)
    # mhw is filtered words
    mhw = []

    # Control debug printing
    debugging = True
    debugging = False

    print('find_matching_words', len(words), pattern)
    exp = re.compile(pattern)

    # Uncomment to get everything
    #exp = re.compile('[a-z][a-z][a-z][a-z][a-z]')

    print('exp', exp)
    with open('temp.txt', 'w') as temp:
        print('words size', len(words))
        for w in words:
            if debugging:
                print('o', w)
            if( exp.match(w)):
                if debugging:
                    print('f', w)
                mhw.append(w)
                temp.write(w + '\n')
    return mhw


def filter_pattern(guess, patterns) -> list:
    ''' use input to filter parameter list

    :param guess: list
    :param patterns: list
    :return: Any
    '''

    print('filter_pattern', guess, patterns)

    letters = guess[0]
    values = guess[1]
    print("letters", letters, '\n', 'values', values)

    # Characters that must appear in the word. (From Y)
    must_have = []
    include = ''

    for index in range(0, 5):
        l: object = letters[index]
        v = values[index]
        print('filter: ', l, v, index)
        # Ensure only black, yellow, green blocks allowed
        if not v in 'bygi':
            raise TypeError('Invalid color type')
        if v == 'b':
            for i in range(0, 5):
                # print('l:', l)
                # print(i, l, patterns[i])
                if l in patterns[i]:
                    patterns[i].remove(l)
            print_patterns(patterns)
        if v == 'g':
            # Set the indexed value to only allow 'l'
            patterns[index] = [ l ]
            # remove l from all other patterns
            # use list() to convert range() to a list.
            r = list(range(0,5))
            print(r, type(r))
            r.remove(index)
            print(r, type(r))
            for i in r:
                patterns[i].remove(l)
            print_patterns(patterns)
        if v == 'y':
            print(patterns[index])
            if v in patterns[index]:
                patterns[index].remove(l)
            print_patterns(patterns)
            must_have.append(l)
            #must_have.append(v)
        if v == 'i':
            include += l
            print_patterns(patterns)
    print('must_have', must_have)
    return patterns


###############################################################################
# main
###############################################################################
if __name__ == '__main__':
    #wortle_words = load_words()
    wortle_words = load_wordle_words()
    print('starting with len wortle_words', len(wortle_words))
    #print(' '.join(wortle_words))

    wf = WordFilter()
    #setup_patterns(wf)
    #print_patterns(WordFilter.alphabet_list, "my_patterns after initial setup")
    print('my_patterns after initial setup ', end='')
    wf.print_patterns()
    sys.exit("debugging")

    word_pattern = create_word_pattern(wf.patterns)
    print('word_pattern', word_pattern)

    # First guess
    guess1 = ['roate', 'yybyg']

    # Filter pattern based on guess
    pattern1 = filter_pattern(guess1, WordFilter.alphabet_list)
    print_patterns(pattern1, 'after guess1')

    # Remove words not matching pattern1
    words1 = find_matching_words(create_word_pattern(pattern1), wortle_words)
    print('len(words1)', len(words1))


'''
    #l2 = ['reamy']
    #ords2 = filter_words(wortle_words, l2)
'''

### Information
'''
What do I know?
If it is yellow, then it cannot appear in that position, but must appear somewhere else. 
If it is green, then it must appear in that position, but may appear somewhere else. 
If it is black, then it must not appear. 

REAMY
bygbb



'''
