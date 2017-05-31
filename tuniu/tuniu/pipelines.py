# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
import pdb, time

class TuniuPipeline(object):
    def __init__(self):
        uri = "mongodb://%s:%s@%s/tuniu" % (
            "kst", "kst410", "121.40.107.148:27017")
        client = MongoClient(uri)
        db = client.tuniu
        self.collection = db.ask

    def process_item(self, item, spider):
        now = time.time()
        item['update_tm'] = now
        a = self.collection.find_one_and_update({"data_code":item['data_code']},{"$set":dict(item)})
        if a:
            return {'operate': 'update'}
        else:
            item['insert_tm'] = now
            self.collection.insert(dict(item))
            return {'operate': 'insert'}
