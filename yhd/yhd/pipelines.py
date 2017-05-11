# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from yhd.mysql import MysqlTool
import json

class YhdPipeline(object):

    def __init__(self):

        self.mt = MysqlTool(host='localhost',user ='kst',password='kst410', db='kst')
        self.count = 0

        self.filecache = ""
        self.datafile = 'yhd-2.json'

    def process_item(self, item, spider):
        self.mt.insertByDict('yhd_ask', item)
        self.filecache += json.dumps(dict(item), ensure_ascii=False) 
        self.filecache += '\n'
        self.count += 1
        if self.count == 100:
            self.mt.flush()
            self.count = 0
            with open(self.datafile, 'a+') as f:
                f.write(self.filecache)
            self.filecache = ''
        return item

    def close_spider(self,spider):
        self.mt.connect.commit()
        with open(self.datafile, 'a+') as f:
            f.write(self.filecache)


