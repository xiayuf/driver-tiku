#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''grab chapter id and save it to chapter-ids.txt file'''

import os
import sys
import requests
import json
from bs4 import BeautifulSoup

def save_txt(content, file_name = 'log.txt', new_line = True, over_write = False):
    ''' save text to file '''
    if over_write:
        fp = open(file_name, 'w')
    else:
        fp = open(file_name, 'a')
    if new_line:
        content = str(content) + '\n'
    fp.write(content)
    fp.close()

# http://m.jiakaobaodian.com/mnks/chapter/car-kemu3-hefei.html
def Iturls():
    '''return Iterator'''
    base_url = 'http://m.jiakaobaodian.com/mnks/chapter/'
    settings = [
        {'car_type': 'bus', 'course': 'kemu1'},
        {'car_type': 'bus', 'course': 'kemu3'},
        {'car_type': 'truck', 'course': 'kemu1'},
        {'car_type': 'truck', 'course': 'kemu3'},
        {'car_type': 'car', 'course': 'kemu1'},
        {'car_type': 'car', 'course': 'kemu3'},
        {'car_type': 'moto', 'course': 'kemu1'},
        {'car_type': 'moto', 'course': 'kemu3'},
        {'car_type': 'keyun', 'course': 'zigezheng'},
        {'car_type': 'huoyun', 'course': 'zigezheng'},
        {'car_type': 'weixian', 'course': 'zigezheng'},
        {'car_type': 'jiaolian', 'course': 'zigezheng'},
        {'car_type': 'chuzu', 'course': 'zigezheng'}
    ]
    return ({'car_type': s['car_type'], 'course': s['course'], 'url': base_url + s['car_type'] + '-' + s['course'] + '-hefei.html'} for s in settings)

def get_html(url):
    ''' make GET request and return '''

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'}
    result = requests.get(url, headers = headers)
    if result.status_code == 200:
        return result.content
    else:
        return None

def parse(content):
    '''parse to get chapter list'''

    soup = BeautifulSoup(content, 'lxml')
    div = soup.find('div', attrs = {'data-item': 'jkbd-tiku-chapterlist'})
    if div:
        lis = div.findAll('li')
    chapter_ids = []
    for li in lis:
        chapter_id = li.get('data-id')
        chapter_ids.append(chapter_id)
    return chapter_ids

# run here
if __name__ == '__main__':
    for item in Iturls():
        print item
        html = get_html(item['url'])
        chapter_ids = parse(html)
        print chapter_ids

        raw_string = '\n'.join(str(item['car_type']) + '|' + str(item['course']) + '|' + str(id) for id in chapter_ids)
        save_txt(raw_string, 'chapter_ids.txt')
