import nltk
import os
from collections import Counter


fileDir = os.path.dirname(os.path.realpath('__file__'))
filename = fileDir + '/articles/12th_Street_Riot.txt'
print(fileDir)
print(filename)


file = open(filename, mode='r')
lines = file.read()


is_noun = lambda pos: pos[:2] == 'NN'

tokenized = nltk.word_tokenize(lines)
nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 

# print(nouns)

counts = Counter(nouns)

print(counts)