#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import glob
import urllib.request
import codecs
import csv
from bs4 import BeautifulSoup
import re
from collections import deque
import datetime
import sys
def expel(string,
veterans = None#["exam","ple"]
):
    try:
        string = string.rstrip()
        string = string.replace("／","/")
        if not veterans is None:
            for veteran in veterans:
                datum = string.replace(veteran,"")
    except:
        datum = 'NAexpel'
    return datum

def recruit(string):
    try:
        dq = deque(string)
        note = ""
        recruits =  [str(i) for i in range(10)] + ["."]
        while True:
            try:
                char = dq.popleft()
                if char in recruits:
                    note += char
            except Exception as e:
                break
        datum = str(note)
        if datum == "":
            datum = "NArec1"
    except:
        datum = 'NArec2'
    return datum

ints = (lambda string:int("".join(
    (lambda string:[
        (lambda char:
            char if char in [str(i) for i in range(10)] else ""
        )(char)
        for char in list(string)
    ])(string)
)))

info = [
'nc_ID','名前','販売スケジュール','完成時期','入居時期','今回販売戸数〔戸〕',
'予定価格下限〔万円〕','予定価格上限〔万円〕',
'予定最多価格帯〔万円〕',
 '管理費下限〔円〕', '管理費上限〔円〕',
 '管理準備金下限〔円〕', '管理準備金上限〔円〕',
'修繕積立金下限〔円〕','修繕積立金上限〔円〕',
'修繕積立基金下限〔円〕','修繕積立基金上限〔円〕',
'その他諸経費〔円〕'
,'間取り',
'専有面積下限〔m^2〕','専有面積上限〔m^2〕',
'バルコニー面積下限〔m^2〕','バルコニー面積上限〔m^2〕',
'その他面積〔m^2〕',
'その他制限事項','その他','物件種別','所在地',
'最寄駅1','徒歩1,バス2','駅まで1〔分〕',
'最寄駅2','徒歩1,バス2','駅まで2〔分〕',
'最寄駅3','徒歩1,バス2','駅まで3〔分〕',
'総戸数〔戸〕','構造・階建て',
'建築面積〔m^2〕','敷地面積〔m^2〕',
'敷地の権利形態','用途地域',
'駐車場台数〔台〕','駐車場料金下限〔円/月〕','駐車場料金上限〔円/月〕',
'駐輪場台数〔台〕','駐輪場料金下限〔円/月〕','駐輪場料金上限〔円/月〕',
'バイク置場台数〔台〕','バイク置場料金下限〔円/月〕','バイク置場料金上限〔円/月〕',
'ミニバイク置場台数〔台〕','ミニバイク置場料金〔円/月〕',
'管理形態','その他概要','会社情報','施工','管理','不動産会社ガイド'
]

csvwriter = csv.writer(codecs.open('suumo_data.csv','w',encoding="utf-8"))
csvwriter.writerow(info)

def url_html(url):
    req = urllib.request.Request(url)
    #useragent = 'Mozilla/5.0'
    #req.add_header("User-agent",useragent)
    res = urllib.request.urlopen(req)
    html = res.read()#.decode()
    return html

