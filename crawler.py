from bs4 import BeautifulSoup

import requests


r  = requests.get("https://en.wikipedia.org/wiki/List_of_riots#2014")

data = r.text

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

soup = BeautifulSoup(data)

print(soup.head())


for li in soup.find_all('li'):
	if(RepresentsInt(li.get_text()[0:4])):
		for link in li.find_all('a'):
			if(link.get_text()[0:1]!='['):
				print(link.get('href'))