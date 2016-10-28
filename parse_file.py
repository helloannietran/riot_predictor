import nltk, re, pprint
from nltk import word_tokenize, FreqDist
from nltk.tokenize.api import TokenizerI
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from os import listdir
from os.path import isfile, join

# sentence = "Michael Jackson likes to eat at McDonalds"
# tagged_sent = pos_tag(sentence.split())
# # [('Michael', 'NNP'), ('Jackson', 'NNP'), ('likes', 'VBZ'), ('to', 'TO'), ('eat', 'VB'), ('at', 'IN'), ('McDonalds', 'NNP')]

# propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
# ...
def find_most_frequent_noun(text, count):
    words = text.split()
    tagged_sent = pos_tag(words)
# [('Michael', 'NNP'), ('Jackson', 'NNP'), ('likes', 'VBZ'), ('to', 'TO'), ('eat', 'VB'), ('at', 'IN'), ('McDonalds', 'NNP')]

    propernouns = [word for word,pos in tagged_sent if pos == 'NNP']

    # words = word_tokenize(text)
    fdist1 = FreqDist(propernouns)
    most_common = fdist1.most_common(count)

    # print most_common
    return most_common
    # filtered_words = [word for word in word_list if word not in stopwords.words('english')]

bag_of_words = {}

def fill_words():
    global bag_of_words
    with open("BagOfWords.txt", 'r') as in_file:
        text = in_file.read()
        bag_of_words = eval(text)
        # print bag_of_words

def does_match_group(group, text):
    global bag_of_words
    if group not in bag_of_words:
        if text.find(group) is not -1:
            return True
        return False

    for word in bag_of_words[group]:
        text = text.lower()
        if text.find(word) is not -1:
            #print word
            return True
    return False

def match_rule_riot(text):
    if does_match_group('riot', text) and does_match_group('happen', text):
        return True

def has_number(text):
    words = word_tokenize(text)
    words = [word for word in words if word.isdigit()]
    if len (words) > 0:
        return True
    return False

def get_number(group, text):
    words = word_tokenize(text)
    words = [word for word in words if word.isdigit()]
    if len (words) > 0:
        for word in bag_of_words[group]:
            text = text.lower()
            if text.find(word) is not -1:
                #print word
                for number in words:
                    sample = number + " " + word
                    if text.find(sample) is not -1:
                        print number

def match_rule_population(text):
    if does_match_group("people", text) and has_number(text):
        # print text
        return True
    return False

def match_rule_place(text):
    if does_match_group('in', text) and does_match_group("people", text):
        return True
    return False

import nltk.corpus  
from nltk.text import Text  
# moby = Text(nltk.corpus.gutenberg.words('melville-moby_dick.txt'))

def check_for_place(file, count):
    # nltk_text = Text(nltk.corpus.gutenberg.words(file))
    with open(file, 'r') as in_file:
        print 'processing %s' %file
        text = in_file.read()
        most_common = find_most_frequent_noun(text, count)
        return most_common
        # nltk_text.concordance(most_common[0][0])
        # tiles = nltk.sent_tokenize(text)
        # for i in xrange(0, len(tiles)):
        #     tiles[i] = tiles[i].strip()
        #     if match_rule_place(tiles[i]):
        #         print tiles[i]
        #         print '---------------'

def check_for_population(file):
    with open(file, 'r') as in_file:
        text = in_file.read()
        tiles = nltk.sent_tokenize(text)
        for i in xrange(0, len(tiles)):
            tiles[i] = tiles[i].strip()
            if match_rule_population(tiles[i]):
                print tiles[i]
                print '---------------'

def generate_paragraphs(file):
    with open(file, 'r') as in_file:
        text = in_file.read()
        ttt = nltk.tokenize.TextTilingTokenizer()
        tiles = ttt.tokenize(text)
        for i in xrange(0, len(tiles)):
            tiles[i] = tiles[i].strip()
            if match_rule_riot(tiles[i]):
                print tiles[i]
                print '---------------'

            # print "%d: %s\n-------------------\n" %(i, tiles[i])
        
        # t = Tokenizer()
        # t.tokenize(text)

BLOCK_COMPARISON, VOCABULARY_INTRODUCTION = 0, 1
LC, HC = 0, 1
DEFAULT_SMOOTHING = [0]


class Tokenizer(TokenizerI):
    def __init__(self,
             w=20,
             k=10,
             similarity_method=BLOCK_COMPARISON,
             stopwords=None,
             smoothing_method=DEFAULT_SMOOTHING,
             smoothing_width=2,
             smoothing_rounds=1,
             cutoff_policy=HC,
             demo_mode=False):


        if stopwords is None:
            from nltk.corpus import stopwords
            stopwords = stopwords.words('english')
        self.__dict__.update(locals())
        del self.__dict__['self']

    def tokenize(self, text):
        """Return a tokenized copy of *text*, where each "token" represents
        a separate topic."""

        lowercase_text = text.lower()
        paragraph_breaks = self._mark_paragraph_breaks(text)
        print "ppp: %s" % paragraph_breaks
        # text_length = len(lowercase_text)


def get_all_files_in_dir(mypath):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

fill_words()

def find_and_write_to_csv_cities():
# generate_paragraphs("example.txt")
    all_files = get_all_files_in_dir('articles/')
    all_files = ['articles/' + file for file in all_files]
    with open("results_place.csv", 'w') as out_file:

        for file in all_files:
            most_common = check_for_place(file, 15)
            out_file.write('%s\t %s\t %s\n' %(file, most_common[0][0], str(most_common))) 

find_and_write_to_csv_cities()
# check_for_place("articles/18_May_Riot.txt")
# check_for_place("/Users/BARNES_3/Documents/niki/courses/Decision making/riot_predictor/articles/18_May_Riot.txt")
# check_for_population("example.txt")
# check_for_place("example.txt")
# generate_paragraphs()
# print does_match_group("riot", "a riot happened in 1996")


