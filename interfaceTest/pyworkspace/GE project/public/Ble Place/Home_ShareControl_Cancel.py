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
    u"""取消分享"""
    def Home_ShareControl_Cancel(self):
        Time(1)
        # 点击home页面右上角功能按钮
        self.swipelocation(1, 0.88, 0.06, 0.98, 0.09)
        sleep(3)
        self.driver.switch_to_alert()
        # 点击退出按钮
        self.swipelocation(1, 0.10, 0.97, 0.30, 0.98)
        sleep(3)
        self.driver.find_element('id', 'com.ge.cbyge:id/id_2').click()
        sleep(3)
        self.assertEqual(self.driver.find_elements('id', 'com.ge.cbyge:id/textview')[0].text, 'Home', '取消失败')
