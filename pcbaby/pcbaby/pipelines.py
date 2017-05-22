# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class PcbabyPipeline(object):

    def __init__(self):
        uri = "mongodb://%s:%s@%s/pcbaby" % (
            "kst", "kst410", "121.40.107.148:27017")
        client = MongoClient(uri)
        db = client.pcbaby
        self.collection = db.ask

    def process_item(self, item, spider):
        a  = self.collection.find_one({'url':item['url']})
        if not a:
            self.collection.insert(dict(item))
        return {"success":True}

