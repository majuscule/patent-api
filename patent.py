#!/usr/bin/env python

import json
import urllib2
from BeautifulSoup import BeautifulSoup

import cgi
import cgitb
cgitb.enable()

import os
from urlparse import urlparse
import urllib


patents = {}
query = ''


class Parse(object):
    def __init__(self):
        query =  urllib.quote(urlparse(os.environ['REQUEST_URI']).query[2:])
        usptoURL = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=5&TERM1=' + query + '&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PTXT';
        response = urllib2.urlopen(usptoURL);
        html = response.read()
        self.soup = BeautifulSoup(html)
        table = self.soup.findAll('table')[1]
        first = True
        for tr in table.findAll('tr'):
            if first:
                first = False
                continue
            i = 0
            for td in tr.findAll('td'):
                if i == 1:
                    self.GUID = str(td.a.text)
                elif i == 3:
                    self.href = "http://patft.uspto.gov" + str(td.a['href'])
                    self.description = str(td.text.replace('\n','').replace('\t',''))
                i += 1
            patents[self.GUID] = {"href" : self.href, "description" : self.description};


if __name__ == "__main__":
    parsed = Parse()
    print "Content-Type: application/json", "\n\n", json.dumps(patents)
