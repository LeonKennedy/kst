# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from items import HuicaibaItem
from pymongo import MongoClient
import time, logging

class AskspiderPipeline(object):
    def __init__(self):
        #uri = "mongodb://%s:%s@%s/admin" % ("kst", "kst410", "121.40.107.148:27017")
        self.client = MongoClient()

    def process_item(self, item, spider):
        item['update_tm'] = now = time.time()
        if isinstance(item, HuicaibaItem):
            db = self.client.huicaiba
            collection = db.ask
        else:
            return {"operate":None}

        a  = collection.find_one_and_update({'url':item['url']},{"$set":dict(item)})
        if a:
            #logger.info("(update) %s" % item['url'])
            return {"operate":"update"}
        else:
            item['insert_tm'] = now
            collection.insert(dict(item))
            #logger.info("(insert) %s" % item['url'])
            return {"operate": "insert"}

