from bs4 import BeautifulSoup

import requests


r  = requests.get("https://en.wikipedia.org/wiki/List_of_riots#2014")

data = r.text

soup = BeautifulSoup(data)

for link in soup.find_all('a'):
    print(link.get('href'))