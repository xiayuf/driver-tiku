#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
import sys
from bs4 import BeautifulSoup
import json
#import dryscrape
from selenium import webdriver
import time

# http://api2.jiakaobaodian.com/api/open/exercise/sequence.htm?_r=11258564547825243087&course=kemu1&carType=bus
baseurl = 'http://api2.jiakaobaodian.com/api/open/exercise/sequence.htm?_r=11258564547825243087'

# http://www.jiakaobaodian.com/mnks/exercise/3-a2-kemu1-chengdu.html?id=829400
exam_host = 'http://www.jiakaobaodian.com/mnks/exercise/0-'

ctype = {'c1': 'car','a1': 'bus', 'a2': 'truck', 'd': 'moto'}
stype = {'1': 'kemu1', '4': 'kemu3'}
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'}

def url_fact(ctype, stype, exam_id = ''):
    print 'start produce url'
    if exam_id == '':
        url = baseurl + '&course=' + stype + '&carType=' + ctype
    else:
        url = exam_host + ctype + '-' + stype + '-chengdu.html?id=' + exam_id
    print 'produced ' + url
    return url

def log(fn, msg, time = False):
    """write msg to given file name [fn]"""
    print 'write to ' + fn
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
    print 'start request ' + url
    r = requests.get(url, headers = headers)
    if r.status_code == 200:
        j = json.loads(r.content)
        if len(j['data']) > 0:
            return j['data']

def find_answer(html):
    """find the true answer of the given html document"""
    print 'start find answer'
    true_answer = []
    answer = []
    soup = BeautifulSoup(html, 'lxml')
    options = soup.find('div', {'class': 'options-container'}).findAll('p')
    for option in options:
        answer.append(option.getText()[1:])
        if 'dui' in option['class']:
            true_answer.append(option.getText()[0])
    print answer
    print true_answer
    print 'true answer found: '
    print true_answer
    return true_answer

def main():
    """grab main program"""
    for c in ctype:
        for s in stype:
            url = url_fact(stype = stype[s], ctype = ctype[c])
            exam_ids = request_url(url)
            for exam_id in exam_ids:
                print 'before produce exam_url'
                exam_url = url_fact(stype = stype[s], ctype = c, exam_id = str(exam_id))
                print 'build chrome browser'
                chrome = webdriver.PhantomJS('/usr/bin/phantomjs')
                print 'before visit'
                chrome.get(exam_url)
                print 'visit ok'
                response = chrome.page_source
                answer = find_answer(response)
                break
            break
        break
            #ids = ';\n'.join(str(c)+'|'+str(s)+'|'+str(x) for x in exam_ids)
            #log('exam_ids.txt', ids)

if __name__ == '__main__':
    main()
