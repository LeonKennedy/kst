#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @Filename: items.py
# @Author: olenji - lionhe0119@hotmail.com
# @Description: ---
# @Create: 2017-04-21 09:34:54
# @Last Modified: 2017-04-21 09:34:54
#


import time, logging, pdb, os, signal, traceback, pymysql
from pyvirtualdisplay import Display
from mysql import MysqlTool
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException       
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


logging.basicConfig(level=logging.INFO,filename='crawl.log',filemode='w')
class TaobaoItem:


    #终止flag
    end_item = None
    def __init__(self):
        self.connect = pymysql.connect(host='localhost',user = 'kst',password='kst410',
                db='kst', charset='utf8mb4')
        self.cur_q = self.connect.cursor()
        self.cur_update = self.connect.cursor()
        self.display = Display(visible=0, size=(1024, 768))
        self.display.start()
        self.driver = webdriver.Firefox()
        self.mt = MysqlTool()

    def getCategoryUrlFromDB(self):
        sql = "select * from taobao_category where cat is not null and stat = 'raw' limit 100 "
        self.cur_q.execute(sql)
        categorys = self.cur_q.fetchall()
        self.cur_q.close()
        for cid,_,_,cat,_,stat, offset in categorys:
            url = "https://s.taobao.com/list?cat=%s" % cat
            self.startPages(url, cid, offset)
            if self.recordEndCategory(cid):
                logging.info("=======Finish %d======" %cid)
            else:
                logging.info("=======wrong %d ======" %cid)
            self.driverRefresh()


    def driverRefresh(self):
        self.driver.quit()
        self.driver = webdriver.Firefox()

    def startPages(self,url, cid, offset):
        flag = True
        while flag:
            pageurl = url + '&s='  
            flag = self.startItems(pageurl + str(offset), cid)
            self.mt.flush()
            self.updateOffset(cid, offset)
            offset += 60


    def startItems(self, url, cid):
        #打开网址
        logging.info(url)
        self.driver.get(url)
        time.sleep(1)
        #点击排序
        try:
            tab = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH,'//div[@class="items"]')))
        except TimeoutException:
            print("maybe end of %s" % url)
            return False
        for i in tab.find_elements_by_xpath('div[@data-index]'):
            item = self.parse_item(i)
            item['category_id'] = cid

            self.mt.uniqueInsertByDict('taobao_items', item, 'item_id')
        return True

    def parse_item(self, element):
        element_info = element.find_element_by_xpath('./div[@class="ctx-box J_MouseEneterLeave J_IconMoreNew"]')
        item = dict()
        item['price'] = element_info.find_element_by_xpath('div[1]//strong').text
        item['paytimes'] = element_info.find_element_by_xpath('div[1]/div[@class="deal-cnt"]').text
        content = element_info.find_element_by_xpath('div[2]/a').text
        item['content'] = content.replace('"','\\"')
        item['item_id'] = element_info.find_element_by_xpath('div[2]/a').get_attribute('data-nid')
        item['url'] = element_info.find_element_by_xpath('div[2]/a').get_attribute('href')
        item['location'] = element_info.find_element_by_xpath('div[3]/div[@class="location"]').text
        #这里加载很慢 需要等待
        try:
            element_shop = WebDriverWait(element_info, 5).until(EC.presence_of_element_located((By.XPATH,'div[3]/div[@class="shop"]/a')))
            item['shop_id'] = element_shop.get_attribute('data-userid')
            item['shop_name'] = element_shop.text
        except TimeoutException:
            return item
        return item

    
    def updateOffset(self, cid, offset):
        sql = "update taobao_category set offset = %d where id = %d" % (offset, cid)
        return self.baseUpdate(sql)

    def recordEndCategory(self, cid):
        sql = "update taobao_category set stat = 'finish' where id = %d" % cid
        if self.cur_update.execute(sql):
            self.connect.commit()
            return True
        else:
            return False

    def baseUpdate(self, sql):
        self.cur_update.execute(sql)
        self.connect.commit()
        return True

    def __del__(self):
        self.driver.quit()
        self.display.stop()
        self.cur_update.close()
        self.connect.commit()
        self.connect.close()
   
    def test(self,url):
        self.driver.get(url)
        time.sleep(1)
        self.driver.quit()
        self.driver.get(url)


if __name__ == "__main__":
    t = TaobaoItem()
    url="https://www.taobao.com/market/nvzhuang/yurong.php"
    t.getCategoryUrlFromDB()
    #t.test(url)

