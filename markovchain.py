"""
Markov chain generator for making fantasy names and other made-up words.
"""
import string
import random
import sys
import collections
from optparse import OptionParser
from unicodedata import category
import csv
import spacy
import re
import nltk
# from spacy_syllables import SpacySyllables

class CharList(collections.defaultdict):
    """Models the list of characters in the chain. The characters
    each have a corresponding int value, which is the proportion of
    those characters which follow the key pattern. """
    def __init__(self):
        """initializes the values to 0"""
        collections.defaultdict.__init__(self, int)

    def add(self, char):
        self[char] += 1

    def total(self):
        return sum(self.values())

    def choice(self):
        """returns a random value based on a key"""
        rnd = random.randrange(0, self.total())
        position = 0
        for char,count in self.items():
            position += count
            if rnd <= position:
                return char

class Chain(collections.defaultdict):
    """The histogram of letter probabilities. It is keyed by tuples,
    the length of which is defined by the lookback parameter."""
    class START(object):pass
    class END(object):pass
    def __init__(self, lookback = 2):
        collections.defaultdict.__init__(self, CharList)
        self.lookback = lookback

    def add(self,string):
        """ adds a word to the chain """
        key = [Chain.START] * self.lookback
        for char in string:
            self[tuple(key)].add(char)
            key.append(char)
            key.pop(0)
        self[tuple(key)].add(Chain.END)

class MarkovChain(collections.defaultdict):
    """ """
    def __init__(self, corpus_files, dictionary_file, lookback = 2):
        """ initializes the Markov object. """
        with open(dictionary_file) as f:
            self.dictionary = f.read().splitlines()
        self.corpus_files = corpus_files
        self.lookback = lookback
        self.chain = Chain(self.lookback)
        self.load_corpuses()
        self.words = self.make_words()

    def load_corpuses(self):
        """loads the corpuses"""
        for file_path in self.corpus_files:
            f = open(file_path,'r')
            lines = f.readlines()
            for line in lines:
                for word in line.split():
                    word = ''.join(ch for ch in word if category(ch)[0] == 'L' )
                    self.chain.add(word.lower())

    def make_words(self):
        """ runs through the dictionary and makes a fantasy word for
        each entry in the 'real' dictionary """
        result = {}
        nlp = spacy.load("en_core_web_sm")
        """ Assuming the dictionary is English language """
        """ suffixes potentially added to nouns - not intended as an exhaustive list """
        nn_suffixes = ["enfolk", "hood", "ic", "inwood", "ish", "ishly", "ishness", "kin", "in", "land", "like", "lock", "ship", "wife", "wort", \
                        "ism", "ling", "ness", "y", \
                        "ess", "ly", "ry", \
                        "craft", "ed", "edly", "en", "ering", "ery"]
        nnRegex = ".*(" + "|".join(nn_suffixes) + ")$"
        nnDict = {}
        for nn in nn_suffixes:
            nnDict[nn] = self.make_word()
        """ prefixes that result in a verb """
        verb_prefixes = ["re", "dis", "over", "un", "mis", "out", "be", "co", "de", "fore", "inter", "pre", "sub", "trans", "under"]
        vpRegex = "^(" + "|".join(verb_prefixes) + ").*"
        vpDict = {}
        for vp in verb_prefixes:
            vpDict[vp] = self.make_word()
        for w in self.dictionary:
            s = w.strip()
            word = ""
            while True:
                word = self.make_word()
                if word not in result.values(): break
            doc = nlp(s)



            """ this tries to handle suffixes, but it gets some things wrong """
            if re.search(nnRegex, s):
                """ found word possibly with suffix """
                for nn in nn_suffixes:
                    if s.endswith(nn) and len(s) > len(nn):
                        baseWord = s[:len(s)-len(nn)]
                        if baseWord in self.dictionary and nltk.pos_tag([baseWord])[0][1].startswith("NN"):
                            if baseWord in result.keys():
                                """ if the word without prefix is saved """
                                result[s] = result[baseWord] + nnDict[nn]
                            else:
                                """ if the word without prefix is not saved """
                                result[baseWord] = word
                                result[s] = word + nnDict[nn]
                        else: result[s] = word
                        break
            elif doc[0].tag_.startswith("VB") and re.search(vpRegex, s):
                """ it's a verb and has a verb prefix """
                for vp in verb_prefixes:
                    if s.startswith(vp):
                        baseWord = s[len(vp):]
                        if baseWord in self.dictionary:
                            if baseWord in result.keys():
                                """ if the word without prefix is saved """
                                result[s] = vpDict[vp] + result[baseWord]
                            else:
                                """ if the word without prefix is not saved """
                                result[baseWord] = word
                                result[s] = vpDict[vp] + word
                        break
            else: result[s] = word
        return result

    def __str__(self):
        """ outputs the results of the corpuses applied to the
        dictionary file"""
        output = ""
        keys = list(self.words.keys())
        keys.sort()
        for key in keys:
            output += key + "," + self.words[key] + "\n"
        return output

    def make_word(self):
        """ makes a fantasy word from a series of random characters."""
        """ TODO: the limit is a bit of a hack - maybe make it an command-line option """
        LIMIT=8
        word = ""
        key = [Chain.START] * self.lookback
        while True:
            char = self.chain[tuple(key)].choice()
            if char == Chain.END: break
            word += char
            key += char
            key.pop(0)
        if len(word) > LIMIT:
            word = self.make_word()
        return word


def strip_chars(s, chars_to_strip = string.punctuation):
    """ Strips a series of characters from a string."""
    return s.translate(''.maketrans("",""), chars_to_strip)
