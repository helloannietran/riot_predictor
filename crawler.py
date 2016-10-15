from bs4 import BeautifulSoup

import requests
# import pandas as pd 
import numpy as np

# df = pd.DataFrame()

np_arr = np.empty(1,)

r  = requests.get("https://en.wikipedia.org/wiki/List_of_riots#2014")

data = r.text

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

soup = BeautifulSoup(data)

# print(soup.head())


for li in soup.find_all('li'):
	if(RepresentsInt(li.get_text()[0:4])):
		if(li.get_text()[0:4]>=2006):
			for link in li.find_all('a'):
				if(link.get_text()[0:1]!='['):
					if(link.get('href')[0:5]=='/wiki'):
						link_str = "https://en.wikipedia.org" + link.get('href')
					else:
						link_str = link.get('href')
					# print(link_str)
					np_arr = np.append(np_arr,link_str)

print(np_arr.shape)
np_arr=np_arr[1:]
print(np_arr)
# with open('test.txt','wb') as f:
# # np.savetxt(f,x,fmt='%.5f')
# 	np.savetxt(f, np_arr, delimiter=',')

fileobj = open('test.csv', mode='wb')
for obj in np_arr:
	fileobj.write(obj + '\n')
# np_arr.tofile(fileobj, sep="\n" , format="%s")