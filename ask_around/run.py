#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @Filename: run.py
# @Author: olenji - lionhe0119@hotmail.com
# @Description: ---
# @Create: 2017-04-20 13:24:21
# @Last Modified: 2017-04-20 13:24:21
#


import requests, pdb, pymysql, traceback
from bs4 import BeautifulSoup

class Taobao:

    def __init__(self):
        self.connect = pymysql.connect(host='localhost',user = 'kst',password='kst410',
                db='kst', charset='utf8mb4')
        self.cur = self.connect.cursor()
        self.s = requests.Session()
    def marketpage(self):
        url = "https://www.taobao.com/tbhome/page/market-list"
        r = self.s.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        records = list()
        for items in soup('div',class_='category-items'):
            subitems = items('a', class_='category-name')
            for item in subitems:
                record = {'url' : item.get('href'), 'text' : item.text}
                records.append(record)
        self.pip_market(records)
    def pip_market(self, records):
        for r in records:
            sql = "insert into taobao_category set name='%s', url='%s';" % (r['text'], r['url'])
            try:    
                self.cur.execute(sql)
            except:
                print(sql)
                traceback.print_exc()

    def __del__(self):
        self.connect.commit()
        self.cur.close()
        self.connect.close()



if __name__ == "__main__":
    t = Taobao()
    t.marketpage()



