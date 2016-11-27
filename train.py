import pandas as pd
df = pd.read_excel("C:\Users\HariniReddy\Documents\DDDM\Structured Data\\train.xlsx")
df.head()

y = df.pop('riot')
X = df

y.head()
X.head()


from sklearn.naive_bayes import MultinomialNB
classifier = MultinomialNB()
classifier.fit(X,y)

'''print(classifier.predict([102.176604,1,1,0,3,2]))
print(classifier.predict([4.48342246,1,1,0,3,12]))
print(classifier.predict([102.176604,2,5,0,5,2]))
print(classifier.predict([102.176604,2,4,0,2,2]))
print(classifier.predict([102.176604,2,1,0,3,2]))
print(classifier.predict([102.176604,3,1,0,3,10]))
print(classifier.predict([102.176604,2,2,0,4,2]))
print(classifier.predict([80.38183417,1,1,0,2,12]))
print(classifier.predict([102.176604,2,1,0,2,10]))
print(classifier.predict([102.176604,2,2,0,3,2]))
print(classifier.predict([10,1,1,0,1,12]))
print(classifier.predict([102.176604,3,1,0,4,9]))
print(classifier.predict([10.2,2,1,5,2,6]))
print(classifier.predict([10.2,1,1,10,3,6]))
print(classifier.predict([10.2,5,1,78,4,6]))
print(classifier.predict([10.2,2,1,5,2,6]))
print(classifier.predict([10.2,5,1,4,2,6]))
print(classifier.predict([10.2,5,1,15,3,6]))
print(classifier.predict([13.36096338,2,1,1,4,1]))
print(classifier.predict([13.36096338,2,1,1,4,1]))
print(classifier.predict([13.36096338,2,1,1,4,1]))
print(classifier.predict([13.36096338,2,1,1,4,1]))
print(classifier.predict([13.36096338,2,1,0,3,6]))
print(classifier.predict([13.36096338,2,1,0,3,1]))
print(classifier.predict([13.36096338,2,1,0,4,1]))
print(classifier.predict([13.36096338,2,1,0,3,1]))
print(classifier.predict([13.36096338,2,1,0,2,1]))
print(classifier.predict([9.2,2,1,0,4,10]))
print(classifier.predict([9.2,2,7,1,5,10]))
print(classifier.predict([9.2,2,1,0,3,10]))
print(classifier.predict([9.2,7,1,5,4,9]))
print(classifier.predict([27.90491502,4,1,0,4,10]))
print(classifier.predict([9.2,2,4,0,5,10]))
print(classifier.predict([9.2,2,6,0,4,2]))
print(classifier.predict([9.2,1,1,6,3,11]))
print(classifier.predict([9.2,2,1,0,4,10]))
print(classifier.predict([9.2,2,1,0,4,10]))
print(classifier.predict([9.2,2,1,0,2,10]))
print(classifier.predict([9.2,1,1,3,1,11]))
print(classifier.predict([5.6,4,3,0,3,12]))
print(classifier.predict([9.023340183,4,1,0,5,2]))
print(classifier.predict([22.70387849,2,4,0,1,1]))
print(classifier.predict([9.023340183,4,1,0,5,12]))'''

print(classifier.predict([22.70387849,2,1,0,3,10]))
print(classifier.predict_proba([22.70387849,2,1,0,3,10]))
#print(classifier.score[X,y])
print "____________"
print(classifier.predict([9.2,2,1,0,4,10]))
print(classifier.predict_proba([9.2,2,1,0,4,10]))
print "____________"
print(classifier.predict([9.2,2,6,0,4,2]))
print(classifier.predict_proba([9.2,2,6,0,4,2]))
print "____________"

print(classifier.predict([9.2,1,1,6,3,11]))
print(classifier.predict_proba([9.2,1,1,6,3,11]))

classifier.fit(X,y)



