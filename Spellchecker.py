from collections import Counter
from re import *
from functools import reduce


def get_words(text):
    """
    Find all words in a text
    :param text:
    :return: list() of all words in a text in lowercase letters
    """
    return findall('\w+', text.lower())


def train(features):
    return Counter(features)


def d_one_edits(word):
    """
    Given a word, find all the words (don't have to be valid words) that are one edit away.
    :param word:
    :return: set() containing words that are one edit away from word
    """
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a,b in splits]
    transposes = [a + b[1] + b[0] + b[2:] for a,b in splits if len(b) > 1]
    replaces = [a + letter + b[1:] for a,b in splits for letter in ALPHABET if b]
    inserts = [a + letter + b for a,b in splits for letter in ALPHABET]
    return set(deletes + transposes + replaces + inserts)


def union(x,y):
    return x | y


def d_two_edits_for(word):
    """
    Given a word, find all valid words that are two edits away from word
    :param word:
    :return: set() containing valid words
    """
    return set(e2 for e1 in d_one_edits(word) for e2 in d_one_edits(e1) if e2 in DICTIONARY)


def d_two_edits_reduce(word):
    return reduce(union, map(d_one_edits, d_one_edits(word)), set())


def known(words):
    return set(word for word in words if word in DICTIONARY)


def correct(word, c):
    """
    Predict the 'correct' spelling of word, given a Counter
    :param word:
    :param c: contains the count of words in an iterable
    :return:
    """
    candidates = known([word]) or known(d_one_edits(word)) or d_two_edits_for(word) or [word]
    return max(candidates, key=lambda w : c[w])


def load_dictionary(filename):
    with open(filename,'r') as f:
        return set(get_words(f.read()))

with open('mobydick.txt','r') as f:
    word_counts = train(get_words(f.read()))
    print(correct('righ',word_counts))

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
DICTIONARY = load_dictionary('wordsEn.txt')

