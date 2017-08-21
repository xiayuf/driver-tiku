#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import json
from bs4 import BeautifulSoup

'''grab question id and save it to question-ids.txt file'''

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

def get_json(url):
    ''' make GET request and return '''

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'}
    result = requests.get(url, headers = headers)
    if result.status_code == 200:
        return json.loads(result.content)
    else:
        return None

# http://api2.jiakaobaodian.com/api/open/exercise/sequence.htm?_r=11258564547825243087&course=kemu1&carType=bus
def Iturls():
    ''' return Iterator '''

    base_url = 'http://api2.jiakaobaodian.com/api/open/exercise/sequence.htm?_r=11258564547825243087'
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
    return ({'car_type': s['car_type'], 'course': s['course'], 'url': base_url + '&course=' + s['course'] + '&carType=' + s['car_type']} for s in settings)

# run here
if __name__ == '__main__':
    for item in Iturls():
        print item
        result = get_json(item['url'])
        question_ids = result[u'data']

        raw_string = '\n'.join(str(item['car_type']) + '|' + str(item['course']) + '|' + str(id) for id in question_ids)
        save_txt(raw_string, 'question_ids.txt')
