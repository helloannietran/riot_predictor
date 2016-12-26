#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 18:47:37 2016

@author:Annie Tran
"""

import pandas as pd
import os
import numpy as np

os.chdir('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/')

data = pd.read_csv('articlesdata_structured.csv')

listofriots = open('listofriot_from2006.txt')
listofriots=listofriots.readlines()
listofriots_ori = open('listofriots.txt')
listofriots_ori=listofriots_ori.readlines()

riotissues = open('riotissues.txt')
riotissues = riotissues.readlines()


removed = list(filter(lambda x: 'citation' in x, listofriots) #store the ones with "citation needed"

#outputs index where 'citation needed' shows up in

for i,j in enumerate(listofriots):
    if 'citation' in j:
        print i, j
    
#remove date columns
data=data.drop(data.columns[[0, 1,2,3,4,5]], axis=1)

#add relevant columns
data['npart'] = np.nan
data['crime rate'] = np.nan
data['target'] = np.nan
data['issue'] = np.nan
data['violence rating'] =  np.nan
data['riot'] = 1
data['population'] = np.nan

#remove repetivive riots
#38 to 53 for food riots
data=data.drop(data.index[38:54])
data = data.reset_index(drop=True)
data=data.set_value(37, 'population', 3) #set that riot to pupylation size of type 3 (affecting multiple areas)
#data.iloc[37]['population']=3

#50 to 54 for Israel_Gaza conflict
data=data.drop(data.index[50:55])
data = data.reset_index(drop=True)
data=data.set_value(49, 'population', 3) 

data=data.drop(data.index[[35]])
data = data.reset_index(drop=True)
data=data.set_value(147, 'population', 3) 

databreak=data.iloc[0:16]
databreak2=data.iloc[16:]

newrow = ['2006 – 2006 protests in Hungary',np.nan,np.nan,'Hungary',np.nan,np.nan,np.nan,np.nan,np.nan,1,np.nan]
cols = data.columns.tolist()
df2 = pd.DataFrame([newrow], columns=cols)
databreak=databreak.append(df2)
databreak = databreak.reset_index(drop=True)

data=databreak.append(databreak2)
data = data.reset_index(drop=True)

#310 in data should not be number for subject
#Riots that were not on list of riots: 
    #[272 in data] Riots. After the death of Kimani Gray who was shot and killed by NYPD
    #[283 in data] Riots. 1 dead and 250 injured. Cordoba, Argentina
    #[284 in data]. Riots. 1 dead and 57 injured. Concordia, Argentina
    #[291 - 298 in data]
    #[303 in data]
    
data=data.drop(data.index[[272,283,284,291,292,293,294,295,296,297,298,303]])
data = data.reset_index(drop=True)

#put in all the riots before 2006 into the dataframe--------
newrow = ['Seattle Mardi Gras riot',np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,1,np.nan]
df2 = pd.DataFrame([newrow], columns=cols)
for i in range(1,51):
    subject = listofriots_ori[i]
    newrow = [subject,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,1,np.nan]
    df3 = pd.DataFrame([newrow], columns=cols)
    df2=df2.append(df3)

df2= df2.reset_index(drop=True)

data=df2.append(data)
data = data.reset_index(drop=True)
#-----------------------------------------------------------

data['subj']=data['subj'].astype(str)

data.to_csv('structured_articles.csv', sep=',',index_col = False)

#fill in the issues column
riotissues=map(lambda x: x.split(' ')[2], riotissues)
data['issue']=riotissues

















