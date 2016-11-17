import  re
from nltk.tag import pos_tag

def find_nouns(text):

    words = text.split()
    # tagged_sent = tagger.tag(words)
    tagged_sent = pos_tag(words)
    # print tagged_sent
    text = re.sub('[^0-9a-zA-Z]+', '', text)
    propernouns = [re.sub('[^0-9a-zA-Z]+', '', word) for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' and len(word)>1 and len(word)<20)]
    return propernouns

kwrd_dict = {}
with open("new_list_of_riots.csv", 'r') as riots_file:
    for i, line in enumerate(riots_file):
        print 'looking at riot %d' % i
        line_list = line.split("\t")
        # print 'line: %s' % (str(line_list))
        kwrd_dict[i] = []
        # kwrd_dict[i].append(line_list[0].strip())
        # kwrd_dict[i].append(line_list[1])
        if line_list[1].strip():
            subj = line_list[1].strip()
            # print 'inja', subj
            nouns = find_nouns(subj)
            # print nouns
            kwrd_dict[i] += nouns
        if line_list[2].strip():
            kwrd_dict[i].append(line_list[2].strip())
        # kwrd_dict[i].append(line_list[3].strip())

with open('keywords.txt', 'w') as keywords_file:
    keywords_file.write(str(kwrd_dict))
        
        # collocations = find_collocations(words)
        # regex = re.compile('[^a-zA-Z]')
        # tagged_ascii_words = [(re.sub(r'[^\x00-\x7F]+',' ', w[0]).strip(), w[1]) for w in tagged_sent]
        # tagged_ascii_words = [(regex.sub('', w[0]).strip(), w[1]) for w in tagged_ascii_words]
        # # tagged_ascii_words = sum_up_vars(tagged_ascii_words)
        # tagged_filtered_words = [w for w in tagged_ascii_words if w[0]]
        #First parameter is the replacement, second parameter is your input string
    # [('Michael', 'NNP'), ('Jackson', 'NNP'), ('likes', 'VBZ'), ('to', 'TO'), ('eat', 'VB'), ('at', 'IN'), ('McDonalds', 'NNP')]

