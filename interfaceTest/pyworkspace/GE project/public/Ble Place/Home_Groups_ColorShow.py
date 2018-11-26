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
    u"""分组组控color显示"""
    def Home_Groups_ColorShow(self):
        Time(1)
        l = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')
        k = len(l)
        print k
        sleep(3)
        for i in range(0,k):
            try:
                if(l[i].text == "Create new group"):
                    print i
                    sleep(3)
                    if(i>1):
                        #打开第一个分组
                        self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_right_image')[1].click()
                        sleep(3)
                        self.swipeUp(1000,0.8,0.8,0.2)
                        sleep(3)
                        list = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')
                        p = len(list)
                        print p
                        #定义空数组b，用来存储灯类型
                        b = []
                        for j in range(0,p):
                            #灯个数计算判断
                            try:
                                if(list[j].text == "Add bulbs to Group"):
                                    print j
                                    sleep(3)
                                    for r in range(0,j):
                                        self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_right_image')[r].click()
                                        sleep(3)
                                        self.assertEqual(self.driver.find_element('id',
                                                                                  'com.ge.cbyge:id/seekbar_light_lum_text').text,
                                                         'BRIGHTNESS', '灯详情查看失败')
                                        a = self.driver.find_element('id', 'com.ge.cbyge:id/bulb_type_text').text
                                        #将灯类型存入数组b中保存
                                        b.append(a)
                                        self.driver.find_element('id', 'com.ge.cbyge:id/id_2').click()
                                        sleep(3)
                                    print b
                                    #只有life灯判断
                                    if('C-Sleep' not in b and 'BR30' not in b):
                                        # print u"ax"
                                        # try:
                                        #     self.assertIsNone(self.driver.find_element('id', 'com.ge.cbyge:id/act_group_detail_titleimage'))
                                        #     self.swipeDown(1000,0.8,0.2,0.8)
                                        #     sleep(3)
                                        #     self.assertEqual(self.driver.find_element('id',
                                        #                                               'com.ge.cbyge:id/act_group_detail_brightness').text,
                                        #                      'BRIGHTNESS', '等控制查看失败')
                                        #     self.assertIsNotNone(self.driver.find_element('name', 'C-SLEEP COLOR'))
                                        # except:
                                        self.swipeDown(1000, 0.8, 0.2, 0.8)
                                        self.assertEqual(self.driver.find_element('id',
                                                                                  'com.ge.cbyge:id/act_group_detail_brightness').text,
                                                         'BRIGHTNESS', '灯控制查看失败')
                                        self.assertIsNotNone(self.driver.find_element('name', 'C-SLEEP COLOR'))
                                        self.assertIsNotNone(self.driver.find_element('name', 'BR30 COLOR'))
                                    #存在sleep，不存在BR30判断
                                    elif('C-Sleep' in b and 'BR30' not in b):
                                        # print u"bx"
                                        self.swipeDown(1000, 0.8, 0.2, 0.8)
                                        self.assertEqual(self.driver.find_element('id',
                                                                                  'com.ge.cbyge:id/act_group_detail_brightness').text,
                                                         'BRIGHTNESS', '灯控制查看失败')
                                        self.assertIsNotNone(self.driver.find_element('name', 'C-SLEEP COLOR'))
                                        self.assertIsNone(self.driver.find_element('name', 'BR30 COLOR'))
                                    #存在br30，不存在sleep判断
                                    elif('C-Sleep' not in b and 'BR30' in b):
                                        # print u"cx"
                                        self.swipeDown(1000, 0.8, 0.2, 0.8)
                                        self.assertEqual(self.driver.find_element('id',
                                                                                  'com.ge.cbyge:id/act_group_detail_brightness').text,
                                                         'BRIGHTNESS', '灯控制查看失败')
                                        self.assertIsNone(self.driver.find_element('name', 'C-SLEEP COLOR'))
                                        self.assertIsNotNone(self.driver.find_element('name', 'BR30 COLOR'))
                                    #存在br30，sleep，或life判断
                                    elif('C-Sleep' in b and 'BR30' in b):
                                        # print u"dx"
                                        self.swipeDown(1000, 0.8, 0.2, 0.8)
                                        self.assertEqual(self.driver.find_element('id',
                                                                                  'com.ge.cbyge:id/act_group_detail_brightness').text,
                                                         'BRIGHTNESS', '灯控制查看失败')
                                        self.assertIsNotNone(self.driver.find_element('name', 'C-SLEEP COLOR'))
                                        self.assertIsNotNone(self.driver.find_element('name', 'BR30 COLOR'))
                            except:
                                j = j + 1
                                continue
                    else:
                        print u"没有分组信息"
                        break
            except:
                i = i +1
                continue
