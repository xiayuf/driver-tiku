#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
import sys
from bs4 import BeautifulSoup
import json

# http://api2.jiakaobaodian.com/api/open/exercise/sequence.htm?_r=11258564547825243087&course=kemu1&carType=bus
baseurl = 'http://api2.jiakaobaodian.com/api/open/exercise/sequence.htm?_r=11258564547825243087'
ctype = {'c1': 'car','a1': 'bus', 'a2': 'truck', 'd': 'moto'}
stype = {'1': 'kemu1', '4': 'kemu3'}
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'}

def url_fact(ctype, stype):
    url = baseurl + '&course=' + stype + '&carType=' + ctype
    return url

def log(fn, msg, time = False):
    """write msg to given file name [fn]"""
    if os.path.isfile(fn):
        fp = open(fn, 'a')
    else:
        fp = open(fn, 'w')
    if msg != '':
        msg = msg + '\n'
    else:
        return False
    if time == False:
        log = msg
        fp.write(log)
        fp.close()

def request_url(url):
    """make request to the given url"""
    r = requests.get(url, headers = headers)
    if r.status_code == 200:
        j = json.loads(r.content)
        if len(j['data']) > 0:
            return j['data']


def main():
    for c in ctype:
        for s in stype:
            url = url_fact(stype = stype[s], ctype = ctype[c])
            exam_ids = request_url(url)
            ids = '\n'.join(str(c)+'|'+str(s)+'|'+str(x) for x in exam_ids)
            log('exam_ids.txt', ids)

if __name__ == '__main__':
    main()
