#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import json
from bs4 import BeautifulSoup

'''grab chapter detail'''

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

def Itchapters(file_name = 'resource_chapter_ids.txt'):
    fp = open(file_name, 'r')
    contents = fp.read()
    chapters = filter(lambda x: x != '', contents.split('\n'))
    fp.close()
    return (chapter.split('|') for chapter in chapters)

def get_json(url):
    ''' make GET request and return '''

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'}
    result = requests.get(url, headers = headers)
    if result.status_code == 200:
        return json.loads(str(result.content))
    else:
        return None

# http://api2.jiakaobaodian.com/api/open/exercise/chapter.htm?_r=11258564547825243087&course=kemu1&carType=truck&chapterId=140
def build_url(s):
    ''' return Iterator '''

    base_url = 'http://api2.jiakaobaodian.com/api/open/exercise/chapter.htm?_r=11258564547825243087'
    return base_url + '&course=' + s[1] + '&carType' + s[0] + '&chapterId=' + s[2]

if __name__ == '__main__':
    for chapter in Itchapters():
        url = build_url(chapter)
        chapter_detail = get_json(url)[u'data'][u'chapter']

        # car_type,course,chapter_id,chapter,title,count
        _s = [chapter[0] , chapter[1] , chapter[2] , str(chapter_detail[u'chapter']) , chapter_detail[u'title'] , str(chapter_detail[u'count'])]
        raw_string = ','.join(_s)
        utf8_string = raw_string.encode('UTF-8')
        print utf8_string
        save_txt(utf8_string, 'resource_chapter_detail.txt')
