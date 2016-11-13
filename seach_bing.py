from py_bing_search import PyBingNewsSearch
from py_bing_search import PyBingWebSearch

import urllib2, time, os, shutil

api_key = 'OP14ieri+Elhn7fChsHgYTJKCnasjdy783spq7QVFlM'

with open("listofriots.txt") as listofriots:
	for i, l in enumerate(listofriots):
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
