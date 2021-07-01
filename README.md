Fantasy Language Maker
----------------------

Makes fantasy language glossaries based on markov chains applied to text corpuses. Comes with some sample corpuses from Project Gutenberg. (http://www.gutenberg.org/wiki/Main_Page)

Requires an installation of the Python programming language version 3
http://www.python.org

This version requires nltk and pattern for natural language processing.

pattern also requires mysql.

To intall mysql on macos you just need to run:

```
brew install mysql
```

For Windows or Linux, refer to https://dev.mysql.com/doc/mysql-getting-started/en/. 

To install nltk and pattern after python and mysql are installed:

```
pip3 install nltk
python3 -m nltk.downloader all
pip3 install pattern
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
                        file to append to, use in conjunction with -s
  -d DICTIONARY, --dictionary=DICTIONARY
                        dictionary file to use
  -n NAME, --name=NAME  Name of the language, if this is set, the output will
                        go into a file
  -s SEED, --seed=SEED  random seed, use in conjunction with -a

```                        

To keep track of the random seed, I let the shell create the seed and name the file with the seed.

```
seed=$RANDOM; ./markov corpus/english.txt -s $seed | tee english_corpus_$seed.txt | less
```

When I like the result with the smaller file, then I can follow up with a larger dictionary.

You can get additional corpora from Project Gutenberg - download the 'utf-8' version. I recommend removing the Gutenberg headers and footers before running the program on it.

Improvements over the original:
* related words like "elf" and "elfish" should render words that look like they are related
* uses nlp to intelligently detect verb prefixes and noun prefixes and suffixes
* option to append to already-generated list of words so you can start out with the small dictionary and iteratively add onto it with larger or custom dictionaries without overwriting what you already had
* ability to specify a seed for random number generation
* Additions to the small dictionary
* A medium-sized dictionary (from http://www.mieliestronk.com/wordlist.html)
* A very larger dictionary (from https://github.com/dwyl/english-words)

Limitations:
* I assume an english language dictionary so that I can add some advanced features that take into account word prefixes and suffixes.
* handling of prefixes and suffixes is not exhaustive or perfect
* uses English pluralization rules

TODO:
* save suffixes and prefixes so I get the same one
* add more prefixes and suffixes
* maybe make the prefixesa nd suffixes come from a file so they are customizable
* improve performance
