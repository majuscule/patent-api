#!/usr/bin/env python2

import json
import urllib2
from BeautifulSoup import BeautifulSoup

patents = {}


class Parse(object):
    def __init__(self):
        response = urllib2.urlopen('http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=5&TERM1=duck&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PTXT');
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
                    self.href = str(td.a['href'])
                    self.description = str(td.text.replace('\n','').replace('\t',''))
                i += 1
            patents[self.GUID] = {"href" : self.href, "description" : self.description};


if __name__ == "__main__":
    parsed = Parse()
    print json.dumps(patents)


