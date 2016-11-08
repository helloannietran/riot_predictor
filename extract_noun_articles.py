import nltk
import os
from collections import Counter


# fileDir = os.path.dirname(os.path.realpath('__file__'))
# # filename = fileDir + '/articles/12th_Street_Riot.txt'
# # print(fileDir)
# # print(filename)
# fileDir = fileDir + '/articles/'

fileDir = '/home/nikhil/Downloads/Riots/Riots/'

def startswith_nonchar(word):
    special_chars = ['!', '(', ')', '"', "'", '.', '}', '{', ':', ';', ',', '$', '%', '^', '&', '@', '#', '*', '\\', '/', '=', '-', '_', '<', '>', '`', 'riot', '|', '+', 'united', 'states', 'us', 'usa', 'news']
    # ret_val = False
    for c in special_chars:
        if word.lower().find(c) > -1:
            return False
    return True

def get_most_common(filename):
	file = open(filename, mode='r')
	lines = file.read()


	is_noun = lambda pos: pos[:2] == 'NN'

	tokenized = nltk.word_tokenize(lines)
	nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos) and startswith_nonchar(word)] 

	# print(nouns)

	counts = Counter(nouns)

	top_items = counts.most_common(15)

	print(top_items)


	fileobj = open('extract_noun_articles.csv', mode='a')
	fileobj.write(filename + '\n')
	for obj in top_items:
		fileobj.write(str(obj) + '\n')


# for filename in os.listdir(fileDir):
# 	print(filename)
# 	if filename.endswith(".txt"): 
# 		get_most_common(fileDir + filename)

for subdir in os.listdir(fileDir):
	# print(subdir)
	for file in os.listdir(fileDir + subdir):
		if(file.endswith(".txt")):
			print(subdir)
			print(fileDir)
			print(file)
			get_most_common(fileDir + subdir + '/' + file)

	# if filename.endswith(".txt"): 
	# 	get_most_common(fileDir + filename)