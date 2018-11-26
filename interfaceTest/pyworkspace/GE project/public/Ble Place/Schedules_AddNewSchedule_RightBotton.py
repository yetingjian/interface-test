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
    u"""Schedules-进入Add New Schedule界面"""
    def Schedules_AddNewSchedule_RightBotton(self):
        Time(1)
        self.driver.find_element('name', 'Schedules').click()
        sleep(3)
        try:
            self.assertIsNotNone(self.driver.find_element('name', 'Add New Schedule').text, '没有添加灯按钮')
            sleep(3)
        except:
            #滑动到Add New Schedule按钮
            self.find_by_scroll('Add New Schedule')
            sleep(3)
        self.driver.find_element('id', 'com.ge.cbyge:id/id_3').click()
        sleep(3)
        self.driver.switch_to_alert()
        # 点击Add New Schedule按钮
        self.swipelocation(1, 0.40, 0.92, 0.50, 0.93)
        sleep(3)
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/add_smart_control_name_tv').text,'NAME','Schedule详情页面显示错误')
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/schedule_target_tv').text, 'SCHEDULING TARGET',
                         'Schedule详情页面显示错误')
        self.assertIsNotNone(self.driver.find_element('name', 'GROUP'), 'Schedule详情页面显示错误')
        self.assertIsNotNone(self.driver.find_element('name', 'SCENE'), 'Schedule详情页面显示错误')
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/turn_on_time').text, '8:00 AM',
                         'Schedule详情页面显示错误')
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/turn_off_time').text, '9:00 AM',
                         'Schedule详情页面显示错误')
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/repeate_value').text, 'Never',
                         'Schedule详情页面显示错误')
        self.assertIsNotNone(self.driver.find_element('name', 'Select Groups'),'Schedule详情页面显示错误')
        self.driver.find_element('name', 'Save').click()
        sleep(3)
        self.assertIsNotNone(self.driver.find_element('name', 'New Schedule'), '不输入信息点击保存失败')