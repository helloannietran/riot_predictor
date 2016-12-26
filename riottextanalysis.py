# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 10:38:59 2016

@author: Annie Tran
"""

#practice with NLTK
import nltk
import pandas as pd
#nltk.download() #download book to practice with

from nltk.book import *
from __future__ import division #need this to do division
from __future__ import print_function #so print function will work

import nltk, re, pprint
from nltk import word_tokenize
from nltk.corpus import stopwords #stopwords are words like 'the', 'a', 'an'
from nltk.tag import pos_tag
import string
import unicodedata
import codecs

text1.concordance("monstrous") #returns all the sentences with the word monstrous in it
text2.concordance("affection")
text3.concordance("lived")
text5.concordance("lol")

text2.similar("monstrous") #find words that are in the same context as monstrous
text1.similar("monstrous")

text2.common_contexts(["monstrous","very"])

text2.similar("heavy")
text1.similar("heavy")

text2.common_contexts(["heavy","deep"])
text1.common_contexts(["heavy","curious"])
text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"])

len(text3) #44764 words or tokens
sorted(set(text3)) #distinct words in a text in order
len(set(text3)) #num of distinct words and punctuation symbols
len(set(text3)) / len(text3) #each word is used 16 times on average

text3.count("smote")
100*text4.count('a') / len(text4)

text5.count("lol")/len(text5)
len(sent2)

#indexing:
text4[200]
text4.index("aware")
sent = ['word1', 'word2', 'word3', 'word4', 'word5', 'word6', 'word7', 'word8', 'word9', 'word10']
sent[5:8]
sent[1:9] = ['second','third']
sent[-2]
sent[-2:]

fdist1 = FreqDist(text1) #frequency of words in the Moby Dick text
fdist1.most_common(50) #50 most common words
fdist1['whale']
fdist1.plot(50,cumulative=True) #these 50 words make up for almost half of the text

fdist1.hapaxes() #infrequent words

#Take a look at long words
V = set(text1) #all the distinct words
long_words = [w for w in V if len(w) > 15] #store words in V with length more than 15 into long_words
sorted(long_words)

#words that are long but also happen frequently
sorted(w for w in V if len(w) > 4 and fdist1[w]>50)

text4.collocations() # return pairs of words that appear quite often

#count the len of each word
[len(w) for w in text1]
fdist=FreqDist(len(w) for w in text1) #how many words have length 2, 3, ...?
fdist.most_common()
fdist.max() #most frequent word length is 3
fdist[3]
fdist.freq(3)

sorted(w for w in set(text1) if w.isdigit() and len(w)==4)
sorted(w for w in set(text7) if '-' in w and 'index' in w)
sorted(wd for wd in set(text3) if wd.istitle() and len(wd) > 10)
sorted(w for w in set(sent7) if not w.islower())
sorted(t for t in set(text2) if 'cie' in t or 'cei' in t)

len(set(word.lower() for word in text1)) #prevent double counting words like The and the
len(set(word.lower() for word in text1 if word.isalpha())) #get rid of punctuation and non-alphabetic items

tricky = sorted(w for w in set(text2) if 'cie' in w or 'cei' in w)
for word in tricky:
    print(word, end=' ')

#more text corpora
nltk.corpus.gutenberg.fileids()
emma = nltk.corpus.gutenberg.words('austen-emma.txt')
len(emma)
set(emma)
emma = nltk.Text(nltk.corpus.gutenberg.words('austen-emma.txt')) #have to do this to use functions like concordance
emma.concordance("surprise")

#a faster way to import the text files from gutenberg:
from nltk.corpus import gutenberg
gutenberg.fileids()
emma = gutenberg.words('austen-emma.txt')

for fileid in gutenberg.fileids():
    num_chars=len(gutenberg.raw(fileid))
    num_words=len(gutenberg.words(fileid))
    num_sents=len(gutenberg.sents(fileid))
    num_vocab=len(set(w.lower() for w in gutenberg.words(fileid)))
    print(round(num_chars/num_words), round(num_words/num_sents), round(num_words/num_vocab), fileid)
    
    
macbeth_sents=gutenberg.sents("shakespeare-macbeth.txt")    
macbeth_sents[180]
    
longest_len=max(len(s) for s in macbeth_sents)

[s for s in macbeth_sents if len(s)==longest_len]

from nltk.corpus import brown
news_text = brown.words(categories='news')
fdist = nltk.FreqDist(w.lower() for w in news_text)

#try some stuff on the riot articles
f=open('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/Oakland2010/grant3.txt')
raw=f.read()
tokens=word_tokenize(raw)
tokens = nltk.Text(tokens) #so I can use function like concordance in nltk
sorted(w for w in set(tokens) if w.isdigit())

words = [w.lower() for w in tokens]

#only show distribution of words that are not stopwords
fdist_riot = FreqDist(w.lower() for w in tokens if w not in stopwords.words('english') and len(w) > 1)
fdist_riot.most_common(10)
fdist_riot.plot(10,cumulative=True)

tokens.collocations()
tokens.similar('police')

for w in set(tokens):
    if w.isdigit() and len(w)==4:
        print(tokens.concordance(w))
        
vocab = sorted(set(words))

#forming dictionaries for issue column using articles
rfile=open('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/Economy/jobsprot_azerbaijan.txt')

rawtext=rfile.read()
rawtext=rawtext.encode('utf-8')
tokens=word_tokenize(rawtext)
tokens=nltk.Text(tokens)
#tokens=nltk.Text(nltk.corpus.gutenberg.words(rfile))

fdist = FreqDist(w.lower() for w in tokens if w not in stopwords.words('english') and len(w)>1 and w.isalpha())
list=fdist.most_common(40)

tokens.similar('price')
tokens.concordance('price')
tokens.collocations()


rfile.close()


#2nd article
rfile2=open('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/Economy/jobsprot_india.txt')
rawtext2=rfile2.read()

#rawtext2=rawtext2.encode('utf-8')
tokens2=word_tokenize(rawtext2)
tokens2=nltk.Text(tokens2)

fdist2 = FreqDist(w.lower() for w in tokens2 if w not in stopwords.words('english') and len(w)>2 and w.isalpha())

rfile2.close()

#3rd article
rfile3=open('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/Economy/jobsprot_China.txt')
rawtext3=rfile3.read()

#rawtext2=rawtext2.encode('utf-8')
tokens3=word_tokenize(rawtext3)
tokens3=nltk.Text(tokens3)
for w in tokens3:
    if w not in stopwords.words('english') and not w.isalpha():
        tokens3.remove(w)
        
tokens3=nltk.Text(tokens3)       
tokens3.collocations()
tokens3.concordance('factory')

fdist3 = FreqDist(w.lower() for w in tokens3 if w not in stopwords.words('english') and len(w)>2 and w.isalpha())
fdist3.most_common(40)
fdist3

rfile3.close()

 #4th article
rfile4=codecs.open('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/Economy/jobsprot_China2.txt',encoding='utf-8',errors='ignore')
rawtext4=rfile4.read()
tokens4=word_tokenize(rawtext4)
tokens4=nltk.Text(tokens4)      
fdist4 = FreqDist(w.lower() for w in tokens4 if w not in stopwords.words('english') and len(w)>2 and w.isalpha())

rfile4.close()

