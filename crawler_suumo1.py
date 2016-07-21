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

if not os.path.exists("./suumo/"):
    os.mkdir("./suumo/")
if not os.path.exists("./suumo/"+areaname[0]):
    os.mkdir("./suumo/"+areaname[0])

area = areaname[0]


#urlからhtmlをつくる関数
def url_html(url):
    req = urllib.request.Request(url)
    #useragent = 'Mozilla/5.0'
    #req.add_header("User-agent",useragent)
    res = urllib.request.urlopen(req)
    html = res.read()#.decode()
    return html

for i in range(4):
    i+=1
    url = "http://suumo.jp/jj/bukken/ichiran/JJ010FJ001/?ar=030&bs=010&ta=13&firstFlg=0&urlFlg=0&jspIdFlg=1&kb=1&kt=9999999&km=1&mb=0&mt=9999999&ekTjCd=&ekTjNm=&tj=0&pn="+str(i)
    html = url_html(url).decode('utf-8')

    filename = "./suumo/"+area+"/"+str(i)+".html"
    f = open(filename,'w')
    f.write(html)
    f.close()

    f2 = open("nowcrawling_suumo.txt",'w') #処理済みの番号を保存
    print(i,file=f2)
    f2.close()

"""
#htmlからlinksをつくる関数
def html_links(html):
    soup = BeautifulSoup(html)
    links = soup.find_all("a")
    hrefs = ""
    for link in links:
        if 'href' in link.attrs:
            #print(link.text, ':', link.attrs['href'])
            hrefs += link.attrs['href'] + ','
            #hrefs.append([link.text, link.attrs['href']])
    return hrefs
"""
