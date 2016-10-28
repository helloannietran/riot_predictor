# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc
import urllib2
import wikipedia
import re

class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text

def main():

    with open("/Users/sathani/Downloads/riot_predictor-master/test.csv","r") as f:
        lines = f.read()
        for url in lines.split():
            #text = urllib2.urlopen(url).read()
            y=url.split('/')[4]
            r1 = wikipedia.page(url.split('/')[4])
            x= r1.content            
            #plain_text = dehtml(text)
            #print url.split('/')[4]
            with open(str(url.split('/')[4])+"."+"txt", "w") as f:
                f.write(x.encode('ascii', 'ignore'))

if __name__ == '__main__':
    main()