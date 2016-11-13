from py_bing_search import PyBingNewsSearch
from py_bing_search import PyBingWebSearch

import urllib2, time, os, shutil, requests

api_key = 'OP14ieri+Elhn7fChsHgYTJKCnasjdy783spq7QVFlM'

def write_text():
	with open("listofriots.txt") as listofriots:
		for i, l in enumerate(listofriots):
			if i < 171: # to pass the ones we already have
				continue
			try:
				print "looking at riot %d" %i
				name  = l.split("-")[1].strip().split('(')[0].strip()
				bing_news = PyBingWebSearch(api_key, name)
				news = bing_news.search(limit=30, format='json')
				time.sleep(3)
				try:
				    shutil.rmtree("riots_bing/riot_%02d" % i)
				except OSError:
				    pass
				os.mkdir("riots_bing/riot_%02d" % i)
				for j, new in enumerate(news):
					with open('riots_bing/riot_%02d/%02d.txt' %(i, j), 'w') as riot_file:
						riot_file.write(new.title.encode('utf-8').strip() + '\n')
						riot_file.write(new.description.encode('utf-8').strip())
			except:
				continue

def write_html():
	with open("listofriots.txt") as listofriots:
		for i, l in enumerate(listofriots):
			if i < 0:
				continue
			try:
				print "looking at riot %d" %i
				name  = l.split("-")[1].strip().split('(')[0].strip()
				bing_news = PyBingNewsSearch(api_key, name)
				news = bing_news.search(limit=30, format='json')
				time.sleep(3)
				try:
				    shutil.rmtree("riots_bing_html/riot_%02d" % i)
				except OSError:
				    pass
				os.mkdir("riots_bing_html/riot_%02d" % i)
				for j, new in enumerate(news):
					with open('riots_bing_html/riot_%02d/%02d.html' %(i, j), 'w') as riot_file:
						web = requests.get(new.url)
						riot_file.write(web.text.encode('utf-8').strip())
						# riot_file.write(new.description.encode('utf-8').strip())
			except:
				continue

write_text()