# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 19:57:02 2016

@author: Annie Tran
"""


import urllib
import numpy as np
import pandas as pd
import pylab as pl 
import os
from urlparse import urlparse
from bs4 import BeautifulSoup
from urllib import FancyURLopener
import re
import codecs

#Method: list of riots and peaceful protests are given
#do a duckduckgo search on each item
#pull the links to all these articles
#get content of each of these links
#save content as individual text files
#categorize these text files


##############################################Run this part first
class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)Gecko/20071127 Firefox/2.0.0.11'

myopener = MyOpener()

listofriots=codecs.open('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/searchkeys.txt').read()


listofriots=listofriots.splitlines()
listofriots = listofriots[4001:]
#using regex to remove stuff in brackets (messes with search result)
#for row in range(len(listofriots)):
##    listofriots[row]=re.sub("[\(\[].*?[\)\]]",'', listofriots[row])
#     listofriots[row]=re.sub("[\[].*?[\]*]",'', listofriots[row])
#     listofriots[row]=listofriots[row].decode('utf-8').strip()
#     listofriots[row]=re.sub(u'\u2013','', listofriots[row]) #gets rid of the dash
#     

##############################################End

#This function pulls contents from the list of links
def getarticles(ls,m):
    ls=ls[2:7] #remove the stuff that are not links only pull the top 5 links
    numlinks=len(ls)
    n=0
    for l in range(numlinks):
        try:
            content = myopener.open(ls[l][0]).read()
        except:
            print ls[l][0]
            continue
        parsed=BeautifulSoup(content)
        article = parsed.get_text().replace('\n','\n\n')
        mypath= '/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/structured_riots_data/riot{0}'.format(m-1)
        if not os.path.isdir(mypath):
            os.makedirs(mypath)
        file= open(mypath+'/riot{0}-{1}.txt'.format(m-1,n),'w')
        article=article.encode('utf8')
        article = article.splitlines()
        for line in article:
            file.write(line)
        n=n+1
        file.close()


#This function pulls the links from duckduckgo
#by putting each line in listofriots into search bar

def searchengine(searchphrase,m):
    encoded=searchphrase.encode('utf-8')
    data=urllib.urlopen('http://duckduckgo.com/html/?q='+encoded).read()
    soup=BeautifulSoup(data)
    n=len(soup.find_all('a'))
    links = np.empty([n, 1],dtype='S150')
    allhtml=soup.find_all('a')
    for i in range(len(allhtml)):
         try:
             links[i,0]=allhtml[i].get('href') #goes through html and finds all the links
         except UnicodeEncodeError:
             links[i,0]=allhtml[i].get('href').encode('utf-8')
    #remove duplicate links
    uniquelinks=[]
    print (len(uniquelinks))
    for item in links:
        if item not in uniquelinks:
            uniquelinks.append(item)
    getarticles(uniquelinks,m)

#loops through the list of riots and make a search for each
m=0 
for r in range(len(listofriots)):
    phrase=listofriots[r]
    searchengine(phrase,m)
    m=m+1
    

    
    
    
    #######################Ignore this part
#google pulls out of order links, not gonna work
#def searchengine(searchphrase):
#    encoded=searchphrase.encode('utf8')
#    rawData=urllib.urlopen('https://www.googleapis.com/customsearch/v1?key=AIzaSyCy0yWoW6zu3Xw8zVd4NGmttmL6JXCBTog&cx=017576662512468239146:omuauf_lfve&q='+encoded).read()    
#    jsonData = json.loads(rawData) #convert to dictionary
#    searchResults = jsonData['items']
#    links = np.empty([4, 1], dtype="S25")
#    i = 0
#    for er in searchResults:
#         link = er['displayLink']
#         link1 = urlparse(link).netloc
#         links[i,0]=link1
#         i = i + 1
#    target = "No Match found" 
#    if links[0,0] == links[1,0] or links[0,0] == links[2,0] or links[0,0] == links[3,0]:
#        target = links[0,0] 
#    if links[1,0] == links[2,0] or links[1,0] == links[3,0]:
#        target = links[1,0] 
#    if links[2,0] == links[3,0] :
#        target = links[2,0] 
#    return [target]
#######################  