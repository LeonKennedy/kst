# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from pymongo import MongoClient
import time, logging
#logger = logging.getLogger('pipeling')

class PcautoPipeline(object):
    def __init__(self):
        uri = "mongodb://%s:%s@%s/admin" % (
            "kst", "kst410", "121.40.107.148:27017")
        client = MongoClient(uri)
        db = client.pcauto
        self.collection = db.ask

    def process_item(self, item, spider):
        item['update_tm'] = now = time.time()
        a  = self.collection.find_one_and_update({'url':item['url']},{"$set":dict(item)})
        if a:
            #logger.info("(update) %s" % item['url'])
            return {"operate":"update"}
        else:
            item['insert_tm'] = now
            self.collection.insert(dict(item))
            #logger.info("(insert) %s" % item['url'])
            return {"operate": "insert"}

