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
    u"""分组-mange-保存"""
    def Home_Groups_AddEqipment_Save(self):
        Time(1)
        l = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')
        k = len(l)
        sleep(3)
        for i in range(0,k):
            try:
                if(l[i].text == "Create new group"):
                    sleep(3)
                    if(i>1):
                        #打开第一个分组
                        name1 = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')[1].text
                        self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_right_image')[1].click()
                        sleep(3)
                        #滑动范围需要判断
                        self.swipeUp(1000, 0.8, 0.8, 0.2)
                        sleep(6)
                        list_G = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item')
                        list_N = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')
                        k_G = len(list_G)
                        #a数组保存起始时灯信息，b数组保存取消后灯信息
                        a = []
                        b = []
                        #获取初始时灯名称信息
                        for j in range(0,k_G):
                            #灯个数计算判断
                            try:
                                if(list_N[j].text == "Add bulbs to Group"):
                                    print j
                                    for r_G in range(0,j):
                                        c = list_N[r_G].text
                                        a.append(c)
                                        a.sort()
                                    print u"取消前列表信息为："
                                    print a
                            except:
                                j = j + 1
                                continue
                        self.driver.find_element('id', 'com.ge.cbyge:id/id_3').click()
                        sleep(3)
                        self.driver.switch_to_alert()
                        #点击Manage bulbs in Group按钮
                        self.swipelocation(1,0.40,0.80,0.50,0.81)
                        sleep(3)
                        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text,'Select Group Bulbs','Manage bulbs in Group功能操作失败')
                        self.driver.find_element('name', 'Save').click()
                        sleep(3)
                        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text, name1,
                                         '不做修改保存失败')
                        #取消后重新检查列表数据，统计写入b列表
                        list_G1 = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item')
                        k_G1 = len(list_G1)
                        print k_G1
                        for j1 in range(0,k_G1):
                            try:
                                if (list_N[j1].text == "Add bulbs to Group"):
                                    print j1
                                    for r_G1 in range(0, j1):
                                        d = list_N[r_G1].text
                                        b.append(d)
                                        b.sort()
                                    print u"取消后列表信息为："
                                    print b
                            except:
                                j1 = j1 + 1
                                continue
                        #验证取消后是否相等
                        if(a==b):
                            print u"Save成功"
                        else:
                            print u"Save失败"
                    else:
                        print u"没有分组信息"
                        break
            except:
                i = i +1
                continue
