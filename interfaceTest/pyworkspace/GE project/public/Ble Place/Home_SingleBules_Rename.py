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
    u"""添加灯重新命名"""
    def Home_SingleBules_Rename(self):
        Time(1)
        # AddBulb_Opinion(1)
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
            # 点击Name your bulbs
            self.driver.find_element('id', 'com.ge.cbyge:id/view_guide_found_new_name').click()
            sleep(3)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/tv_login').text,'Skip naming your bulbs','灯重命名页面进入失败')
            self.driver.find_element('id', 'com.ge.cbyge:id/view_bulb_edit_name').click()
            sleep(3)
            self.driver.find_element('id', 'com.ge.cbyge:id/view_new_bulb_et').send_keys(u"重命名灯")
            rename = self.driver.find_element('id', 'com.ge.cbyge:id/view_new_bulb_et').text
            sleep(3)
            self.driver.find_element('name', 'Save').click()
            sleep(3)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/tv_login').text, 'Skip naming your bulbs',
                             '灯重命名保存失败')
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/view_bulb_edit_tv').text,rename,'灯重命名保存失败')
            #添加分组
            self.driver.find_element('id', 'com.ge.cbyge:id/view_bulb_edit_add').click()
            sleep(3)
            try:
                self.driver.find_element('id', 'com.ge.cbyge:id/view_new_group_first_tips1').text.find(
                    'to the following groups:') >= 0
                # 有分组,添加到第一个分组中
                self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_left_image')[0].click()
                GroupName = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')[0].text
                # print GroupName
                sleep(3)
                self.driver.find_element('name', 'Save').click()
                sleep(3)
                self.driver.find_element('name', 'Next').click()
                sleep(3)
                #查找分组，验证灯是否存在
                l = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')
                k = len(l)
                print k
                #a数组用来保存home页面分组名称
                a = []
                for i in range(0, k):
                    # print l[i].text
                    a.append(l[i].text)
                print a
                sleep(2)
                for j in range(0,k):
                    if(a[j] == GroupName):
                        sleep(3)
                        # print a[j]
                        # print j
                        self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_right_image')[j].click()
                        sleep(3)
                        #判断是否需要滑动
                        try:
                            self.assertIsNone(self.driver.find_element('name', 'Add bulbs to Group').text,
                                              '有添加灯按钮')
                        except:
                            self.swipeUp(1000, 0.8, 0.8, 0.2)
                            sleep(3)
                        Grpupslist = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item')
                        GrpupslistName = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')
                        #list是分组中灯列表长度
                        list = len(Grpupslist)
                        b = []
                        for r in range(0, list):
                            b.append(GrpupslistName[r].text)
                        print b
                        if (rename in b):
                            print u"增加灯进分组成功"
                        else:
                            print u"增加灯进分组失败"
                    else:
                        j = j + 1
            except:
                self.driver.find_element('id', 'com.ge.cbyge:id/act_bulb_to_group_name_tips1').text.find(
                    "Let's create a group.") >= 0
                #测试用例：新灯设置-将灯加入新分组
                self.driver.find_element('id', 'com.ge.cbyge:id/act_bulb_to_group_name_edittext').send_keys(u"加灯新增分组")
                name = self.driver.find_element('id', 'com.ge.cbyge:id/act_bulb_to_group_name_edittext').text
                print name
                sleep(3)
                self.driver.find_element('name', 'Save').click()
                sleep(3)
                self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_left_image')[0].click()
                name_group = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')[0].text
                print name_group
                sleep(3)
                self.driver.find_element('name', 'Save').click()
                sleep(3)
                self.driver.find_element('name', 'Next').click()
                sleep(3)
                # 查找分组，验证灯是否存在
                l1 = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')
                k1 = len(l1)
                print k1
                # c数组用来保存home页面分组名称
                c = []
                for i in range(0, k1):
                    # print l[i].text
                    c.append(l1[i].text)
                print u"c是："
                print c
                sleep(2)
                for j1 in range(0, k1):
                    if (c[j1] == name_group):
                        sleep(3)
                        print c[j1]
                        # print j
                        self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_right_image')[j1].click()
                        sleep(3)
                        # 判断是否需要滑动
                        try:
                            self.assertIsNone(self.driver.find_element('name', 'Add bulbs to Group').text,
                                              '有添加灯按钮')
                        except:
                            self.swipeUp(1000, 0.8, 0.8, 0.2)
                            sleep(3)
                        Grpupslist1 = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item')
                        GrpupslistName1 = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')
                        # list是分组中灯列表长度
                        list = len(Grpupslist1)
                        d = []
                        for r1 in range(0, list):
                            d.append(GrpupslistName1[r1].text)
                        print u"d是："
                        print d
                        #名称已经修改为rename值
                        if (rename in d):
                            print u"新增分组加灯成功"
                        else:
                            print u"新增分组加灯失败"
                    else:
                        j1 = j1 + 1