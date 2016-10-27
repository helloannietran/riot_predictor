import nltk, re, pprint
from nltk import word_tokenize
from nltk.tokenize.api import TokenizerI
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
            print word
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

def match_rule_population(text):
    if does_match_group("people", text) and has_number(text):
        # print text
        return True
    return False

def match_rule_place(text):
    if does_match_group('in', text) and does_match_group("people", text):
        return True
    return False

def check_for_place(file):
    with open(file, 'r') as in_file:
        text = in_file.read()
        tiles = nltk.sent_tokenize(text)
        for i in xrange(0, len(tiles)):
            tiles[i] = tiles[i].strip()
            if match_rule_place(tiles[i]):
                print tiles[i]
                print '---------------'

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


fill_words()
# generate_paragraphs("example.txt")
check_for_place("example.txt")
# generate_paragraphs()
# print does_match_group("riot", "a riot happened in 1996")


