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


class CtripItem(AskCardItem):
    user_url = scrapy.Field()
#   旅游推荐 不计入回答总数
    yoyoanswer = scrapy.Field()
#   被采纳
    bestanswer = scrapy.Field()
    tags = scrapy.Field()
    question_title = scrapy.Field()
    

