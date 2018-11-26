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
    u"""Schedule Details界面-新建schedule"""
    def Schedules_AddNewSchedule_Scene(self):
        Time(1)
        self.driver.find_element('name', 'Schedules').click()
        sleep(3)
        try:
            self.assertIsNotNone(self.driver.find_element('name', 'Add New Schedule').text, '没有添加灯按钮')
            sleep(3)
        except:
            self.find_by_scroll('Add New Schedule')
            sleep(3)
        self.driver.find_element('name', 'Add New Schedule').click()
        sleep(3)
        self.driver.find_element('id', 'com.ge.cbyge:id/add_smart_control_name').send_keys(u"GROUP2")
        name = self.driver.find_element('id', 'com.ge.cbyge:id/add_smart_control_name').text
        sleep(3)
        On_text = self.driver.find_element('id', 'com.ge.cbyge:id/turn_on_time').text
        # 点击SCENE
        self.driver.find_element('id', 'com.ge.cbyge:id/tv_scene').click()
        sleep(2)
        Trigger_text = self.driver.find_element('id', 'com.ge.cbyge:id/add_smart_control_time').text
        self.assertEqual(Trigger_text, On_text, '切换SCENE后时间不一致')
        try:
            self.assertIsNotNone(self.driver.find_element('name', 'Select Scene').text, '没有添加场景按钮')
            sleep(3)
        except:
            self.find_by_scroll('Select Scene')
            sleep(3)
        self.driver.find_element('name', 'Select Scene').click()
        sleep(3)
        self.driver.find_elements('id', 'com.ge.cbyge:id/item_select_child_checkBox')[0].click()
        sleep(2)
        self.driver.find_element('name', 'Done').click()
        sleep(3)
        self.assertIsNotNone(self.driver.find_element('id', 'com.ge.cbyge:id/add_smart_control_conflict_layout'),
                             'Scene保存失败')
        self.assertIsNotNone(self.driver.find_element('name', 'Change Scene'), 'Scene保存按钮显示错误')