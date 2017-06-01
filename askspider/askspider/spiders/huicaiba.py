# -*- coding: utf-8 -*-
import scrapy


class HuicaibaSpider(scrapy.Spider):
    name = "huicaiba"
    allowed_domains = ["huicaiba.com"]
    start_urls = ['http://huicaiba.com/']

    def parse(self, response):
        pass
