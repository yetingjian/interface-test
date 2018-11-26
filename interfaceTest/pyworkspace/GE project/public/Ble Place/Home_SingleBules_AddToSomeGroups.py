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

def Home_SingleBules_AddToSomeGroups(self):
    u"""添加多个灯到多个分组"""
    Time(1)
    try:
        self.assertIsNone(self.driver.find_element('name', 'Add a bulb').text, '没有添加灯按钮')
        self.driver.find_element('name', 'Add a bulb').click()
        sleep(3)
    except:
        self.swipeUp(1000, 0.8, 0.8, 0.2)
        sleep(3)
        self.driver.find_element('name', 'Add a bulb').click()
        sleep(3)
    self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item')[0].click()
    sleep(15)
    if (self.driver.find_element('id', 'com.ge.cbyge:id/act_guide_pager_tv').text == 'Looking for bulbs...'):
        print u"不存在未分组的bulbs灯"
    elif (
                self.driver.find_element('id', 'com.ge.cbyge:id/act_guide_pager_tv').text.find('bulbs found...') >= 0):
        print u"存在未分组的bulbs灯"
        self.driver.find_element('name', 'Next').click()
        sleep(3)
        # 从加灯首页获取灯个数
        num_name = self.driver.find_element('id', 'com.ge.cbyge:id/tv_found_bulbs_qty').text
        num_name2 = num_name.encode('gbk')
        num1 = filter(str.isdigit, num_name2)
        num = int(num1)
        # 点击Name your bulbs
        self.driver.find_element('id', 'com.ge.cbyge:id/view_guide_found_new_name').click()
        sleep(3)
        # 添加多个灯进行添加分组判断
        for j in range(0, num):
            self.driver.find_element('id', 'com.ge.cbyge:id/view_bulb_edit_add').click()
            # list是列表名称，botton是勾选按钮
            list = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')
            button = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_left_image')
            l = len(list)
            a = []
            sleep(3)
            if (l >= 2):
                # 保存所添加到的分组名称，用于检测分组中是否有灯信息
                for i in range(0, l):
                    if (i > 8):
                        print u"超出设定值3"
                        break
                    else:
                        button[i].click()
                        sleep(2)
                        a.append(list[i].text)
                # print a
                self.driver.find_element('name', 'Save').click()
                sleep(3)
                self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/tv_login').text,
                                 'Skip naming your bulbs', '添加多分组保存失败')
                self.driver.find_element('name', 'Next').click()
                sleep(3)
            else:
                print u"不能添加多个分组"
