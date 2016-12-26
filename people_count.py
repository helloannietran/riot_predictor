#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 14:37:14 2016

@author: Annie Tran
"""

import pandas as pd
import os
import numpy as np
from itertools import groupby
import matplotlib.pyplot as plt
from scipy.stats import expon

os.chdir('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/riot_predictor/')

peoplecount=open('people_count_cleaned.csv')
peoplecount=peoplecount.readlines()
peoplecount.pop(0)


#create dataframe for the count of people, deaths, and injuries
df_ = pd.DataFrame(index=np.arange(354),data=None,columns=['npart','injuries','death'])
df_ = df_.fillna(0)

#remove the non riot ones first
for i in range(len(peoplecount)):
    items = peoplecount[i].split('\t')
    if items[0] in ['riot110','riot111','riot173','riot280','riot326','riot338','riot347','riot350']:
        print i

peoplecount.pop(341)


for i in range(len(peoplecount)):
    items = peoplecount[i].split('\t')
    df_['npart'][i]=items[1]
    df_['injuries'][i]=items[2]
    df_['death'][i]=items[3].split('\n')[0]

sum((df_['npart']== '-99'))
sum((df_['injuries']== '-99'))
sum((df_['death']== '-99'))

df_['npart']=df_['npart'].astype(float)
df_['injuries']=df_['injuries'].astype(float)
df_['death']=df_['death'].astype(float)

#impute the missing values
#look at npart with less than 10 participants

sumdeaths=0
count=0
for i in range(len(df_)):
    if df_['npart'][i]>100 and df_['npart'][i]<=1000:
        #print i, df_['npart'][i], df_['injuries'][i],df_['death'][i]
        if df_['death'][i] != -99:
            sumdeaths=df_['death'][i]+sumdeaths
            count=count + 1
        else:
            print i
print sumdeaths/count

df_[df_['death']==-99]

#dont need injuries
del df_['injuries']      

#[i for i in l if i < number]

#average of npart, too big here
sum(df_[df_['npart']!=-99]['npart'])/len(df_[df_['npart']!=-99]['npart'])

#try to only average the "normal" ones
matchkey = list(set(df_[df_['npart']!=-99]['npart']))
withoutmissing = list(df_[df_['npart']!=-99]['npart'])
#average participants if remove the odly large ones out is 8654 people
for i in range(len(matchkey)):
    if withoutmissing.count(matchkey[i])>1:
        print matchkey[i], withoutmissing.count(matchkey[i])


#merge the count data with the csv
data=pd.concat([data, df_], axis=1)


#impute the missing death values
xl = pd.ExcelFile('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/combineddata.xlsx')
xl.sheet_names
fulldata=xl.parse('Sheet1')

locality = fulldata['Locality']
fulldata=fulldata.drop('Locality',1)
#fulldata = fulldata.drop_duplicates()

fulldata=fulldata.reset_index(drop=True)

notmissing = fulldata['deaths'][fulldata['deaths']>=0]


np.average(notmissing[notmissing<10]) #avergae number of deaths for small values is 1 death
np.average(notmissing[notmissing>=10]) #avergae number of deaths for large values is 60 deaths


plt.hist(notmissing[notmissing>=10],bins=np.arange(notmissing[notmissing>=10].min(), notmissing[notmissing>=10].max()+1))

#print out the number that has the maximum number of occurrences (mode)
max(list(notmissing[notmissing>=10]),key=list(notmissing[notmissing>=10]).count) #10 deaths
#loc, scale = expon.fit(notmissing[notmissing>=10], floc=0)

for i in range(len(fulldata)):
    if fulldata['deaths'][i] == -88:
        fulldata['deaths'][i]= 0
    elif fulldata['deaths'][i] == -77:
        fulldata['deaths'][i]= 10

np.average(fulldata['deaths'][fulldata['deaths']<10])
np.average(fulldata['deaths'][fulldata['deaths']>=10])
max(list(fulldata['deaths'][fulldata['deaths']>=10]),key=list(fulldata['deaths'][fulldata['deaths']>=10]).count)


fulldata['locality'] = locality

###########################
#Check this protest/riot affects multiple area



writer = pd.ExcelWriter('fulldata.xlsx',engine='xlsxwriter')
fulldata.to_excel(writer,'Sheet1')
writer.save()

