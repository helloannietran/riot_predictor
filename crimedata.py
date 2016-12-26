#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 20:31:38 2016

@author: Annie Tran
"""


#Functions to get crime number and crime rates
#Write a function to get crime numbers
def crimeNum(link):
    import requests
#    globals()["requests"] = __import__("requests")
    rawtext = requests.get(link).text
    rawtext=rawtext.split(" ")
    crimecount = rawtext.index('name="description"')+1 
    crimecount = rawtext[crimecount].split('=')[1]
    try:
        crimecount=crimecount.encode('utf-8').split('"')[1]
        crimecount=float(crimecount.replace(',',''))
    except:
        crimecount = 0
    return crimecount


    
#function to get crime rate
def crimerate(link):
    import requests
    rawtext = requests.get(link).text
    rawtext=rawtext.split(" ")
    crimerate = rawtext.index('name="description"')+1 
    crimerate = rawtext[crimerate].split('=')[1]
    try:
        crimerate=crimerate.encode('utf-8').split('"')[1]
        crimerate=float(crimerate)
    except:
        crimerate=0
    return crimerate
