# -*- coding: utf-8 -*-
import scrapy,pdb, logging
from ctrip.items import CtripItem
from ctrip.tools import parseContentList2Str, str2Timestamp
from pybloomfilter import BloomFilter


class CtripAskSpider(scrapy.Spider):
    name = "ctrip_ask"
    allowed_domains = ["ctrip.com"]
    baseurl = 'http://you.ctrip.com'
    start_urls = [
        'http://you.ctrip.com/asks',
     #   'http://you.ctrip.com/asks/hulunbeier458/3979605.html',
         # 'http://you.ctrip.com/asks/shenzhen26/1259915.html'
         # 'http://you.ctrip.com/asks/shanghai2/4073570.html'
        ]

    def __init__(self):
        bloomfilterfilename = 'ctrip.filter'
        try:
            self.bf = BloomFilter.open(bloomfilterfilename)
        except:
            logging.info("new filter.bloom")
            self.bf = BloomFilter(100000000, 0.05, bloomfilterfilename)

    def parse(self, response):
        crawled = zero = 0
        for element_askcard in response.xpath('//ul[@class="asklist"]/li'):
            url = response.urljoin(element_askcard.xpath('@href').extract_first())
            count =  element_askcard.xpath('span[1]/b[1]/text()').extract_first()
            if count == '0':
                zero += 1
                continue
            if (url,count) in self.bf:
                crawled += 1
            else:
                yield scrapy.Request(url=url, callback=self.parse_askcard)
                self.bf.add((url,count))
        if crawled > 0:
            total = len(response.xpath('//ul[@class="asklist"]/li')) 
            logging.info("[%d page had been crawl %d, zero is %d] %s" % (total, crawled, zero, response.url))

        next_url = response.urljoin(response.xpath('//a[@class="nextpage"]/@href').extract_first())
        if next_url:
            yield scrapy.Request(url=next_url, callback = self.parse)

        
    def parse_askcard(self, response):
        item = CtripItem()
        item['url'] = response.url
        element_question = response.xpath('//div[@class="detailmain_top"]')[0]
        item['ask_user'] = element_question.xpath('.//span[@class="ask_idtime"]/a[1]/text()').extract_first()
        item['user_url'] = self.baseurl + element_question.xpath('.//span[@class="ask_idtime"]/a[1]/@href').extract_first()
        ask_time = element_question.xpath('.//span[@class="ask_time"]/text()').extract_first()
        item['ask_time'] = str2Timestamp(ask_time)
        tags = list()
        for element_tag in element_question.xpath('.//div[@class="asktag_oneline cf"]/a'):
            tag_url = response.urljoin(element_tag.xpath('@href').extract_first())
            title = element_tag.xpath('@title').extract_first()
            tags.append({'tag_url':tag_url,'tag_title': title})
        item['tags'] = tags
        question_title = element_question.xpath('.//h1[@class="ask_title"]/text()').extract()
        item['question_title'] = parseContentList2Str(question_title)
        question_contents = element_question.xpath('.//p[@id="host_asktext"]//text()').extract()
        item['question'] = parseContentList2Str(question_contents)
        tempanswer = response.xpath('//div[@class=" youyouanswer_con"]')
        item['yoyoanswer'] = self.parse_answer(tempanswer.pop()) if tempanswer else None
        tempanswer = response.xpath('//div[@class=" bestanswer_con"]')
        item['bestanswer'] = self.parse_answer(tempanswer.pop()) if tempanswer else None
        
        answer_list = list()
        for element_answer  in response.xpath('//div[@id="replyboxid"]/ul[1]/li'):
            answer_list.append(self.parse_answer(element_answer))
        item['answer_list'] = answer_list
        yield item

    #bug1 : 页面有js加载
    def parse_answer(self, element):
        answer = dict()
        answer['id'] = element.xpath('div[1]/@data-answerid').extract_first()
        answer['userid'] = element.xpath('div[1]/@data-answeruserid').extract_first()
        #这里都是js加载 先注释掉
        #answer['user_icon'] = element.xpath('.//img/@src').extract_first()
        #answer['user_url'] = self.baseurl + element.xpath('div[1]/a[1]/@href').extract_first()
        #answer['user_name'] = element.xpath('.//a[@class="answer_id"]/text()').extract_first()
        interval_tm = element.xpath('.//span[@class="answer_time"]/text()').extract_first()
        answer_contents = element.xpath('.//p[@class="answer_text"]//text()').extract()
        answer['answer'] = parseContentList2Str(answer_contents)
        answer_time = element.xpath('.//span[@class="answer_time"]/text()').extract_first()
        answer['answer_time'] = str2Timestamp(answer_time)
        like = element.xpath('.//a[@class="btn_answer_zan"]/span[1]/text()').extract_first()
        answer['like'] = int(like) if like else 0
        answer['imgs'] = element.xpath('.//div[@class="ask_piclist cf"]/a/@href').extract() or None
        return  answer
        


