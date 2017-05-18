# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TuniuItem(scrapy.Item):
    ask_time = scrapy.Field()
    ask_user = scrapy.Field()
    ask_tag = scrapy.Field()
    city = scrapy.Field()
    question = scrapy.Field()
    question_content = scrapy.Field()
    answer_list = scrapy.Field()
    data_code = scrapy.Field()
