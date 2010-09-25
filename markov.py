#!/usr/bin/python
"""
Markov chain generator for making fantasy names and other made-up words.
"""
import re
import random
import sys
import collections

class CharList(collections.defaultdict):
    """models the list of characters in the histogram"""
    def __init__(self):
        """initializes the values to 0"""
        collections.defaultdict.__init__(self, int)

    def add(self, char):
        """adds a character value to the character list """
        self[char] += 1

    def total(self):
        """totals the values of a character list"""
        return sum(self.values())

    def choose(self):
        """returns a random value based on a key"""
        rnd = random.randrange(0, self.total())
        position = 0
        for char,count in self.items():
            position += count
            if rnd <= position:
                return char

class Histogram(collections.defaultdict):
    """The histogram of letter probabilities."""
    class START(object):pass
    class END(object):pass
    def __init__(self):
        collections.defaultdict.__init__(self, CharList)


class Chain(collections.defaultdict):
    """ """
    def __init__(self, corpus_files, dictionary_file, lookback = 2):
        """ initializes the Markov object. """
        df = open(dictionary_file, 'r')
        self.dictionary = df.readlines()
        self.corpus_files = corpus_files
        self.lookback = lookback

    def load_corpuses(self):
        """loads the corpuses"""
        for file_path in self.corpus_files:
            f = open(file_path,'r')
            char = f.read(1)

    def make_key(self):
        """makes the keys for the histogram."""
        key = []
        for i in range(self.lookback):
            key.push(Markov.START)

    def make_histogram(self, file_list, lookback = 2):
        """makes the Markov histogram"""
        # the markov frequency histogram
        histogram = {}
        # pattern for matching characters
        skip_pattern = re.compile("[\d\n]",re.UNICODE)
        eow_pattern = re.compile('^[ \.,\?!@#$%^&*\(\)\\\/\[\]"]', re.UNICODE)
        # load the files in the file list
        for file_path in file_list:
            f = open(file_path, 'r')
            # read the file by character
            last_char = '^' # use '^' as a special character denoting the start of a word.
            while True:
                char = f.read(1)
                if not char: break
                if eow_pattern.match(char):
                    char = '$' # used to denote end of a word
                else:
                    char = char.lower();
                if not skip_pattern.match(char):
                    if last_char not in histogram.keys():
                        histogram[last_char] = {}
                    if char not in histogram[last_char].keys():
                        histogram[last_char][char] = 0
                    histogram[last_char][char] += 1
                last_char = char
                if char == '$': last_char = '^'
        return histogram


    def __str__(self):
        "outputs the histogram and the dictionary of words."
        output = "Histogram:\n"
        for char in self.histogram.keys():
            output += char + "\n"
            output += str(self.histogram[char])
            output += "\n"
        output += "\nWords:\n"
        output += str(self.words)
        return output


    def make_words(self):
        "creates the word list from the histogram and the dictionary of English words."
        # seed the random number generator with the time
        random.seed()
        words = {}
        # loop over the words in the dictionary and create fake words for them
        for word in self.dictionary:
            current_word = ""
            # word starts with the '^' character
            char = '^'
            # determine the next character
            done =  False
            while char != '$': # end of word
                # add up all the totals from the current position to see what the top of the random range will be
                rand_total = 0
                for key in self.histogram[char]:
                    rand_total += self.histogram[char][key]
                selection = random.randrange(0, rand_total)
                # figure out which character in the histogram that random number points to
                index = 0
                for key in self.histogram[char]:
                    index += self.histogram[char][key]
                    if index > selection:
                        if ((len(current_word) < (len(word) * 0.50)) and key == '$'): continue
                        char = key
                        # append the character to the word in progress
                        current_word += char
                        break

                done = (char != '$') or (not len(current_word) > len(word) * 1.5)
            words[word.rstrip()] = current_word.rstrip('$')
        return words



if __name__ == "__main__":
    lookback = sys.argv[0]
else:
    lookback = 2

m = Markov(['corpus/english/1739.txt'],'small_dict.txt')
print m
