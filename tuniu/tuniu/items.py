# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class AskCardItem(scrapy.Item):
    insert_tm = scrapy.Field()
    update_tm = scrapy.Field()

class TuniuItem(AskCardItem):
    
    ask_time = scrapy.Field()
    ask_user = scrapy.Field()
    ask_tag = scrapy.Field()
    city = scrapy.Field()
    question = scrapy.Field()
    question_content = scrapy.Field()
    answer_list = scrapy.Field()
    data_code = scrapy.Field()
    url = scrapy.Field()
    answer_count = scrapy.Field()