def scrape_suumo(soup, info):
    data = []

    #名前
    try:
        text = soup.find('h1', class_="fl fs20 pL10 mB5 lh25 bdGreenL3 mR10")
        text = text.get_text()
        datum = text.replace("（物件概要・スケジュール）",'').replace(';','')
        datum = datum.rsplit()[0]
    except:
        datum = 'NA'
    data.append(datum)

    try:
        text = soup.find('th',text = "販売スケジュール").next_sibling.next_sibling.get_text()
        datum = text.rsplit()[0]
    except:
        B
        datum = 'NA'
    data.append(datum)

    try:
        text = soup.find('th',text = "完成時期").next_sibling.next_sibling.get_text()
        datum = text.rsplit()[0].split("月")[0] + "月"
    except:
        datum = 'NA'
    data.append(datum)

    try:
        text = soup.find('th',text = "入居時期").next_sibling.next_sibling.get_text()
        text = text.rsplit()[0]
        text.find("即")
        datum = "即日"
    except:
        try:
            datum = text.rsplit()[0].split("月")[0] + "月"
        except:
            datum = 'NA'
    data.append(datum)

    try:
        text = soup.find('th',text = "今回販売戸数")
        text = text.next_sibling.next_sibling.get_text()
        datum = text.rsplit()[0].split("戸")[0]
    except:
        datum = 'NA'
    data.append(datum)

    #予定価格
    try:
        text = soup.find('td',class_="bdCell w265").get_text()
        text = text.split("～")
        datum1 = text[0].rsplit()[0].strip("万円")
        datum1 = recruit(datum1)
    except:
        datum1 = 'NA'
    try:
        datum2 = text[1].rsplit()[0].strip("万円")
        datum2 = recruit(datum2)
    except:
        datum2 = 'NA'
    data += [datum1, datum2]


    #予定最多価格
    try:
        text = soup.find('th',text =re.compile("予定最多価格帯"))
        text = text.next_sibling.next_sibling.get_text()
        datum = text.rsplit()[0]
        datum = recruit(datum)
    except:
        datum = 'NA'
    data.append(datum)

    #管理費
    try:
        text = soup.find('th',text = "管理費")
        text = text.next_sibling.next_sibling.get_text()
        text = text.split("～")
        datum1 = text[0].rsplit()[0].strip("万円")
        datum1 = recruit(datum1)
    except:
        datum1 = 'NA'
    try:
        datum2 = text[1].rsplit()[0].strip("万円")
        datum2 = recruit(datum2)
    except:
        datum2 = 'NA'
    data += [datum1, datum2]

    #管理準備費
    try:
        text = soup.find('th',text = "管理準備金")
        text = text.next_sibling.next_sibling.get_text()
        text = text.split("～")
        datum1 = text[0].rsplit()[0].strip("万円")
        datum1 = recruit(datum1)
    except:
        datum1 = 'NA'
    try:
        datum2 = text[1].rsplit()[0].strip("万円")
        datum2 = recruit(datum2)
    except:
        datum2 = 'NA'
    data += [datum1, datum2]

    #修繕積立金
    try:
        text = soup.find('th',text = "修繕積立金")
        text = text.next_sibling.next_sibling.get_text()
        text = text.split("～")
        datum1 = text[0].rsplit()[0].strip("万円")
        datum1 = recruit(datum1)
    except:
        datum1 = 'NA'
    try:
        datum2 = text[1].rsplit()[0].strip("万円")
        datum2 = recruit(datum2)
    except:
        datum2 = 'NA'
    data += [datum1, datum2]

    #修繕積立基金
    try:
        text = soup.find('th',text = "修繕積立基金")
        text = text.next_sibling.next_sibling.get_text()
        text = text.split("～")
        datum1 = text[0].rsplit()[0].strip("万円")
        datum1 = recruit(datum1)
    except:
        datum1 = 'NA'
    try:
        datum2 = text[1].rsplit()[0].strip("万円")
        datum2 = recruit(datum2)
    except:
        datum2 = 'NA'
    data += [datum1, datum2]

    #その他諸経費
    try:
        text = soup.find('th',text = "その他諸経費")
        text = text.next_sibling.next_sibling.get_text()
        datum = text.rsplit()[0]
    except:
        datum = 'NA'
    data.append(datum)

    #間取り
    try:
        text = soup.find('th',text = "間取り")
        text = text.next_sibling.next_sibling.get_text()
        datum = text.rsplit()[0]
    except:
        datum = 'NA'
    data.append(datum)

    #専有面積
    try:
        text = soup.find('th',text = "専有面積")
        text = text.next_sibling.next_sibling.get_text()
        text = text.split("～")
        datum1 = text[0].rsplit()[0].split("m2")[0]
    except:
        datum1 = 'NA'
    try:
        datum2 = text[1].rsplit()[0].split("m2")[0]
    except:
        datum2 = 'NA'
    data += [datum1, datum2]

    #バルコニー面積
    text = soup.find('th',text = "その他面積")
    text = text.next_sibling.next_sibling.get_text()
    try:
        text.find("バルコニー")
        try:
            text = text.split("～")
            datum1 = text[0].rsplit()[0].split("m2")[0]
            datum1 = recruit(datum1)
        except:
            datum1 = 'NA'
        try:
            text = text[1].rsplit()[0].split("m2")
            datum2 = text[0]
        except:
            datum2 = 'NA'
        try:
            datum3 = text[1].split("、")[1]
        except:
            datum3 = 'NA'
    except:
        [datum1, datum2, datum3] = ['NA', 'NA', text]
    data += [datum1, datum2, datum3]

    #
    try:
        text = soup.find('th',text = "その他制限事項")
        text = text.next_sibling.next_sibling.get_text()
        datum = text.rsplit()[0]
    except:
        datum = 'NA'
    data.append(datum)

    #
    try:
        text = soup.find('th',text = "その他")
        text = text.next_sibling.next_sibling.get_text()
        datum = text.rsplit()[0]
    except:
        datum = 'NA'
    data.append(datum)

    #
    try:
        text = soup.find('th',text = "物件種別")
        text = text.next_sibling.next_sibling.get_text()
        datum = text.rsplit()[0]
    except:
        datum = 'NA'
    data.append(datum)

    #
    try:
        text = soup.find('th',text = "所在地").next_sibling.next_sibling.get_text()#get_text()
        datum = text.rsplit()[0]
    except:
        datum = 'NA'
    data.append(datum)

    #
    try:
        text = soup.find('th',text = "交通").next_sibling.next_sibling.get_text()#get_text()
        text = text.split("「")
        sta1 = text[1].split("」")[0].rsplit()[0]
    except:
        sta1 = 'NA'
    try:
        by1 = 1 if "歩" in text[1] else\
            2 if "バス" in text[1] else\
            0
        time1 = text[1].split("分")[0]
        time1 = recruit(time1)
    except:
        [by1, time1] = ['NA', 'NA']
    try:
        sta2 = text[2].split("」")[0].rsplit()[0]
    except:
        sta2 = 'NA'
    try:
        by2 = 1 if "歩" in text[2] else\
            2 if "バス" in text[2] else\
            0
        time2 = text[2].split("分")[0]
        time2 = recruit(time2)
    except:
        [by2, time2] = ['NA', 'NA']
    try:
        sta3 = text[3].split("」")[0].rsplit()[0]
    except:
        sta3 = 'NA'
    try:
        by3 = 1 if "歩" in text[3] else\
            2 if "バス" in text[3] else\
            0
        time3 = text[3].split("分")[0]
        time3 = recruit(time3)
    except:
        [by3, time3] = ['NA', 'NA']
    data += [
        sta1, by1, time1,
        sta2, by2, time2,
        sta3, by3, time3
    ]

    #
    try:
        text = soup.find('th',text = "総戸数").next_sibling.next_sibling.get_text()#get_text()
        datum = text.rsplit()[0].split("戸")[0]
    except:
        datum = 'NA'
    data.append(datum)

    try:
        text = soup.find('th',text = "構造・階建て").next_sibling.next_sibling.get_text()#get_text()
        datum = text.rsplit()[0]
    except:
        datum = 'NA'
    data.append(datum)

    try:
        text = soup.find('th',text = "建築面積")
        text = text.next_sibling.next_sibling.get_text()
        datum = text.rsplit()[0].split("m2")[0]
        datum = recruit(datum)
    except:
        datum = 'NA'
    data.append(datum)

    try:
        text = soup.find('th',text = "敷地面積")
        text = text.next_sibling.next_sibling.get_text()
        datum = text.rsplit()[0].split("m2")[0]
        datum = recruit(datum)
    except:
        datum = 'NA'
    data.append(datum)


    try:
        text = soup.find('th',text = "敷地の権利形態").next_sibling.next_sibling.get_text()#get_text()
        datum = text.rsplit()[0]
    except:
        datum = 'NA'
    data.append(datum)

    try:
        text = soup.find('th',text = "用途地域").next_sibling.next_sibling.get_text()#get_text()
        datum = text.rsplit()[0]
    except:
        datum = 'NA'
    data.append(datum)

    #駐車場台数、料金
    try:
        text = soup.find('th',text = "駐車場")
        text = text.next_sibling.next_sibling.get_text()
        text = text.split("（")
        datum1 = text[0].rsplit()[0]
        datum1 = recruit(datum1)
    except:
        datum1 = 'NA1'
    try:
        text = text[1].split("～")
        datum2 = text[0].rsplit()[0].split("円")[0]
        datum2 = ints(datum2)
    except:
        datum2 = 'NA2'
    try:
        datum3 = text[1].rsplit()[0].split("円")[0]
        datum3 = ints(datum3)
    except:
        datum3 = 'NA3'
    data += [datum1, datum2 ,datum3]

    #駐輪場台数、料金
    try:
        text = soup.find('th',text = "駐輪場")
        text = text.next_sibling.next_sibling.get_text()
        text = text.split("（")
        datum1 = text[0].rsplit()[0]
        datum1 = recruit(datum1)
    except:
        datum1 = 'NA1'
    try:
        text = text[1].split("～")
        datum2 = text[0].rsplit()[0].split("円")[0]
        datum2 = ints(datum2)
    except:
        datum2 = 'NA2'
    try:
        datum3 = text[1].rsplit()[0].split("円")[0]
        datum3 = ints(datum3)
    except:
        datum3 = 'NA3'
    data += [datum1, datum2 ,datum3]

    #バイク置場台数、料金
    try:
        text = soup.find('th',text = "バイク置場")
        text = text.next_sibling.next_sibling.get_text()
        text = text.split("（")
        datum1 = text[0].rsplit()[0]
        datum1 = recruit(datum1)
    except:
        datum1 = 'NA1'
    try:
        text = text[1].split("～")
        datum2 = text[0].rsplit()[0].split("円")[0]
        datum2 = ints(datum2)
    except:
        datum2 = 'NA2'
    try:
        datum3 = text[1].rsplit()[0].split("円")[0]
        datum3 = ints(datum3)
    except:
        datum3 = 'NA3'
    data += [datum1, datum2 ,datum3]


    try:
        text = soup.find('th',text = "ミニバイク置場").next_sibling.next_sibling.get_text()#get_text()
        text = text.split("（")
        datum1 = text[0].rsplit()[0]
        datum1 = recruit(datum1)
    except:
        datum1 = 'NA'
    try:
        datum2 = text[1].rsplit()[0].split("円")[0]
        datum2 = ints(datum2)
    except:
        datum2 = 'NA'
    data += [datum1, datum2]

    try:
        text = soup.find('th',text = "管理形態").next_sibling.next_sibling.get_text()#get_text()
        datum = text.rsplit()[0]
    except:
        datum = 'NA'
    data.append(datum)

    try:
        text = soup.find('th',text = "その他概要").next_sibling.next_sibling.get_text()#get_text()
        datum = text.rsplit()[0]
    except:
        datum = 'NA'
    data.append(datum)

    try:
        text = soup.find('th',text = "会社情報").next_sibling.next_sibling.get_text()#get_text()
        datum = text.rsplit()[0]
    except:
        datum = 'NA'
    data.append(datum)

    try:
        text = soup.find('th',text = "施工").next_sibling.next_sibling.get_text()#get_text()
        datum = text.rsplit()[0]
    except:
        datum = 'NA'
    data.append(datum)

    try:
        text = soup.find('th',text = "管理").next_sibling.next_sibling.get_text()#get_text()
        datum = text.rsplit()[0]
    except:
        datum = 'NA'
    data.append(datum)

    try:
        text = soup.find('th',text = "不動産会社ガイド").next_sibling.next_sibling.get_text()#get_text()
        datum = text.rsplit()[0]
    except:
        datum = 'NA'
    data.append(datum)

    return  data



nowTime = str(datetime.datetime.today())
print("SUUMO-START "+nowTime)
i=0
for f in glob.glob('./suumo/tokyopages/*.html'):
    #文字コードがなにかブラウザで事前に確認しよう
    html = codecs.open(f, encoding='utf-8').read()#'r'なくても動く
    soup = BeautifulSoup(html,'html.parser')
    targets = info[1:]

    filename = os.path.basename(f).replace(".html","")
    #print(filename) #-> 0.html
    csvwriter.writerow([filename] + scrape_suumo(soup, info))






















#    l = '(        )' if i==0 else\
#        '(`       )' if i==1 else\
#        '(・｀    )' if i==2 else\
#        '(ω・`    )' if i==3 else\
#        '(・ω・`  )' if i==4 else\
#        '(´・ω・｀)' if i==5 else\
#        '(  ´・ω・)' if i==6 else\
#        '(    ´・ω)' if i==7 else\
#        '(     ´・)' if i==8 else\
#        '(       ´)'
#    print("    "+l)
#    i= i+1 if i!=8 else 0
print("SUUMO-END "+nowTime)
