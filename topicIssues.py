#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 12:02:49 2016

@author: Annie Tran
"""

import glob
import nltk
from nltk.book import *
from nltk import word_tokenize
import codecs
import os
import re
from nltk.corpus import stopwords
os.chdir('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/structured_riots_data/')


#rename files so they all have 3 digits
for num in xrange(345, 354):
    for i in xrange(345, 354):
        try:
            directory = 'riot_%03d/' % i #Ex. riot001/
            print 'directory: ', directory
            for filename in os.listdir(directory): #loop through all the text files in the riot folders
                try:
                    print filename #ex. riot001_01.txt
                    number = int(filename.split('_')[1].split('.')[0])
                    new_name = '%02d.txt' %(number)
                    print 'new name', new_name
                    # if filename.startswith("cheese_"):
                    os.rename(directory+filename,directory+ new_name)
                except:
                    continue
        except Exception as e:
            print e
            continue

#rename the folders
directory =os.listdir(os.getcwd())
directory=directory[1:]
print 'directory: ', directory
for i in range(len(directory)):
    try:
        print directory[i]
        number = int(directory[i].split('t')[1])
        print number
        new_name = 'riot%04d' %(number)
        print 'new name', new_name
        # if filename.startswith("cheese_"):
        os.rename(directory[i],new_name)
    except:
        continue



#Figure out how to store multiple articles
#for each riot, remove articles that are not relevant to the riot topic
#do matching with dictionary and assign appropriate label


listofriots = open('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/listofriots.txt')
listofriots=listofriots.readlines()
listofriots=map(lambda x: x.replace('"',''),listofriots)
#dictionary=map(lambda x: x != '\r',dictionary[x])

#list of all the directories of text files
configfiles = glob.glob('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/structured_riots_data/*/*.txt')


#Store all the irrelevant articles 
uselessarticles=[]
t=0
regex = listofriots_ori[t]
regex=regex.split()
for k in range(0,len(configfiles)):
    rawtext= open(configfiles[k])
    rawtext=rawtext.read()
    rawtext=rawtext.split()
    #check if it's a different riot
    riotnum = int(configfiles[k].split('/')[8].split('t')[1]) #pulls the riot number
    if riotnum != t: #if riot number is not the same, increase t 
        t=riotnum
        regex = listofriots[t]
        regex=regex.split()
    reglen=len(regex)
    countset = 0
    for i in range(reglen):
        if regex[i] not in stopwords.words('english'):
            if regex[i] in rawtext:
                print regex[i]
                count = rawtext.count(regex[i])
                countset = count + countset
    print riotnum, countset
    if reglen <=6:
        if countset < 2:
            print configfiles[k]
            uselessarticles.append([configfiles[k]])
    elif countset < 4:
        print configfiles[k]
        uselessarticles.append([configfiles[k]])
        
        
#move all the irrelevant articles to diff folder
for f in range(len(uselessarticles)):
    filename = uselessarticles[f][0].split('/')[9]
    os.rename(uselessarticles[f][0], '/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/irrelevant/'+filename)
    
    
for i in range(len(directory)):
    text_file = open(directory[i]+"/06.txt", "w")
    text_file.write(listofriots[i])
    text_file.close()



#Leftover files
configfiles = glob.glob('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/Riots/*/*.txt')    


#Remove the list of riots wikipedia pages
for k in range(len(configfiles)):
    rawtext= open(configfiles[k])
    rawtext=rawtext.read()
    string = 'List of riots - Wikipedia, the free encyclopedia'
    string2='Listing of US Civil Unrest Incidents'
    string3='List of riots'
    string4='Civil Unrest & Rioting WorldWide'
#    if string in rawtext:
#        os.remove(configfiles[k])
#    elif string2 in rawtext:
#        os.remove(configfiles[k])
#    elif string3 in rawtext:
#        os.remove(configfiles[k])
    if string4 in rawtext:
        os.remove(configfiles[k])


#Leftover files
configfiles = glob.glob('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/Riots/*/*.txt')

#Try to figure out the riot topic based on dictionary
dictionary = open('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/riot_predictor/BagOfWords.txt')
dictionary=dictionary.read()
dictionary=eval(dictionary)


#store all the dictionaries of the different riot topic
unwanteditems={'country','dead','happen','people','riot','tension'}
map(dictionary.pop,unwanteditems)
    
#Try classifying the first riot...Please work ;~;
#test on riot number 15, correct topic should be religion (297 to 325)
riot=open(configfiles[300])
riot=riot.read()

#issuept = {'domestic':0, 'education':0, 'election':0,'env':0,'food':0,
#               'foreign_affairs':0,'human_rights':0,'jobs':0,'religion':0,'sport':0}

rnum=[] #list of all the riot numbers
for l in range(len(configfiles)): 
    rnum.append(configfiles[l].split('/')[8])

riotnum=335
category='t'
numwordmatched=0
maxwordnum=0
for r in range(5244,len(configfiles)):       
    if int(rnum[r].split('t')[1])!=riotnum:
        print 'riot',riotnum, category, numwordmatched
        riotnum=riotnum+1
        maxwordnum=0
#    riot=open(configfiles[r])
#    riot=riot.read()
    riotnltk=codecs.open(configfiles[r],encoding='utf-8',errors='ignore')
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
                #print key, wordnum
                #count=count+1 #for each word in dictionary of an issue, count +1
        #if count > maxcount:
            #maxcount=count
            #k = key
        if wordnum > maxwordnum:
            maxwordnum=wordnum
            maxkey=key
    category=maxkey
    numwordmatched=maxwordnum
print 'riot',riotnum, category, numwordmatched
            
    #print k, maxcount
    #issuept[k]=issuept[k]+1
           
