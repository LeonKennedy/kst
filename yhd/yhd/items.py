# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QAItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    product = scrapy.Field()
    question = scrapy.Field()
    question_user = scrapy.Field()
    question_tm = scrapy.Field()
    answer = scrapy.Field()
    answer_user = scrapy.Field()
    answer_tm = scrapy.Field()
