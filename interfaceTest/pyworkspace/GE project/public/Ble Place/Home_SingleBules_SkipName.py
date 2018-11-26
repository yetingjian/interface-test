#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import unittest
from appium import webdriver
from time import sleep
import re
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
sys.path.append("C:\Users\Demon\Desktop\GE project\public")
from Start import ContactsAndroid
from TimeOut import Time

def Home_SingleBules_SkipName(self):
    u"""添加灯，点击log连接返回Home页面"""
    Time(1)
    try:
        self.assertIsNone(self.driver.find_element('name', 'Add a bulb').text, '没有添加灯按钮')
        self.driver.find_element('name', 'Add a bulb').click()
        sleep(3)
    except:
        self.swipeUp(1000, 0.8, 0.8, 0.2)
        sleep(3)
        self.driver.find_element('name', 'Add a bulb').click()
        sleep(3)
    self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item')[0].click()
    sleep(15)
    if (self.driver.find_element('id', 'com.ge.cbyge:id/act_guide_pager_tv').text == 'Looking for bulbs...'):
        print u"不存在未分组的bulbs灯"
    elif (
                self.driver.find_element('id', 'com.ge.cbyge:id/act_guide_pager_tv').text.find(
                    'bulbs found...') >= 0):
        print u"存在未分组的bulbs灯"
        self.driver.find_element('name', 'Next').click()
        sleep(3)
        self.driver.find_element('id', 'com.ge.cbyge:id/view_guide_found_new_name').click()
        sleep(3)
        self.driver.find_element('id', 'com.ge.cbyge:id/tv_login').click()
        sleep(3)
        self.assertEqual(self.driver.find_elements('id', 'com.ge.cbyge:id/textview')[0].text, 'Home',
                         'log跳出检查失败')

