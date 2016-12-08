#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 00:11:43 2016

@author: Annie Tran
"""

#random forest 
from sklearn.ensemble import RandomForestClassifier
from numpy import genfromtxt, savetxt
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

xl = pd.ExcelFile('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/riot_predictor/completedata.xlsx')
xl.sheet_names
fulldata=xl.parse('Sheet1')
fulldata = pd.DataFrame(fulldata)

fulldata = fulldata.reset_index(drop=True)
fulldata = fulldata.drop('locality',1)
fulldata = fulldata.drop('country',1)
fulldata = fulldata.drop('Duration',1)

#fulldata['violentce rating']=map(lambda x: 2 if x < 0 else 1, fulldata['violentce rating'])

fulldata['target'] = pd.Categorical(fulldata['target'])
fulldata['npart'] = pd.Categorical(fulldata['npart'])
fulldata['issue'] = pd.Categorical(fulldata['issue'])
fulldata['riot'] = pd.Categorical(fulldata['riot'])
fulldata['crime rate'] = pd.to_numeric(fulldata['crime rate'])
fulldata['deaths'] = pd.to_numeric(fulldata['deaths'])
fulldata['violentce rating'] = pd.to_numeric(fulldata['violentce rating'])
#fulldata['violentce rating'] = pd.Categorical(fulldata['violentce rating'])

#randomize the rows, frac tells it to return all rows
fulldata = fulldata.sample(frac=1).reset_index(drop=True)

train = fulldata.iloc[0:4303]
test = fulldata.iloc[4304:]

#fit random forest
rf = RandomForestClassifier(n_estimators=100)
rf_fit = rf.fit(train.iloc[0::,0:6],train.iloc[0::,6])

#test on test data
output = rf.predict(test.iloc[0::,0:6])
outputprob = rf.predict_proba(test.iloc[0::,0:6])

df_confusion = pd.crosstab(test.iloc[0::,6], output)
df_confusion / df_confusion.sum(axis=1)
accuracy_score(test.iloc[0::,6], output)


testvalues=[[16.2, 2, 0, 1, -2.94544,10]] #remeber to do double brackets

rf.predict(testvalues)
rf.predict_proba(testvalues)



#save model
import pickle
f = open('rfmodel.pickle','wb')
pickle.dump(rf_fit, f)
f.close()



