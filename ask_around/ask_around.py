#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @Filename: ask_around.py
# @Author: olenji - lionhe0119@hotmail.com
# @Description: ---
# @Create: 2017-04-18 11:15:22
# @Last Modified: 2017-04-18 11:15:22
#


import time, logging, pdb, os, signal, traceback
from pyvirtualdisplay import Display
from selenium import webdriver
#from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException       
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logging.basicConfig(level=logging.DEBUG)


class TaoBao:


    #binary = FirefoxBinary('/root/bin/geckodriver')
    used_count = 0

    def __init__(self):
        self.display = Display(visible=0, size=(1024, 768))
        self.display.start()
        self.driver = webdriver.Firefox()
        pass

    def getInfo(self):
        driver = self.driver
        time.sleep(1)

    def getAskAroundByItemPage(self, url):
        self.used_count += 1
        driver = self.driver
        driver.get(url)
        bd = driver.find_element_by_id('bd')
        element_comment = bd.find_element_by_id('J_TabBar').find_element_by_xpath('.//li[2]')
        if element_comment.find_element_by_xpath('.//em[@class="J_ReviewsCount"]').text ==  '0':
            return None
        else:
            #点击评论
            element_comment.find_element_by_xpath('a').click()
            #点击大家说
            time.sleep(3)
            element_as = WebDriverWait(bd, 10).until(EC.presence_of_element_located((By.XPATH, './/div[@class="kg-rate"]/ul/li[3]')))
            #element_as = self.waitRender(driver.find_element_by_xpath, '//div[@class="kg-rate"]/ul/li[3]'
            element_as.click()
            #获取评论列表
            element_as_list = WebDriverWait(bd,6).until(EC.presence_of_element_located((By.XPATH, './/div[@class="J_KgRate_List_AskAround kg-rate-wd-ask-around-list"]')))
            WebDriverWait(element_as_list,6).until(EC.presence_of_element_located((By.XPATH, './/div[@class="kg-rate-ct-review-item"]')))
            #element_as_list = self.waitRender(bd.find_element_by_xpath, '//div[@class="J_KgRate_List_AskAround kg-rate-wd-ask-around-list"]')
            #element_one = self.waitRender(element_as_list.find_element_by_xpath, '//div[@class="kg-rate-ct-review-item"]')
            try:
                element_as_list.find_element_by_xpath('.//div[@class="kg-rate-ct-review-item"]')
            except:
                logging.debug("Not Found Ask Around Record!!!")
                return None

            #点击跟多
            self.clickMoreComment(element_as_list)

            #处理所有ask_around
            for element_askaround in element_as_list.find_elements_by_xpath('//div[@class="kg-rate-ct-review-item"]'):
                self.holdAskAround(element_askaround)
            #element_askaround = element_as_list.find_element_by_xpath('.//div[@class="kg-rate-ct-review-item"]')
            #print(self.holdAskAround(element_askaround))


    #点击更多
    def clickMoreComment(self, element):
        flag = True
        while flag:
            try:
                element_more = WebDriverWait(element, 5).until(EC.presence_of_element_located((By.XPATH, './/a[@class="J_KgRate_AskAround_MoreQuestions"]')))
                element_more.click()
                logging.debug("翻页, 当前有 %d 个" % len(element.find_elements_by_xpath('.//div[@class="kg-rate-ct-review-item"]')))
            except TimeoutException:
                logging.debug("当前有 %d 个" % len(element.find_elements_by_xpath('.//div[@class="kg-rate-ct-review-item"]')))
                return True
            except:
                traceback.print_exc()
                logging.warn("somthing wrong!!!!!!!!!!!!!!")
                return True
        return True

    #处理ask around单条
    def holdAskAround(self, element):
        result = dict()
        result['id'] = element.get_attribute('data-kg-rate-ask-around-id')
        result['ask_user_name'] = element.find_element_by_xpath('div[@class="from-whom"]/div').text
        #问题
        element_ask = element.find_element_by_xpath('.//div[@class="q-or-a q"]/div')
        result['ask_content'] = element_ask.find_element_by_xpath('div[@class="tb-tbcr-content heavier"]').text
        result['ask_tm'] = element_ask.find_element_by_xpath('//div[@class="info-part"]').text

        try:
            #是否有更多对话
            element.find_element_by_xpath('.//div[@class="q-or-a J_KgRate_AskAround_MoreAnswers more"]/span')
            self.clickMoreAnswer(element)
        except:
            #traceback.print_exc()
            pass
        #回答
        answer_list = list()
        for element_ans in element.find_elements_by_xpath('.//div[@class="q-or-a a"]/div'):
            ans = dict()
            ans['answer_content'] = element_ans.find_element_by_xpath('div[@class="tb-tbcr-content"]').text
            ans['answer_name'] = element_ans.find_element_by_xpath('div[2]/div[1]').text
            ans['answer_tm'] = element_ans.find_element_by_xpath('div[2]/div[2]').text
            answer_list.append(ans)

        result['answer'] = answer_list
        return result

    def clickMoreAnswer(self, element):
        element.find_element_by_xpath('.//div[@class="q-or-a J_KgRate_AskAround_MoreAnswers more"]/span').click()
        time.sleep(1)

    def waitRender(self,call, params, intertime = 3, times = 2):
        time.sleep(intertime)
        try:
            return call(params)
        except:
            time.sleep(intertime)
            return call(params)

    def __del__(self):
        #self.closeFirefox()
        logging.warn(self.driver.current_url)
        self.driver.quit()
        self.display.stop()
        logging.info("total used is %d", self.used_count) 

    #无用
    #用来关闭子进程
    def closeFirefox(self):
        pid = os.getpid()
        gecko_pid = None
        ps = os.popen("ps -ef ")
        for line in ps:
            fields = line.split()
            if str(pid)  == fields[2] and "geckodriver" in line:
                gecko_pid = fields[1]
                continue
            if gecko_pid and gecko_pid == fields[2]:
                os.kill(int(fields[1]), signal.SIGHUP)
                logging.info("kill firefox subprocess, pid is %s" % fields[1])
                return True
        return False



if __name__ == "__main__":
    t = TaoBao()
    #正常
    url = "https://item.taobao.com/item.htm?spm=a217f.1257546.1998139181.1000.n6IvEB&id=524277413474&scm=1029.minilist-17.1.50099260&ppath=&sku=&ug=#detail"
    #累计评论 0
    #url = "https://item.taobao.com/item.htm?spm=a217f.1257546.1998139181.518.KNFLNq&id=521371673727&scm=1029.minilist-17.1.50099260&ppath=&sku=&ug=#detail"
    t.getAskAroundByItemPage(url)

