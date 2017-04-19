#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @Filename: kst.py
# @Author: olenji - lionhe0119@hotmail.com
# @Description:  产品需求
#                根据淘宝用户ID搜索用户相关店铺 包括主营 销量 产品数
# @Create: 2017-04-14 11:21:13
# @Last Modified: 2017-04-14 11:21:13

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from pyvirtualdisplay import Display

class TaoBao:

    binary = FirefoxBinary('/home/olenji/bin/geckodriver')

    def __init__(self):
        pass

    def setUp(self):
        self.selenium = selenium()
    def getInfo(self):
        display = Display(visible=0, size=(1024, 768))
        display.start()
        driver = webdriver.Firefox(firefox_binary=self.binary)
        driver.get("https://s.taobao.com/search/?")
        time.sleep(1)
        print(dir(driver))
        driver.close()
        display.stop()
        pass

    def __del__(self):
        pass

if __name__ == "__main__":
    t = TaoBao()
    t.getInfo()
