# -*- coding: utf-8 -*-

import os
from parse_file import *
from fetch_articles import dehtml
import sys
import csv 

super_dir = 'D:/riot_predictor'
os.chdir(super_dir)

root_dir = 'D:/riot_predictor/Riots'
os.chdir(root_dir)
list_folders = os.listdir(root_dir)

for i in range(32, 361):
    folder = 'riot'+ str(i)
    print folder
    dir = root_dir + '/' + folder
    os.chdir(dir)
    list_files = os.listdir(dir)
    #print list_files
    people = []
    dead = []
    injured = []
    for file in list_files:
        f = open(file, 'r')
        text=f.read()
        plain_text = dehtml(text)
        plain_text = unicode(plain_text, 'utf-8')
        #print plain_text
    
        if does_match_group("people", plain_text) and has_number(plain_text):
            #get_sentences("people", text)
            people.append(get_people_count("people", plain_text))
            injured.append(get_people_injured_count("injured", plain_text))
            dead.append(get_people_dead_count("dead", plain_text)) 
        f.close()
    if len(people) > 0: 
        people_count = str(max(people))
    else:
        people_count = 0
    if len(injured) > 0:
        injured_count = str(max(injured))
    else:
        injured_count = 0
    if len(dead) > 0:
        dead_count = str(max(dead))
    else:
        dead_count = 0
    fields=[folder, people_count, injured_count, dead_count]
    os.chdir(super_dir)
    fd = open('records.csv','a')
    fd.write(str(fields)) 
    print people_count
    print injured_count
    print dead_count
    print '---------------------' 
    fd.close()