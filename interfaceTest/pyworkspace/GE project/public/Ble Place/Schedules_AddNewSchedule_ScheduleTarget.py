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
    u"""Schedules-add new schedule（scene）-1、切换Schedule Target，2、设置REPEATS ON"""
    def Schedules_AddNewSchedule_ScheduleTarget(self):
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
        # 点击GROUP，验证GROUP内容
        self.driver.find_element('id', 'com.ge.cbyge:id/tv_group').click()
        sleep(2)
        self.assertIsNotNone(self.driver.find_element('id', 'com.ge.cbyge:id/schedule_tv'), 'ScheduleTarget_GROUP显示错误')
        self.assertIsNotNone(self.driver.find_element('id', 'com.ge.cbyge:id/turn_on_tv'), 'ScheduleTarget_GROUP显示错误')
        self.assertIsNotNone(self.driver.find_element('id', 'com.ge.cbyge:id/turn_off_tv'), 'ScheduleTarget_GROUP显示错误')
        # 点击SCENE，验证SCENE内容
        self.driver.find_element('id', 'com.ge.cbyge:id/tv_scene').click()
        sleep(2)
        self.assertIsNotNone(self.driver.find_element('id', 'com.ge.cbyge:id/add_smart_control_time_text'),
                             'ScheduleTarget_GROUP显示错误')
        # 设置REPEATS ON
        try:
            self.assertIsNotNone(self.driver.find_element('name', 'SCENE'), '有分组')
            sleep(3)
        except:
            # self.find_by_scroll('GROUPS')
            self.swipeUp(1000, 0.5, 0.9, 0.4)
            sleep(3)
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/repeate_value').text, 'Never', '为空显示错误')
        # 选择单个星期
        self.driver.find_element('id', 'com.ge.cbyge:id/week_sunday').click()
        sleep(2)
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/repeate_value').text, ' Sun', '单天选择错误')
        # 选择整个星期
        self.driver.find_element('id', 'com.ge.cbyge:id/week_monday').click()
        sleep(2)
        self.driver.find_element('id', 'com.ge.cbyge:id/week_tuesday').click()
        sleep(2)
        self.driver.find_element('id', 'com.ge.cbyge:id/week_wednesday').click()
        sleep(2)
        self.driver.find_element('id', 'com.ge.cbyge:id/week_thursday').click()
        sleep(2)
        self.driver.find_element('id', 'com.ge.cbyge:id/week_friday').click()
        sleep(2)
        self.driver.find_element('id', 'com.ge.cbyge:id/week_saturday').click()
        sleep(2)
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/repeate_value').text, 'Everyday', '整个星期选择错误')