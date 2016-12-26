#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:07:35 2016

@author: Annie Tran
"""

#Topic issues for the Bing articles of the same riots
import os
import glob
os.getcwd()
import nltk  
from nltk.book import *
from nltk import word_tokenize
from nltk.corpus import stopwords 
from urllib import urlopen
from bs4 import BeautifulSoup
import codecs

os.chdir('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/riots_bing_html/')

#rename the folders to format: riot_001
directory =os.listdir(os.getcwd())
print 'directory: ', directory
for i in range(len(directory)):
    try:
        print directory[i]
        number = int(directory[i].split('_')[1])
        print number
        new_name = 'riot_%03d' %(number)
        print 'new name', new_name
        # if filename.startswith("cheese_"):
        os.rename(directory[i],new_name)
    except:
        continue


bing_configfiles = glob.glob('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/riots_bing_html/*/*.html')

for f in range(len(bing_configfiles)):
    #Clean HTML to get text
    rawtext= open(bing_configfiles[f])
    rawtext=rawtext.read()
    soup = BeautifulSoup(rawtext) 
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    text=text.encode('utf-8')
    filename=bing_configfiles[f].split('.')[0]
    bingfile = open(filename+".txt", "w")
    for line in text.splitlines():
        bingfile.write(line)
        bingfile.write('\n')
    bingfile.close()
 
    
#store the text files    
bing_configfiles = glob.glob('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/riots_bing_html/*/*.txt')
listofriots = open('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/listofriots.txt')
listofriots=listofriots.read()
listofriots=listofriots.split('\n')

dictionary = open('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/riot_predictor/BagOfWords.txt')
dictionary=dictionary.read()
dictionary=eval(dictionary)

#store all the dictionaries of the different riot topic
unwanteditems={'country','dead','happen','people','riot','tension'}
map(dictionary.pop,unwanteditems)
    


rnum=[] #list of all the riot numbers
for l in range(len(bing_configfiles)): 
    rnum.append(bing_configfiles[l].split('/')[8])

riotnum=0
category='t'
numwordmatched=0
maxwordnum=0
for r in range(4194,4207):
    print 'new article'
    riot=int(rnum[r].split('_')[1])
    if riot!=riotnum: #if not the same riot then increment riot number
        print 'riot', riotnum, category, numwordmatched
        riotnum=riot
        maxwordnum=0
#    riot=open(configfiles[r])
#    riot=riot.read()
    riotnltk=codecs.open(bing_configfiles[r],encoding='utf-8',errors='ignore')
    riotnltk=riotnltk.read()
    riottokens=word_tokenize(riotnltk) #to count freq of words
    fdist_riot = FreqDist(w.lower() for w in riottokens)
    for key in dictionary:
        wordnum=0 #keep count of how many times a word in an 
                  #article match with the words in the dictionary of an issue
        dictlen = len(dictionary[key])
        for i in range(dictlen):
            if dictionary[key][i] in riotnltk.encode('utf-8'):
                wordnum=wordnum + fdist_riot[dictionary[key][i]]
                print dictionary[key][i],key, wordnum
                #count=count+1 #for each word in dictionary of an issue, count +1
        #if count > maxcount:
            #maxcount=count
            #k = key
        if wordnum > maxwordnum:
            maxwordnum=wordnum
            maxkey=key
    category=maxkey
    numwordmatched=maxwordnum
    print 'max', maxkey, maxwordnum
print 'riot', riot, category, numwordmatched #informtion clouded by ads
            
    #print k, maxcount
    #issuept[k]=issuept[k]+1
           