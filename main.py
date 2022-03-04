# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import string
import copy

alphabet_string = string.ascii_lowercase
alphabet_list = list(alphabet_string)

base_list = alphabet_list

def load_words():
    filename = '5_letter_words.txt'
    with open(filename) as word_file:
        valid_words = set(word_file.read().split())
    return valid_words

def print_patterns(patterns):
    print('patterns = [')
    for item in patterns:
        print('\t', item)
    print(']')

def filter_words(words, input):
    patterns = [];
    include = '['
    exclude = '['
    must_have = ''
    letters = input[0]
    values = input[1]
    print(letters, values)

    # Create a list of patterns. One for each character position.
    for i in range(0,5):
        patterns.append(copy.deepcopy(alphabet_list))
    print_patterns(patterns)

    for index in range(0,5):
        l = letters[index]
        v = values[index]
        print(l, v)
        # Ensure only black, yellow, green blocks allowed
        if not v in 'byg':
            raise TypeError('Invalid color type')
        # Add must_have char
        if v == 'g':
            must_have = must_have + l
            patterns[index] = [ l ]
        else:
            must_have = must_have + '.'

        if v == 'y':
            include = include + l
            patterns[index].remove(l)
            print_patterns(patterns)

        if v == 'b':
            exclude = exclude + l
            base_list.remove(l)
            for i in range(0, 5):
                #print('l:', l)
                #print(i, l, patterns[i])
                if l in patterns[i]:
                    patterns[i].remove(l)
            print_patterns(patterns)

        if v == 'i':
            include += l
            print_patterns(patterns)

    include = include + ']'
    exclude = exclude + ']'

    print('must_have: ' + must_have)
    must_have_pat = re.compile(must_have)
    include_pat = re.compile(include)
    exclude_pat = re.compile(exclude)
    print('must_have_pat:', must_have_pat)
    print('include_pat: ', include_pat)
    print('exclude_pat:', exclude_pat)
    base_pat = re.compile('[' + ''.join(base_list) + ']')
    print(len(base_list), base_list, base_pat)
    print_patterns(patterns)



    # filter words
    mhw = []
    for w in words:
        if not re.match(must_have_pat, w):
            continue
        if not re.search(include_pat, w):
            continue
        if re.search(exclude_pat, w):
            continue
        mhw.append(w)
    print('new size:', len(mhw))
    with open('temp.txt', 'w') as temp:
        for w in mhw:
           temp.write(w + '\n')
    return mhw

if __name__ == '__main__':
    wortle_words = load_words()
    print('starting with size:', len(wortle_words))

### block comment
    l1 = ['roate', 'yybyg']
    words1 = filter_words(wortle_words, l1)
    print('after l1 size:', len(words1))

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
