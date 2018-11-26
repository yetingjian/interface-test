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

class ContactsAndroidTests(ContactsAndroid):
    u"""Schedule Details界面-schedule详情页面"""
    def Schedules_details(self):
        Time()
        self.driver.find_element('name', 'Schedules').click()
        sleep(3)
        list = self.driver.find_elements('id', 'com.ge.cbyge:id/view_smart_ctrl_item_text')
        list_Schedule = len(list)
        if(list_Schedule > 0):
            print u"存在Schedule"
            name = list[0].text
            list[0].click()
            sleep(2)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text,name,'名称显示错误')
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/detail_smart_enable_text').text, 'Enabled?', '详情显示错误')
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/turn_on_tv').text,
                             'TURN ON', '详情显示错误')
        else:
            print u"不存在Schedule"