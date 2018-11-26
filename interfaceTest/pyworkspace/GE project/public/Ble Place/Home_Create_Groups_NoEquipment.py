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
    u"""创建无设备分组"""
    def Home_Create_Groups_NoEquipment(self):
        Time(1)
        self.driver.find_element('name', 'Create new group').click()
        sleep(3)
        self.driver.find_element('name', 'Next').click()
        sleep(3)
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/dialog_tips').text,
                         'Please select at least one light you want in this group!', '无设备添加分组提示错误')