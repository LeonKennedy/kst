# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class AskCardItem(scrapy.Item):
    ask_time = scrapy.Field()
    ask_user = scrapy.Field()
    question = scrapy.Field()
    answer_list = scrapy.Field()
    answer_count = scrapy.Field()
    insert_tm = scrapy.Field()
    update_tm = scrapy.Field()
    url = scrapy.Field()


class PcautoItem(AskCardItem):
    question_title = scrapy.Field()
    best_answer = scrapy.Field()
