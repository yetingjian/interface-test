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
    u"""Enable OR Disable Schedule-Enable Schedule"""
    def Schedules_details(self):
        Time()
        self.driver.find_element('name', 'Schedules').click()
        sleep(3)
        list = self.driver.find_elements('id', 'com.ge.cbyge:id/view_smart_ctrl_item_text')
        list_Schedule = len(list)
        if (list_Schedule > 0):
            print u"存在Schedule"
            list[0].click()
            sleep(2)
            # 点击Enabled按钮
            self.driver.find_element('id', 'com.ge.cbyge:id/detail_smart_control_checkBox').click()
            sleep(1)
            try:
                self.assertIsNotNone(self.driver.find_element('id', 'com.ge.cbyge:id/tv_deleting'), 'enable失败')
                self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/tv_deleting').text,
                                 'Enabling Schedule...', 'enable提示信息错误')
                print u"enable成功"
            except:
                self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/tv_deleting').text,
                                 'Disabling Schedule...', 'disable提示信息错误')
                self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/tv_deleting').text,
                                 'Disabling Schedule...', 'disable提示信息错误')
                print u"disable成功"
                sleep(5)
                list[0].click()
                sleep(2)
                self.driver.find_element('id', 'com.ge.cbyge:id/detail_smart_control_checkBox').click()
                sleep(1)
                self.assertIsNotNone(self.driver.find_element('id', 'com.ge.cbyge:id/tv_deleting'), 'enable失败')
                self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/tv_deleting').text,
                                 'Enabling Schedule...', 'enable提示信息错误')
                print u"disable转enable成功"
            sleep(5)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text, 'Schedules ',
                             '返回页面错误')
        else:
            print u"不存在Schedule"