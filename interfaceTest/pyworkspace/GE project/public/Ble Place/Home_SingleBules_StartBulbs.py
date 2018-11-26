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
    u"""添加灯直接使用灯"""
    def Home_SingleBules_StartBulbs(self):
        Time(1)
        # AddBulb_Opinion(1)
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
        # try:
        #     self.assertIsNone(self.driver.find_element('id', 'com.ge.cbyge:id/bt_no_find_bulbs_try_conncet'), '没有添加灯按钮')
        #     print u"没有可添加的Sleep或life灯"
        # except:
        if (self.driver.find_element('id', 'com.ge.cbyge:id/act_guide_pager_tv').text == 'Looking for bulbs...'):
            print u"不存在未分组的bulbs灯"
        elif (
            self.driver.find_element('id', 'com.ge.cbyge:id/act_guide_pager_tv').text.find('bulbs found...') >= 0):
            print u"存在未分组的bulbs灯"
            self.driver.find_element('name', 'Next').click()
            sleep(3)
            # 点击Start using your bulbs
            self.driver.find_element('id', 'com.ge.cbyge:id/view_guide_found_new_start').click()
            sleep(3)
            self.assertEqual(self.driver.find_element('name', 'Home').text,'Home','开始使用你的灯泡失败')