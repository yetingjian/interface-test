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


def Home_SingleBules_BuleInformationAddGroups(self):
    u"""将灯同时加入多个分组"""
    Time(1)
    try:
        self.assertIsNone(self.driver.find_element('name', 'Add a bulb').text, '没有添加灯按钮')
        sleep(3)
    except:
        self.swipeUp(1000, 0.8, 0.8, 0.2)
        sleep(3)
    list = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')
    l = len(list)
    a = []
    b = []
    # 查找SINGLE BULBS位置
    for i in range(0, l):
        if (list[i].text == 'SINGLE BULBS'):
            a.append(i)
        else:
            i = i + 1
    # 查找Add a bulb位置
    for j in range(0, l):
        if (list[j].text == 'Add a bulb'):
            b.append(j)
        else:
            j = j + 1
    # k计算是否有单灯在SINGLE BULBS中
    k = b[0] - a[0]
    c = b[0] - 1
    if (k > 0):
        print u"存在灯"
        self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_right_image')[c].click()
        sleep(3)
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/seekbar_light_lum_text').text,
                         'BRIGHTNESS', '单灯详情查看失败')
        name = self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text
        self.driver.find_element('id', 'com.ge.cbyge:id/id_3').click()
        sleep(3)
        self.driver.switch_to_alert()
        # 点击Edit Bulb Name按钮
        self.swipelocation(1, 0.40, 0.80, 0.50, 0.81)
        sleep(3)
        # 计算Group列表长度
        list = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')
        l = len(list)
        d = []
        if (l > 1):
            for w in range(0, l):
                self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_left_image')[w].click()
                d.append(list[w].text)
                # list_name = list[0].text
                sleep(3)
            self.driver.find_element('name', 'Save').click()
            sleep(3)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/seekbar_light_lum_text').text,
                             'BRIGHTNESS', '添加分组保存失败')
            self.driver.find_element('id', 'com.ge.cbyge:id/id_2').click()
            sleep(3)
        else:
            print u"没有多个分组添加可以添加设备"
    elif (k <= 0):
        print u"不存在灯"