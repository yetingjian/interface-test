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
    u"""Home_Wakeup设置后不保存"""
    def Home_Wakeup_SetUnsaved(self):
        Time(1)
        self.driver.find_element('name', 'WAKE UP').click()
        sleep(3)
        # 进入setup选择列表
        self.driver.find_element('id', 'com.ge.cbyge:id/act_scene_setup_start').click()
        sleep(3)
        self.assertEqual(self.driver.find_element('name', 'Cancel').text, 'Cancel', 'WakeUp创建页面没有返回功能')
        self.assertEqual(self.driver.find_element('name', 'Next').text, 'Next', 'WakeUp创建页面没有下一步功能')
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text, 'Setup (1 of 2)',
                         'WakeUp创建页面步骤一显示错误')
        t = len(self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item_left_image'))
        # print t
        if(t>1):
            for i in range(0,t):
                self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item_left_image')[i].click()
                # print i
                sleep(2)
            self.driver.find_element('name', 'Next').click()
            sleep(3)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text,'Setup (2 of 2)','步骤2页面跳转失败')
            sleep(3)
            # 编辑功能验证
            self.driver.find_element('id', 'com.ge.cbyge:id/view_scene_edit_start').click()
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text, 'Setup (1 of 2)',
                             'edit编辑失败')
            sleep(3)
            self.driver.find_element('name', 'Cancel').click()
            sleep(3)
            self.assertEqual(self.driver.find_elements('id', 'com.ge.cbyge:id/textview')[0].text, 'Home',
                             'WakeUp编辑取消失败')
        else:
            print u"没有在线的灯"
