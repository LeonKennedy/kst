# -*- coding: utf-8 -*-
import scrapy, pdb, logging
from pcbaby.items import PcbabyItem
from datetime import datetime
from datetime import timedelta
from pybloomfilter import BloomFilter
class PcbabyAskSpider(scrapy.Spider):
    def __init__(self):
        try:
            self.bf = BloomFilter.open('filter.bloom')
        except:
            logging.info("new filter.bloom")
            self.bf = BloomFilter(100000000, 0.05, 'filter.bloom')

    name = "pcbaby_ask"
    allowed_domains = ["pcbaby.com.cn"]
    #start_urls = ['http://kuaiwen.pcbaby.com.cn/']
    start_urls = [ 'http://kuaiwen.pcbaby.com.cn/question/t%d/p1.html' % i for i in (1,2,3,4,5,6,7,8,9,10,11,30161,30162,30163,30164,30165)]

    def start_requests(self):
        urls = [ 'http://kuaiwen.pcbaby.com.cn/question/t%d/p1.html' % i for i in range(1,12) + range(30161,30166)]
        for category_url in urls:
            #print(category_url)
            yield scrapy.Request(category_url, callback=self.parse)

    def parse(self, response):
        count = zore_count = 0
        for element_askcard in response.xpath('//ul[@class="qaList-ulList "]/li'):
            reply_count = element_askcard.xpath('p[@class="pQ"]/span[1]/em/text()').extract_first()
            askcard_url = "http:" + element_askcard.xpath('p[@class="pQ"]/a[1]/@href').extract_first()
            time_interval = element_askcard.xpath('p[@class="pAuthor"]/span[2]/text()').extract_first()
            if reply_count == '0':
                zore_count += 1
            elif (askcard_url,reply_count) in self.bf:
                count += 1
            else:
                yield scrapy.Request(url=askcard_url, callback=self.parse_askcard)
                self.bf.add((askcard_url,reply_count))
        if count > 0:
            total = len(response.xpath('//ul[@class="qaList-ulList "]/li'))
            logging.info("[%d page had been crawl %d, zero is %d] %s" % (total, count, zore_count, response.url))

        next_url = response.xpath('//div[@class="pcbaby-page mb10"]/a[@class="next"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(url="http:" + next_url, callback = self.parse)
        

    def parse_askcard(self, response):
        item = PcbabyItem()
        element_question = response.xpath('//dl[@class="wt-PicTxt"]')
        item['category'] = '/'.join(response.xpath('//p[@class="position"]/a/text()').extract())
        user_icon = element_question.xpath('dt//img/@src').extract_first()
        user_url = response.urljoin(element_question.xpath('dd/p[1]//a/@href').extract_first())
        user_name = element_question.xpath('dd/p[1]//a/text()').extract_first()
        item['ask_user'] = {'icon':user_icon, 'url':user_url, 'name':user_name}
        item['ask_time'] = element_question.xpath('dd/p[1]/span[@class="fr"]/i[2]/text()').extract_first()
        item['question_title'] = element_question.xpath('.//p[@class="wt-PicTxt-Title"]/text()').extract_first()
        item['question'] = element_question.xpath('.//p[@class="wt-PicTxt-Txt"]/text()').extract_first()
        item['best_answer'] = self.parse_answer(response.xpath('//div[@class="wt-wd wt-bestAns"]/dl[1]/dd[1]'))

        answers = list()
        for element_askcard in response.xpath('//div[@class="lBox-tb"]/dl[1]/dd[@class="last"]'):
            answers.append(self.parse_answer(element_askcard))
        item['answer_list'] = answers
        item['answer_count'] = len(answers) + 1 if item['best_answer'] else len(answers)
        item['url'] = response.url
        yield item

        
    def parse_answer(self, element):
        if not element:
            return None
        ans = dict()
        name = element.xpath('p[1]/span[1]/i[1]/a[1]/text()').extract_first()
        url = element.xpath('p[1]//a/@href').extract_first()
        ans['answer_user'] = {'name': name, 'url':url}
        time_interval = element.xpath('p[1]/span[1]/i')[-1].xpath('text()').extract_first()
        ans['answer_time'] = self.parse_time(time_interval)
        ans['answer'] = ' '.join(element.xpath('div[@class="wt-PicTxt-Txt"]//text()').extract())
        tags = list()
        for element_tag in element.xpath('div[@class="jh-titles"]/a'):
            tag_url = element_tag.xpath('@href').extract_first()
            tag_name = element_tag.xpath('text()').extract_first()
            tags.append({'tag_url':tag_url,'tag_name':tag_name})
        ans['answer_tags'] = tags or None
        return ans

        #显示 timestamp x小时前  x天前 x分钟前
    def parse_time(self, t):
        if u'\u5c0f\u65f6\u524d' in t:
            t = datetime.now() - timedelta(hours = int(t.replace(u'\u5c0f\u65f6\u524d','')))
        elif u'\u5929\u524d' in t:
            t = datetime.now() - timedelta(days = int(t.replace(u'\u5929\u524d','')))
        elif u'\u5206\u949f\u524d' in t:
            t = datetime.now() - timedelta(minutes = int(t.replace(u'\u5206\u949f\u524d','')))
        return str(t)
        


