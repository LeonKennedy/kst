# -*- coding: utf-8 -*-
import scrapy, pdb, logging, traceback
from tuniu.items import TuniuItem


class TuniuAskSpider(scrapy.Spider):
    name = "tuniu_ask"
    allowed_domains = ["tuniu.com"]
    start_urls = ['http://ask.tuniu.com']
    baseurl = "http://ask.tuniu.com"
    current_page_number = 7760
    #末尾页数
    #end_page_number = 71267
    end_page_number = 10000

    def parse(self, response):
        for ask_card in response.xpath('//div[@class="moudle-list J_MList"]'):
            answer_count = ask_card.xpath('.//div[@class="moudle-bottom-right"]/span[2]/em/text()').extract_first()
            browse_count  = ask_card.xpath('.//div[@class="moudle-bottom-right"]/span[3]/em/text()').extract_first()
            elements_a =  ask_card.xpath('.//p[@class="moudle-title"]/a')
            #一般会有两条,一条话题 一条title可以抽取url   
            # 但有时只有一天 直接抽取
            card_url = None
            if len(elements_a) == 1:
                card_url = self.baseurl + elements_a[0].xpath('@href').extract_first()
            elif len(elements_a) == 2 : 
                card_url = self.baseurl + elements_a[1].xpath('@href').extract_first()
            else:
                pdb.set_trace()
            if card_url:
                yield scrapy.Request(card_url, callback = self.parse_askcard, meta = {'answer_count': answer_count, 'browse_count':browse_count})

        if self.current_page_number < self.end_page_number:
            self.current_page_number += 1
            url = self.baseurl + "/p%d/" % self.current_page_number
            yield scrapy.Request(url,callback = self.parse)

#    def parse(self, response):
    def parse_askcard(self, response):
        #检测是不是最后一页
        last_element = response.xpath('//div[@id="pagination"]/a')
        # u'\u4e0b\u4e00\u9875' is '下一页'
        isLast = False if last_element and last_element[-1].xpath('text()').extract_first() == u'\u4e0b\u4e00\u9875' else True
        a = response.meta.get('answer_list') or list()
        for element_answer in response.xpath('//div[@class="qa-details J_MoudleDetails"]/div'):
            a.append(self.parse_answer(element_answer))
        if isLast:
            try:
                item = TuniuItem()
                element_ask = response.xpath('//div[@class="moudle-delist"]/div[1]')
                item['data_code'] = element_ask.xpath('.//div[@class="moudle-operate moudle-share qa-icon J_Share"]/@data-code').extract_first()
                item['ask_time'] = element_ask.xpath('.//span[@class="moudle-right-list"]/text()').extract_first()
                item['question'] = element_ask.xpath('.//div[@class="moudle-title"]/h1/span/text()').extract_first()
                item['question_content'] = element_ask.xpath('.//p[@class="moudle-bewrite"]/text()').extract_first().replace('\r\n','').strip()
                city_url = response.urljoin(element_ask.xpath('.//div[@class="moudle-title"]/a/@href').extract_first())
                city_name = element_ask.xpath('.//div[@class="moudle-title"]/a/text()').extract_first()
                item['city'] = {'name': city_name, 'url': city_url}
                user_icon = element_ask.xpath('.//img/@src').extract_first()
                user_name = element_ask.xpath('.//div[@class="moudle-user-name"]/a/text()').extract_first()
                user_url = element_ask.xpath('.//div[@class="moudle-user-name"]/a/@href').extract_first()
                item['ask_user'] = {'icon': user_icon, 'name':user_name, 'url':user_url}
                tag_list = list()
                for element_tag in element_ask.xpath('.//p[@class="moudle-tag"]/span'):
                    tag_name = element_tag.xpath('a/text()').extract_first()
                    tag_url = response.urljoin(element_tag.xpath('a/@href').extract_first())
                    tag_list.append({'tag_name': tag_name, 'tag_url': tag_url})
                item['ask_tag'] = tag_list
                item['answer_list'] = a
                yield item
            except:
                logging.error("%s" % response.url)
                traceback.print_exc()
        else:
            url = response.urljoin(last_element[-1].xpath('@href').extract_first())
            yield scrapy.Request(url, callback = self.parse_askcard, meta = {'answer_list' : a})

    def parse_answer(self, element):
        answer = dict()
        answer['answer'] = element.xpath('.//p[@class="moudle-bewrite"]/text()').extract_first().replace('\r\n','').strip()
        answer['answer_time'] = element.xpath('.//div[@class="moudle-bottom J_AcceptBox"]/span/text()').extract_first()
        user_icon = element.xpath('.//img/@src').extract_first()
        user_name = element.xpath('.//div[@class="moudle-user-name"]/a/text()').extract_first()
        user_url = element.xpath('.//div[@class="moudle-user-name"]/a/@href').extract_first()
        answer['answer_user'] = {'icon': user_icon, 'name':user_name, 'url':user_url}
        answer['likes_count'] = element.xpath('.//a[@class="moudle-right-list qa-icon qa-like mpniu"]/em/text()').extract_first()
        return answer

    def __del__(self):
        logging.info("stop page is %d" % self.current_page_number)

        
        
