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
    u"""分享"""
    def Home_ShareControl(self):
        Time(1)
        # TimeOut.Time(1)
        self.swipelocation(1, 0.88, 0.06, 0.98, 0.09)
        sleep(3)
        #定位到弹出框
        self.driver.switch_to_alert()
        #点击share control
        self.swipelocation(1, 0.10, 0.79, 0.30, 0.81)
        sleep(3)
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text,'Share Control','分享页面进入失败')
        self.driver.find_element('id', 'com.ge.cbyge:id/fgt_share_with_to_edittext').send_keys(u"cxj616@qq.com")
        sleep(3)
        self.driver.find_element('name', 'Send').click()
        sleep(3)
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/fgt_share_done_text').text, 'Done', '分享失败')
        self.driver.find_element('id', 'com.ge.cbyge:id/activity_group_delete_sure').click()
        sleep(3)
        self.assertEqual(self.driver.find_elements('id', 'com.ge.cbyge:id/textview')[0].text, 'Home', '分享成功，页面跳转错误')
