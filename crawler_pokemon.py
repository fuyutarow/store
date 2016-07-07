#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import glob
import urllib.request
import codecs
import csv
from bs4 import BeautifulSoup
import re

if not os.path.exists("./pokemon_data/"):
    os.mkdir("./pokemon_data/")
if not os.path.exists("./pokemon_data/poke"):
    os.mkdir("./pokemon_data/poke")

dirname = './pokemon_data/poke_html/'
decode_code = 'EUC-JP'
target_url = 'http://yakkun.com/xy/zukan/n'


#urlからhtmlをつくる関数
def url_to_html(url):
    req = urllib.request.Request(url)
    #useragent = 'Mozilla/5.0'
    #req.add_header("User-agent",useragent)
    res = urllib.request.urlopen(req)
    html = res.read()#.decode()
    return html

#htmlからをファイルに書き出す関数
def html_to_file():
    i = 1
    while i <= 10:
        url = target_url + str(i)
        html = url_to_html(url).decode(decode_code)
        filename = dirname+str(i)+".html"
        f = codecs.open(filename,'w','utf-8')
        f.write(html)
        f.close()
        print(i)
        i+=1

def scraper(html):
    soup = BeautifulSoup(html,'html.parser')
    divleft = soup.select(".table layout_left")
    print(divleft)

def main():
    i = 1
    while i <= 10:
        url = target_url + str(i)
        html = url_to_html(url).decode(decode_code)
        scraper(html)



if __name__ == '__main__':
    main()
'''
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
'''
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
