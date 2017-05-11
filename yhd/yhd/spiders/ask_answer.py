# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy, logging, pdb
from yhd.items import QAItem
from scrapy.selector import Selector


class AskAnswerSpider(scrapy.Spider):
    name = "ask_answer"
    allowed_domains = ["www.yhd.com"]
    start_urls = ['http://www.yhd.com/marketing/QA/C0-P1.html']
    baseurl = 'http://www.yhd.com/marketing/QA/C0-P%d.html'
    #urlindex = 78190
    urlindex = 52000
    urlendindex = 78190

    def parse(self, response):
#        element_QAs = response.xpath('//div[@id="productQA"]/div[@class="question_list borderbottom_dotted"]').extract()
        while self.urlindex < self.urlendindex:
            url = self.baseurl % self.urlindex
            yield scrapy.Request(url=url, callback = self.parse_ask_answer)
            self.urlindex += 1
        '''
        url = self.baseurl % self.urlindex
        yield scrapy.Request(url=url, callback = self.parse_ask_answer)
        '''


    def parse_ask_answer(self, response):
        element_QAs = response.xpath('//div[@id="productQA"]/div[@class="question_list borderbottom_dotted"]')
        #问答凑成一对 生成一个item
        questionaswer_cp = dict()
        if not element_QAs:
            logging.info("Not found ask_answer : %s" % response.url)

        for element_qa in element_QAs:
            product = element_qa.xpath('span[@class="goodsname"]/a/text()').extract_first()
            user = element_qa.xpath('ul/li[3]/text()').extract_first().replace('\r\n','')
            tm = element_qa.xpath('ul/li[4]/text()').extract_first().replace('\r\n','')
            if product: 
                '''
                if questionaswer_cp:
                    logging.warn("cp has question when insert question")
                    questionaswer_cp = {}
                    continue
                '''
                questionaswer_cp['product'] = product.replace('\r\n','')
                questionaswer_cp['question'] = element_qa.xpath('ul/li[2]/span/a/text()').extract_first().replace('\r\n','')
                questionaswer_cp['question_user'] = user
                questionaswer_cp['question_tm'] = tm

            else:
                if not questionaswer_cp:
                    logging.warn("cp dont have question when insert answeer")
                    raise BaseException('aa')
                questionaswer_cp['answer'] = element_qa.xpath('ul/li[2]/span/text()').extract_first().replace('\r\n','')
                questionaswer_cp['answer_user'] = user
                questionaswer_cp['answer_tm'] = tm
                questionaswer_cp['url'] = response.url
                yield QAItem(questionaswer_cp)
                questionaswer_cp = {}





