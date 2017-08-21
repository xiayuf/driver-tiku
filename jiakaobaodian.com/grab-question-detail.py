#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import json
from bs4 import BeautifulSoup

'''grab question detail'''

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
        return json.loads(str(result.content))
    else:
        return None

# http://api2.jiakaobaodian.com/api/open/question/question-list.htm?_r=15822608861463596095&page=1&_=0.877899413535759&questionIds=836500
def build_url(question_ids):
    ''' return Iterator '''

    base_url = 'http://api2.jiakaobaodian.com/api/open/question/question-list.htm?_r=15822608861463596095&page=1&_=0.877899413535759&questionIds='
    return base_url + question_ids

def Itquestions(file_name = 'resource_question_ids.txt'):
    fp = open(file_name, 'r')
    contents = fp.read()
    chapters = filter(lambda x: x != '', contents.split('\n'))
    fp.close()
    return (chapter.split('|') for chapter in chapters)

if __name__ == '__main__':
    counter = 0
    for question in Itquestions():
        url = build_url(question[2])
        question_detail = get_json(url)[u'data'][0]
        q = question_detail

        # answer,chapter_id,difficulty,explain,id,label,media_height,media_type,media_width,option_a,option_b,option_c,option_d,option_e,option_f,option_g,option_h,option_type,question,question_id,media_content,false_count,true_count,wrong_rate
        if not q.has_key(u'mediaContent'):
            q[u'mediaContent'] = ''
        if q[u'explain'] == None:
            q[u'explain'] = ''
        if q[u'optionC'] == None:
            q[u'optionC'] = ''
        if q[u'optionD'] == None:
            q[u'optionD'] = ''
        if q[u'optionE'] == None:
            q[u'optionE'] = ''
        if q[u'optionF'] == None:
            q[u'optionF'] = ''
        if q[u'optionG'] == None:
            q[u'optionG'] = ''
        if q[u'optionH'] == None:
            q[u'optionH'] = ''
        _s = [
            str(q[u'answer']),
            str(q[u'chapterId']),
            str(q[u'difficulty']),
            str(q[u'explain'].encode('UTF-8')),
            str(q[u'id']),
            str(q[u'label']),
            str(q[u'mediaHeight']),
            str(q[u'mediaType']),
            str(q[u'mediaWidth']),
            str(q[u'optionA'].encode('UTF-8')),
            str(q[u'optionB'].encode('UTF-8')),
            str(q[u'optionC'].encode('UTF-8')),
            str(q[u'optionD'].encode('UTF-8')),
            str(q[u'optionE'].encode('UTF-8')),
            str(q[u'optionF'].encode('UTF-8')),
            str(q[u'optionG'].encode('UTF-8')),
            str(q[u'optionH'].encode('UTF-8')),
            str(q[u'optionType']),
            str(q[u'question'].encode('UTF-8')),
            str(q[u'questionId']),
            str(q[u'mediaContent'].encode('UTF-8')),
            str(q[u'falseCount']),
            str(q[u'trueCount']),
            str(q[u'wrongRate'])
        ]
        raw_string = ','.join(_s)
        save_txt(raw_string, 'resource_question_detail.txt')
        counter = counter + 1
        print 'now %d has been completed' % counter

