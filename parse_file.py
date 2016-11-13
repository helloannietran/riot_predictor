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
def startswith_nonchar(word):
    special_chars = ['!', '(', ')', '"', "'", '.', '}', '{', ':', ';', ',', '$', '%', '^', '&', '@', '#', '*', '\\', '/', '=', '-', '_', '<', '>', '`', 'riot', '|', '+', 'united', 'states', 'us', 'usa', 'news']
    # ret_val = False
    # for c in special_chars:
    #     if word.lower().find(c) > -1:
    #         return True
    return False

# def sum_up_vars(l):
#     l2 = {}
#     for i,j in l:
#         print i, j
#         if not i :
#             continue
#         if not i in l2:
#             l2[i] = 0
#         l2[i] += j
#     l3 = [(k, l2[k]) for k in l2.keys()]
#     return l3
# import nltk
from nltk.collocations import *
# >>> bigram_measures = nltk.collocations.BigramAssocMeasures()
# >>> trigram_measures = nltk.collocations.TrigramAssocMeasures()
# >>> finder = BigramCollocationFinder.from_words(
# ...     nltk.corpus.genesis.words('english-web.txt'))
# >>> finder.nbest(bigram_measures.pmi, 10)  # doctest: +NORMALIZE_WHITESPACE
# [(u'Allon', u'Bacuth'), (u'Ashteroth', u'Karnaim'), (u'Ben', u'Ammi'),
#  (u'En', u'Mishpat'), (u'Jegar', u'Sahadutha'), (u'Salt', u'Sea'),
#  (u'Whoever', u'sheds'), (u'appoint', u'overseers'), (u'aromatic', u'resin'),
#  (u'cutting', u'instrument')]


def find_collocations(words):
    regex = re.compile('[^a-zA-Z]')
    words = [re.sub(r'[^\x00-\x7F]+',' ', w).strip() for w in words if not startswith_nonchar(w) and len(w)<20 and w.isalpha()]
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(words)
    return finder.nbest(bigram_measures.pmi, 10)

def find_most_frequent_noun_any(text, count):
    # from nltk.tag.sequential.TrigramTagger import tagger
    import pickle
    tagger_file = open('/Users/BARNES_3/nltk_data/taggers/treebank_aubt.pickle')
    tagger = pickle.load(tagger_file)
    words = text.split()
    # collocations = find_collocations(words)
    tagged_sent = tagger.tag(words)
    regex = re.compile('[^a-zA-Z]')
    tagged_ascii_words = [(re.sub(r'[^\x00-\x7F]+',' ', w[0]).strip(), w[1]) for w in tagged_sent]
    tagged_ascii_words = [(regex.sub('', w[0]).strip(), w[1]) for w in tagged_ascii_words]
    # tagged_ascii_words = sum_up_vars(tagged_ascii_words)
    tagged_filtered_words = [w for w in tagged_ascii_words if w[0]]
    #First parameter is the replacement, second parameter is your input string
# [('Michael', 'NNP'), ('Jackson', 'NNP'), ('likes', 'VBZ'), ('to', 'TO'), ('eat', 'VB'), ('at', 'IN'), ('McDonalds', 'NNP')]

    propernouns = [word for word,pos in tagged_filtered_words if (pos == 'NN' and not startswith_nonchar(word) and len(word)>1 and len(word)<20 and word.isalpha())]

    # words = word_tokenize(text)
    fdist1 = FreqDist(propernouns)
    most_common = fdist1.most_common(count)

    # print 'coming together: ', collocations
    # print most_common
    return most_common
    # filtered_words = [word for word in word_list if word not in stopwords.words('english')]

def find_most_frequent_noun(text, count):
    import pickle
    tagger_file = open('/Users/BARNES_3/nltk_data/taggers/treebank_aubt.pickle')
    tagger = pickle.load(tagger_file)

    words = text.split()
    collocations = find_collocations(words)
    tagged_sent = tagger.tag(words)
    regex = re.compile('[^a-zA-Z]')
    tagged_ascii_words = [(re.sub(r'[^\x00-\x7F]+',' ', w[0]).strip(), w[1]) for w in tagged_sent]
    tagged_ascii_words = [(regex.sub('', w[0]).strip(), w[1]) for w in tagged_ascii_words]
    # tagged_ascii_words = sum_up_vars(tagged_ascii_words)
    tagged_filtered_words = [w for w in tagged_ascii_words if w[0]]
    #First parameter is the replacement, second parameter is your input string
# [('Michael', 'NNP'), ('Jackson', 'NNP'), ('likes', 'VBZ'), ('to', 'TO'), ('eat', 'VB'), ('at', 'IN'), ('McDonalds', 'NNP')]

    propernouns = [word for word,pos in tagged_filtered_words if (pos == 'NNP' and not startswith_nonchar(word) and len(word)<20 and word.isalpha())]

    # words = word_tokenize(text)
    fdist1 = FreqDist(propernouns)
    most_common = fdist1.most_common(count)

    # print 'coming together: ', collocations
    # print most_common
    return most_common, collocations
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

