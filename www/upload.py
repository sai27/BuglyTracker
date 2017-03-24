#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'sai27'

import requests, os

'''
crashDoc = None
appDetail = None
with open('D:/bugly_v2.4/77_C4_0E_5A_DB_5B_07_E5_89_87_C0_83_C2_C6_36_98_crashDoc.json','r', encoding='utf-8') as f:
    crashDoc = f.read()
with open('D:/bugly_v2.4/77_C4_0E_5A_DB_5B_07_E5_89_87_C0_83_C2_C6_36_98_appDetail.json','r', encoding='utf-8') as f:
    appDetail = f.read()


r = requests.post("http://127.0.0.1:8000/api/upload", data={
    'name' : '77_C4_0E_5A_DB_5B_07_E5_89_87_C0_83_C2_C6_36_98',
    'crashDoc' : crashDoc,
    'appDetail' : appDetail
})

print(r.text)
'''

def upload(filepath, url):
    idx = 0
    for root, dirs, files in os.walk(filepath):
        for file in files:
            if file.endswith('_crashDoc.json'):
                name = file[:-14]
                crashDocPath = name + '_crashDoc.json'
                crashDocPath = os.path.join(root, crashDocPath)
                appDetailPath = name + '_appDetail.json'
                appDetailPath = os.path.join(root, appDetailPath)
                crashDoc = ""
                appDetail = ""
                if os.path.isfile(crashDocPath):
                    with open(crashDocPath,'r', encoding='utf-8') as f:
                        crashDoc = f.read()
                if os.path.isfile(appDetailPath):
                    with open(appDetailPath,'r', encoding='utf-8') as f:
                        appDetail = f.read()
                r = requests.post(url, data={
                    'name' : name,
                    'crashDoc' : crashDoc,
                    'appDetail' : appDetail
                })
                if r.text != "success":
                    print(idx, ":", r.text)
                idx += 1

upload("D:/bugly_v2.4", "http://127.0.0.1:8000/api/upload")