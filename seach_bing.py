from py_bing_search import PyBingNewsSearch
from py_bing_search import PyBingWebSearch

import urllib2, time, os, shutil, requests

api_key = 'OP14ieri+Elhn7fChsHgYTJKCnasjdy783spq7QVFlM'
# riots_file = 'africa_list_of_riots.txt'
riots_file = 'south_america_list_of_riots.txt'

def write_text():
	with open(riots_file) as listofriots:
		for i, l in enumerate(listofriots):
			if i < 0: # to pass the ones we already have
				continue
			try:
				print "looking at riot %d" %i
				name  = l.strip()
				# name  = l.split("-")[1].strip().split('(')[0].strip()
				bing_news = PyBingWebSearch(api_key, name)
				news = bing_news.search(limit=5, format='json')
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
	with open(riots_file) as listofriots:
		for i, l in enumerate(listofriots):
			if i < 0:
				continue
			try:
				print "looking at riot %d" %i
				name  = l.split("\t")[1].strip()
				idx = int(l.split("\t")[0].strip())
				# name  = l.split("-")[1].strip().split('(')[0].strip()
				bing_news = PyBingNewsSearch(api_key, name)
				news = bing_news.search(limit=5, format='json')
				time.sleep(3)
				try:
				    shutil.rmtree("riots_africa/riot_%04d" % idx)
				except OSError:
				    pass
				os.mkdir("riots_africa/riot_%04d" % idx)
				for j, new in enumerate(news):
					with open('riots_africa/riot_%04d/%d.html' %(idx, j), 'w') as riot_file:
						web = requests.get(new.url)
						riot_file.write(web.text.encode('utf-8').strip())
						# riot_file.write(new.description.encode('utf-8').strip())
			except:
				continue

write_html()