def get_sentences(group, text):
    words = word_tokenize(text)
    words = [word for word in words if word.isdigit()]
    text = text.lower() 
    all_sentences_with_numbers = set()
    for line in text.split("."):
        for word in words:
            if(line.find(word)) is not -1:
                all_sentences_with_numbers.add(line)
    #print all_sentences_with_numbers
    sentences = set()
    for sentence in all_sentences_with_numbers:
        for word in bag_of_words[group]:
            sentence = sentence.lower()
            sentences.add(sentence)
            my_regex = r"\b[0-9]+\s" + word
            if re.search(my_regex, sentence, re.IGNORECASE):
                sentences.add(sentence)
    print sentences
    
def get_people_count(group, text):
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

def get_all_files_in_dir(mypath):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

fill_words()

def find_and_write_to_csv_cities():
# generate_paragraphs("example.txt")

    with open("results_place3.csv", 'a') as out_file:
        for i in [0,1,2,3,4,5]:# xrange(1, 361):
            try:
                directory = 'riots_bing/riot_%02d/' % i
                all_files = get_all_files_in_dir(directory)
                all_files = [directory + file for file in all_files]
            except Exception as e:
                print e
                continue
            bests = {}
            happening_together = {}
            for file in all_files:
                # name = file.split("/")[2]
                # name = name[:len(name)-4]
                most_common, collocations = check_for_place(file, 20)
                for c in collocations:
                    if c[0] not in happening_together:
                        happening_together[c[0]] = []
                    if c[1] not in happening_together:
                        happening_together[c[1]] = []
                    happening_together[c[0]].append(c[1])
                    happening_together[c[1]].append(c[0])
                if most_common:
                    for common_word in most_common:
                        if common_word[0] not in bests:
                            bests[common_word[0]] = 0
                        bests[common_word[0]] += common_word[1]
            m = -1
            bests_list = [(k, bests[k]) for k in bests.keys()]
            bests_list.sort(key=lambda x: x[1], reverse=True)
            ans = bests_list[0][0]
            if bests_list[0][0].lower() == 'new':
                if 'York' in bests.keys():
                    ans = 'New York'
                else:
                    ans = 'New\t%s' % str(bests_list[0:5]) 

            # if bests[0][0] in happening_together:
            #     ans = bests[0][0] + ' ' + str(happening_together[bests[0][0]])
            # for item in bests.keys():
            #     if len(item) > 1 and (m == -1 or bests[item] > bests[m]):
            #         m = item
            # res = bests_list[0:5]
            # res = [r[0] for r in res]

            out_file.write('%d\t %s \n' %(i, ans )

def find_category(most_common):
    global bag_of_words
    categories = ['election', 'jobs', 'food', 'env', 'discrimination', 'religion', 'education', 'foregin_affairs', 'domestic', 'human_rights', 'sport']
    occurance = {}
    for cat in categories:
        occurance[cat] = 0
    for word in most_common:
        for cat in categories:
            if does_match_group(cat, word):
                occurance[cat] += most_common[word]
    occ_list = [(occurance[k], k) for k in occurance if occurance[k]>0]
    print occ_list
    if not occ_list:
        return "No category"
    else:
        occ_list.sort(key=lambda x: x[0], reverse=True)
        print occ_list[0][0], occ_list[0][1]
        return occ_list[0][1]


def find_and_write_to_csv_categories():
# generate_paragraphs("example.txt")

    with open("results_categories.csv", 'a') as out_file:
        for i in [1, 2, 3, 4, 5]:#xrange(1, 361):
            try:
                directory = 'Riots/riot%d/' % i
                all_files = get_all_files_in_dir(directory)
                all_files = [directory + file for file in all_files]
            except:
                continue
            bests = {}
            # happening_together = {}
            for file in all_files:
                # name = file.split("/")[2]
                # name = name[:len(name)-4]
                with open(file, 'r') as in_file:
                    print 'processing %s' %file
                    text = in_file.read()
                    most_common = find_most_frequent_noun_any(text, 20)
                
                if most_common:
                    for common_word in most_common:
                        if common_word[0] not in bests:
                            bests[common_word[0]] = 0
                        bests[common_word[0]] += common_word[1]

            cat = find_category(bests)
            # m = -1
            # bests_list = [(k, bests[k]) for k in bests.keys()]
            # bests_list.sort(key=lambda x: x[1], reverse=True)
            # ans = bests_list[0][0]
            # if bests_list[0][0].lower() == 'new':
            #     if 'York' in bests.keys():
            #         ans = 'New York'
            #     else:
            #         ans = 'New\t%s' % str(bests_list[0:5]) 

            # if bests[0][0] in happening_together:
            #     ans = bests[0][0] + ' ' + str(happening_together[bests[0][0]])
            # for item in bests.keys():
            #     if len(item) > 1 and (m == -1 or bests[item] > bests[m]):
            #         m = item
            # res = bests_list[0:5]
            # res = [r[0] for r in res]

            out_file.write('%d\t %s \t\n' %(i, cat)) 

fill_words()
# find_and_write_to_csv_categories()
find_and_write_to_csv_cities()
# check_for_place("articles/18_May_Riot.txt")
# check_for_place("/Users/BARNES_3/Documents/niki/courses/Decision making/riot_predictor/articles/18_May_Riot.txt")
# check_for_population("example.txt")
# check_for_place("example.txt")
# generate_paragraphs()
# print does_match_group("riot", "a riot happened in 1996")


