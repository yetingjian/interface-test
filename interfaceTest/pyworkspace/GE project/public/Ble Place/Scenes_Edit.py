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
    u"""Scenes界面-编辑情景"""
    def Scenes_Edit(self):
        Time(1)
        self.driver.find_element('name', 'Scenes').click()
        sleep(3)
        list = self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item_text')
        # 计算列表长度
        l = len(list)
        # print l
        if (l > 4):
            # 点击最后一个场景，打开场景详情
            self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item_right_image')[l - 1].click()
            sleep(3)
            self.driver.find_element('id', 'com.ge.cbyge:id/act_scene_control_edit').click()
            sleep(3)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text,'Edit Scene','场景编辑失败')
        else:
            print u"不存在可编辑的分组"