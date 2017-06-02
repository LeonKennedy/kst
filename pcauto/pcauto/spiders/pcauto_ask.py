# -*- coding: utf-8 -*-
import scrapy, pdb, logging
from pcauto.items import PcautoItem
from pcauto.tools import parseContentList2Str, str2Timestamp
from pybloomfilter import BloomFilter


class PcautoAskSpider(scrapy.Spider):
    name = "pcauto_ask"
    allowed_domains = ["pcauto.com.cn"]
    #start_urls = ['http://k.pcauto.com.cn/question/4035240.html']
    start_urls= ['http://k.pcauto.com.cn/question/k16/p1.html']

    def __init__(self):
        bloomfilterfilename = 'pcauto.filter'
        try:
            self.bf = BloomFilter.open(bloomfilterfilename)
        except:
            logging.info("new filter.bloom")
            self.bf = BloomFilter(50000000, 0.05, bloomfilterfilename)


    def start_requests(self):
        urls = [ "http://k.pcauto.com.cn/question/k%d/p1.html" % i for i in (1,2,4,5,6)]
        for url in urls:
            yield scrapy.Request(url, callback = self.parse_category)

    def parse_category(self, response):
        for element_li  in response.xpath('//ul[@id="wtList"]/li[@class!="liTit"]'):
            url = element_li.xpath('i[@class="iTitle"]/a/@href').extract_first()
            num = element_li.xpath('i[@class="iNum"]/text()').extract_first()
            #状态 用来记录是否有最佳答案
            phase = True if element_li.xpath('i[@class="iPhase"]/span[@class="icon_jj"]') else False
            #print("%s [%s]" % (url, num))
            if phase:
                if (url, phase) not in self.bf:
                    yield scrapy.Request(url, callback=self.parse_askcard)
                    self.bf.add((url, phase))
            else:
                if not num == '0' and (url, phase, num) not  in self.bf:
                    yield scrapy.Request(url, callback=self.parse_askcard)
                    self.bf.add((url, phase, num))
        next_url = response.xpath('//div[@class="pcauto_page"]/a[@class="next"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(response.urljoin(next_url),callback=self.parse_category)

    def parse_askcard(self, response):
        item = PcautoItem()
        item['url'] = response.url
        question_title = response.xpath('//div[@id="question_content"]/div[@class="modInner"]/div[1]//text()').extract()
        item['question_title'] = parseContentList2Str(question_title)
        item['question'] = response.xpath('//div[@class="modInner"]/p/text()').extract_first()
        ask_time = response.xpath('//div[@class="dInfo gray"]/span[@class="sTime"]/text()').extract_first()
        item['ask_time'] = str2Timestamp(ask_time)
        user_name = response.xpath('//div[@class="dInfo gray"]/span[@class="sName"]/a/text()').extract_first()
        user_url = response.xpath('//div[@class="dInfo gray"]/span[@class="sName"]/a/@href').extract_first()
        item['ask_user'] = {'name': user_name, 'url':user_url}
        element_best_answer = response.xpath('//div[@class="modAnswer modBest mt10"]//div[@class="tb"]')
        item['best_answer'] = self.parse_answer(element_best_answer[0]) if element_best_answer else None
        
        answer_list = list()
        for element in response.xpath('//div[@class="modAnswer mt10 modOut"]/div[@class="modInner"]/div[@class!="th"]'):
            answer_list.append(self.parse_answer(element))
        item['answer_list'] = answer_list
        item['answer_count'] = len(answer_list)
        yield item

    def parse_answer(self, element):
        answer = dict()
        answer['id'] = element.xpath('div[2]/@id').extract_first()
        user_icon = element.xpath('.//img/@src').extract_first()
        element_user = element.xpath('.//i[@class="blue"]') or element.xpath('.//div[@class="dTitle"]')
        user_name = element_user[0].xpath('a/text()').extract_first()
        user_url = element_user[0].xpath('a/@href').extract_first()
        answer['user'] = {'name': user_name, 'url': user_url, 'icon': user_icon}
        answer_time = ''.join(element.xpath('.//div[@class="gray"]/text()').extract())
        answer['answer_time'] = str2Timestamp(answer_time) or element.xpath('.//span[@class="sTime"]/text()').extract_first()
        answer['answer'] = element.xpath('.//div[@class="answerCon"]/p/text()').extract_first()
        return  answer
        


