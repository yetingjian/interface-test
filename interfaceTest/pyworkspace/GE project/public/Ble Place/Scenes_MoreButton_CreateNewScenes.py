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
    u"""Scenes界面-Create New Scene选项"""
    def Scenes_MoreButton_CreateNewScenes(self):
        Time(1)
        self.driver.find_element('name', 'Scenes').click()
        sleep(3)
        self.driver.find_element('id', 'com.ge.cbyge:id/id_3').click()
        sleep(3)
        self.driver.switch_to_alert()
        #点击Create New Scenes
        self.swipelocation(1, 0.40, 0.87, 0.50, 0.88)
        sleep(3)
        self.assertIsNotNone(self.driver.find_element('id', 'com.ge.cbyge:id/fg_new_scene_bulb_select_tips1').text,'创建新场景失败')
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/fg_new_scene_bulb_select_tips1').text,'Select the bulbs you want in this scene:','创建新场景失败')
