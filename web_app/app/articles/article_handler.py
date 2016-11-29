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
from os.path import isfile, join
from app.utils import violence_rating

def get_all_files_in_dir(mypath):
    onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles


class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)Gecko/20071127 Firefox/2.0.0.11'


def getarticles(ls,m):
    ls=ls[2:7] #remove the stuff that are not links and only pull the top 5 links
    numlinks=len(ls)
    myopener = MyOpener()
    n=0
    for l in range(numlinks):
        try:
            content = myopener.open(ls[l][0]).read()
        except Exception as e:
            print e
            print ls[l][0]
            continue
        parsed=BeautifulSoup(content)
        article = parsed.get_text().replace('\n','\n\n')
        mypath= '/Users/BARNES_3/Documents/niki/courses/Decision making/riot_predictor/web_app/app/downloaded_articles/{0}'.format(m)
        if not os.path.isdir(mypath):
            os.makedirs(mypath)
        file= open(mypath+'/riot{0}-{1}.txt'.format(m,n),'w')
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
    while True:
        try:
            data=urllib.urlopen('http://duckduckgo.com/html/?q='+encoded).read()
            break
        except:
            continue
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

def has_word(content, words):
    for word in words:
        if content.find(word) < 0:
            return False
    return True

def save_articles(keyword):
    m = keyword
    mypath= '/Users/BARNES_3/Documents/niki/courses/Decision making/riot_predictor/web_app/app/downloaded_articles/{0}'.format(m)
    if not os.path.isdir(mypath):
        searchengine(keyword,m)
        # return
    all_files = get_all_files_in_dir(mypath)
    all_content = []
    for f in all_files:
        full_path = join(mypath, f)
        with open(full_path, 'r') as res_articles:
            content = res_articles.read()
            words = keyword.split(' ')
            if not has_word(content, words):
                os.remove(full_path)
            else:
                all_content.append(content)
    return all_content


save_articles("obama")
