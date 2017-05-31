#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @Filename: tools.py
# @Author: olenji - lionhe0119@hotmail.com
# @Description: ---
# @Create: 2017-05-25 09:12:10
# @Last Modified: 2017-05-25 09:12:10
#

import re,pdb
from datetime import datetime,timedelta
#时间转换
# u'\u53d1\u8868\u4e8e2017-05-10 23:32:56'   => 发表于2017-05-10 23:32:56
# u'\u53d1\u8868\u4e8e17\u5206\u949f\u524d'   => 发表于17分钟前
# u'\u5c0f\u65f6\u524d'          => 小时前
# u'\u5929\u524d'                  =>  天前
# u'\u5206\u949f\u524d'            => 分钟前
def str2Timestamp(timestr):
    if not timestr:
        return None
    a1 = re.search(ur'\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}(:\d{1,2})?', timestr)
    if a1:
        return a1.group(0)
    a = re.search(ur'\d+(?=\u5206\u949f\u524d)', timestr)
    if a:
        t = datetime.now() - timedelta(minutes = int(a.group(0)))
        return str(t)
    b = re.search(ur'\d+(?=\u5c0f\u65f6\u524d)', timestr)
    if b:
        t = datetime.now() - timedelta(hours = int(b.group(0)))
        return str(t)
    c = re.search(ur'\d+(?=\u5929\u524d)', timestr)
    if c:
        t = datetime.now() - timedelta(days = int(c.group(0)))
        return str(t)
    return timestr


def parseContentList2Str(content_list):
    c = ''
    for content in content_list:
        c += content.strip() 
    return c

