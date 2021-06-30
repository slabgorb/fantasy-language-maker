Fantasy Language Maker
----------------------

Makes fantasy language glossaries based on markov chains applied to text corpuses. Comes with some sample corpuses from Project Gutenberg. (http://www.gutenberg.org/wiki/Main_Page)

Requires an installation of the Python programming language version 3
http://www.python.org

This version requires both nltk for natural language processing.

To install nltk after python is installed:

```
pip3 install nltk
python3 -m nltk.downloader all
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
  -a APPEND_TO, --appendto=APPEND_TO
                        file to append to
  -d DICTIONARY, --dictionary=DICTIONARY
                        dictionary file to use
  -n NAME, --name=NAME  Name of the language, if this is set, the output will
                        go into a file

```                        

You can get additional corpora from Project Gutenberg - download the 'utf-8' version. I recommend removing the Gutenberg headers and footers before running the program on it.

Improvements over the original:
* related words like "elf" and "elfish" should render words that look like they are related
* uses nlp to intelligently detect verb prefixes and noun prefixes and suffixes
* option to append to already-generated list of words so you can start out with the small dictionary and iteratively add onto it with larger or custom dictionaries without overwriting what you already had
* Additions to the small dictionary
* A medium-sized dictionary (from http://www.mieliestronk.com/wordlist.html)
* A very larger dictionary (from https://github.com/dwyl/english-words)

Limitations:
* I assume an english language dictionary so that I can add some advanced features that take into account word prefixes and suffixes.
* handling of prefixes and suffixes is not exhaustive or perfect

TODO:
* improve prefix and suffix handling, maybe make the prefixesa nd suffixes come from a file so they are customizable
* improve performance
