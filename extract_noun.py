import nltk
import os
from collections import Counter


fileDir = os.path.dirname(os.path.realpath('__file__'))
# filename = fileDir + '/articles/12th_Street_Riot.txt'
# print(fileDir)
# print(filename)
fileDir = fileDir + '/articles/'


def get_most_common(filename):
	file = open(filename, mode='r')
	lines = file.read()


	is_noun = lambda pos: pos[:2] == 'NN'

	tokenized = nltk.word_tokenize(lines)
	nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 

	# print(nouns)

	counts = Counter(nouns)

	top_items = counts.most_common(15)

	print(top_items)


	fileobj = open('extract_noun.csv', mode='a')
	fileobj.write(filename + '\n')
	for obj in top_items:
		fileobj.write(str(obj) + '\n')


for filename in os.listdir(fileDir):
	print(filename)
	if filename.endswith(".txt"): 
		get_most_common(fileDir + filename)