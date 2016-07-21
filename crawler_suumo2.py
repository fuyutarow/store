#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import glob
import urllib.request
import codecs
import csv
from bs4 import BeautifulSoup
import re

areaname = ["tokyo","kanagawa","saitama","chiba","ibaraki","tochigi","gunma"]

area = areaname[0]
if not os.path.exists("./suumo/"+area+"pages/"):
        os.mkdir("./suumo/"+area+"pages/")

filename = ".suumo/"+area+"pages/cassetlist"
f = open("./suumo/"+area+"pages/cassetlist",'w')
f.write("")
f.close()

def url_html(url):
    req = urllib.request.Request(url)
    #useragent = 'Mozilla/5.0'
    #req.add_header("User-agent",useragent)
    res = urllib.request.urlopen(req)
    html = res.read()#.decode()
    return html


for f in glob.glob("./suumo/"+area+"/*.html"):
    soup1 = BeautifulSoup(codecs.open(f,encoding='utf-8').read(), "html.parser")

    for cassetlist in soup1.find_all('div', attrs={'class':"property_unit-header"}):
        link = cassetlist.find('a',attrs={'class':"js-cassetLinkHref"})
        if 'href' in link.attrs:
            href = "http://suumo.jp"+link.attrs['href']

        infohtml = url_html(href).decode('utf-8')
        soup2 = BeautifulSoup(infohtml,"html.parser")
        infourl = soup2.find('a',href=re.compile("bukkengaiyo"))
        url = "http://suumo.jp"+infourl.attrs['href']
        html = url_html(url).decode('utf-8')

        start = url.find("nc_")#[:11]
        filename = url[start:start+11]

        f = open("./suumo/"+area+"pages/"+filename+".html",'w')
        f.write(html)
        f.close()
