# -*- coding: utf-8 -*-
import scrapy, pdb, logging
from askspider.items import HuicaibaItem
from askspider.tools import parseContentList2Str, str2Timestamp
from pybloomfilter import BloomFilter


class HuicaibaSpider(scrapy.Spider):
    name = "huicaiba_ask"
    allowed_domains = ["huicaiba.com"]
    start_urls = ['http://huicaiba.com/']

    def __init__(self):
        bloomfilterfilename = 'bloomfilter/buicaiba.filter'
        try:
            self.bf = BloomFilter.open(bloomfilterfilename)
        except:
            logging.info("new filter.bloom")
            self.bf = BloomFilter(50000000, 0.05, bloomfilterfilename)


    def start_requests(self):
        url = 'http://www.huicaiba.com/ask/1/index_12.html'
        #url ='http://www.huicaiba.com/ask/2920820.html'
        yield scrapy.Request(url, callback=self.parse_category)

    def parse_category(self, response):
        for element_li in response.xpath('//div[@id="wdrnav1_a"]/ul[@class="ask_list"]/li') + \
            response.xpath('//div[@id="wdrnav2_a"]/ul[@class="ask_list"]/li'):
            url = response.urljoin(element_li.xpath('h3/a/@href').extract_first())
            answer_count = element_li.xpath('h3/span/text()').extract_first().replace(u'\u56de\u7b54','')
            if '0' == answer_count or (url, answer_count) in self.bf:
                print(1)
            else:
                yield scrapy.Request(url, callback=self.parse_askcard)
                self.bf.add((url, answer_count))

               


    def parse_askcard(self, response):
        item = HuicaibaItem()
        item['url'] = response.url
        item['question_title'] = response.xpath('//div[@class="wdxx"]/div[@class="line"]/h1/span/text()').extract_first()
        item['question'] = response.xpath('//div[@class="wdxx"]/div[@class="line"]/div[1]/text()').extract_first()
        ask_time = response.xpath('//span[@class="wd_fl"]/em/text()').extract()
        item['ask_time'] = str2Timestamp(''.join(ask_time))
        element_best_answer = response.xpath('//div[@class="zjda"]')
        if element_best_answer:
            item['best_answer'] = self.parse_bestanswer(element_best_answer[0]) 

        answer_list = list()
        for element in response.xpath('//ul[@class="qtlist"]/li'):
            answer_list.append(self.parse_answer(element))
        item['answer_list'] = answer_list
        item['answer_count'] = len(answer_list)
        yield item

    def parse_bestanswer(self, element):
        answer = dict()
        answer['answer_time'] = element.xpath('h2/em/text()').extract_first()
        a = element.xpath('div[1]/text()').extract()
        answer['answer'] = parseContentList2Str(a)
        return answer
        
    def parse_answer(self, element):
        answer = dict()
        answer_time = element.xpath('div[@class="qtxx"]/p[1]/em/text()').extract_first()
        answer['answer_time'] = str2Timestamp(answer_time) 
        answer_content = element.xpath('div[@class="qtxx"]/p[2]/text()').extract()
        answer['answer'] = parseContentList2Str(answer_content)
        return  answer
        


