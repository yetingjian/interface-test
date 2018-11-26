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
    u"""Scenes界面-删除情景"""
    def Scenes_Delete(self):
        Time(1)
        self.driver.find_element('name', 'Scenes').click()
        sleep(3)
        list = self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item_text')
        # 计算列表长度
        l = len(list)
        if (l > 4):
            # 点击最后一个场景，打开场景详情
            self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item_right_image')[l - 1].click()
            sleep(3)
            name = self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text
            self.driver.find_element('id', 'com.ge.cbyge:id/id_3').click()
            sleep(3)
            self.driver.switch_to_alert()
            #点击删除按钮
            self.swipelocation(1,0.40,0.92,0.50,0.93)
            sleep(3)
            #断言标题是否存在
            self.assertIsNotNone(self.driver.find_element('name', 'Delete Scene').text,'删除功能失败')
            self.driver.find_element('id', 'com.ge.cbyge:id/activity_group_delete_sure').click()
            sleep(3)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text,'Scenes ','删除后返回页面跳转错误')
            a = []
            list1 = self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item_text')
            l2 = len(list1)
            for i in range(0,l2):
                a.append(list1[i].text)
            flag = True
            if (name not in a):
                return flag
            else:
                flag = False
                return flag
            self.assertTrue(flag, '场景删除失败')
        else:
            print u"不存在可编辑的分组"