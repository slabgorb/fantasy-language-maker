#!/usr/bin/python
import re
import random
import sys


class Markov:
    def __init__(self, corpus_files, dictionary_file, lookback = 2):
        """ initializes the Markov object. """
        df = open('small_dict.txt','r')
        self.dictionary = df.readlines()
        self.histogram = self.make_histogram(corpus_files, lookback)
        self.words = self.make_words()

    def make_histogram(self, file_list, lookback = 2):
        # the markov frequency histogram
        histogram = {}
        # pattern for matching characters
        skip_pattern = re.compile("[\d]",re.UNICODE)
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
