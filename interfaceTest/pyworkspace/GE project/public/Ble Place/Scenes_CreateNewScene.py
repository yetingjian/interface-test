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
    u"""Scenes界面-创建新场景"""
    def Scenes_CreateNewScene(self):
        Time(1)
        self.driver.find_element('name', 'Scenes').click()
        sleep(3)
        try:
            self.assertIsNone(self.driver.find_element('name', 'Create New Scene').text, '没有添加场景按钮')
            sleep(3)
        except:
            self.swipeUp(1000, 0.8, 0.8, 0.2)
            sleep(3)
        self.driver.find_element('name', 'Create New Scene').click()
        sleep(3)
        list = self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item_text')
        l = len(list)
        if(l > 0):
            # print u"存在设备，可添加场景"
            list[0].click()
            sleep(2)
            self.driver.find_element('name', 'Next').click()
            sleep(3)
            self.driver.find_element('id', 'com.ge.cbyge:id/fg_scene_name_edittext').send_keys(u"场景添加")
            name = self.driver.find_element('id', 'com.ge.cbyge:id/fg_scene_name_edittext').text
            sleep(3)
            self.driver.find_element('name', 'Next').click()
            sleep(3)
            #场景名称重复判断
            try:
                self.assertIsNotNone(self.driver.find_element('id', 'com.ge.cbyge:id/dialog_tips'),'重复名称场景添加成功')
                print u"存在重复名称分组"
                self.driver.find_element('id', 'com.ge.cbyge:id/dialog_btn').click()
                sleep(3)
            except:
                self.driver.find_element('name', 'Save').click()
                sleep(3)
                l1 = len(list)
                a = []
                for i in range(0,l1):
                    a.append(list[i].text)
                    flag = True
                    if (name in a):
                        return flag
                    else:
                        flag = False
                        return flag
                    self.assertTrue(flag, 'Scene添加失败')
        else:
            print u"没有设备进行自定义场景添加"
