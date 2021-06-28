Fantasy Language Maker
----------------------

Makes fantasy language glossaries based on markov chains applied to text corpuses. Comes with some sample corpuses from Project Gutenberg. (http://www.gutenberg.org/wiki/Main_Page)

Requires an installation of the Python programming language version 3
http://www.python.org

This version requires both nltk and spacy for nlp for part of speech tagging.
In other words, to tell whether an English word is noun, verb, etc.

I found that determining part of speech outside the context of a sentence is inexact.
When there is ambiguity, nltk favors NN (noun) whereas spacy doesn't.
e.g. spacy tags elf as PRP (personal pronoun) and wizard as JJ (adjective),
nltk tags both elf and wizard as NN (noun) - which is more what I expect

So, if I'm looking for/expecting a noun, I use nltk. Otherwise, I use spacy.

To install these packages after python is installed:

```
pip3 install nltk
python3 -m nltk.downloader all
pip3 install spacy
python3 -m spacy download en_core_web_sm
```

To run:

on linux/mac 
From the command line, type './markov [options] <path to corpus> [path to additional corpus..]'

on windows
From the dos prompt, 'python markov [options] <path to corpus> [path to additional corpus..]'

```
Usage: markov [options]

Options:
  -h, --help            show this help message and exit
  -l LOOKBACK, --lookback=LOOKBACK
                        number of characters to look back in the chain
  -d DICTIONARY, --dictionary=DICTIONARY
                        dictionary file to use
```                        

You can get additional corpora from Project Gutenberg - download the 'utf-8' version. I recommend removing the Gutenberg headers and footers before running the program on it.

Limitations: I assume an english language dictionary so that I can add some advanced features that take into account word prefixes and suffixes.
