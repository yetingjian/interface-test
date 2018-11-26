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
    u"""将灯加入新分组"""
    def Home_SingleBules_AddBulesToNewGroup(self):
        Time(1)
        try:
            self.assertIsNone(self.driver.find_element('name', 'Create new group').text, '没有新增分组按钮')
            sleep(3)
        except:
            self.swipeUp(1000, 0.8, 0.8, 0.2)
            sleep(3)
        list = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')
        l = len(list)
        a = []
        b = []
        #计算创建分组长度，判断是否有分组
        for i in range(0,l):
            if(list[i].text == 'Create new group'):
                a.append(i)
            else:
                i = i + 1
        print a
        try:
            self.assertIsNone(self.driver.find_element('name', 'Add a bulb').text, '没有新增分组按钮')
            sleep(3)
        except:
            self.swipeUp(1000, 0.8, 0.8, 0.2)
            sleep(3)
        #计算灯列表长度，检查是否有灯
        for i1 in range(0,l):
            if(list[i1].text == 'Add a bulb'):
                b.append(i1)
            else:
                i1 = i1 + 1
        print b
        if(a[0]<=1):
            print u"不存在分组，可创建新分组"
            k = b[0] - a[0]
            if(k>= 2):
                print u"存在灯"
                self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_right_image')[a[0]+2].click()
                sleep(3)
                self.driver.find_element('id', 'com.ge.cbyge:id/id_3').click()
                sleep(3)
                self.driver.switch_to_alert()
                # 点击Add or Remove Bulb from Groups按钮
                self.swipelocation(1, 0.40, 0.81, 0.50, 0.82)
                sleep(3)
                self.assertIsNotNone(self.driver.find_element('name', 'Add Bulb to Groups'),'添加新分组失败')
                #添加灯到新创建的分组中
                self.driver.find_element('id', 'com.ge.cbyge:id/act_bulb_to_group_name_edittext').send_keys(u"加灯新建分组")
                sleep(3)
                name = self.driver.find_element('id', 'com.ge.cbyge:id/act_bulb_to_group_name_edittext').text
                self.driver.find_element('name', 'Save').click()
                sleep(3)
                #只有一个新创建分组，因此不需要进行判断
                self.assertEqual(self.driver.find_elements('id','com.ge.cbyge:id/view_groups_item_text')[0].text,name,'加灯新建分组失败')
                #点击添加分组按钮
                self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_left_image')[0].click()
                sleep(3)
                self.driver.find_element('name', 'Save').click()
                sleep(3)
                self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/seekbar_light_lum_text').text,
                                 'BRIGHTNESS', '单灯详情查看失败')
            else:
                print u"不存在灯"
        else:
            print u"已经存在分组，不能创建新分组"
