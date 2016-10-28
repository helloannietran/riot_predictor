# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 12:38:18 2016

@author: Rohit Mandge
"""

import nltk, re, pprint
from nltk import word_tokenize
from nltk.tokenize.api import TokenizerI
from parse_file import *

text="OAKLAND About 50 people gathered outside the Alameda County Superior Courthouse on Tuesday night in a vigil for Oscar Grant III, commemorating what will be the first day of his killer's trial and there were 89 protestors"

if does_match_group("people", text) and has_number(text):
    get_number("people", text)
    #print text