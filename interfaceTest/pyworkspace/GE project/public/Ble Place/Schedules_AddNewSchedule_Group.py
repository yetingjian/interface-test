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
    u"""Schedules-add new schedule（groups）"""
    def Schedules_AddNewSchedule_Group(self):
        Time(1)
        try:
            self.assertIsNotNone(self.driver.find_element('name', 'Create new group').text, '没有添加灯按钮')
            sleep(3)
        except:
            self.find_by_scroll('Create new group')
            sleep(3)
        list = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')
        l = len(list)
        print l
        a = []
        # 查找Create new group位置
        for i in range(0, l):
            if (list[i].text == 'Create new group'):
                a.append(i)
        print a
        if(a[0]>1):
            print u"存在分组"
            #点击最后一个分组
            self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_right_image')[a[0]-1].click()
            sleep(3)
            #name为空保存
            try:
                self.assertIsNotNone(self.driver.find_element('name', 'Add New Schedule').text, '有添加场景按钮')
                sleep(3)
            except:
                self.find_by_scroll('Add New Schedule')
                sleep(3)
            list1 = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')
            list_s = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_details')
            #l_s场景长度计算，l_n列表长度计算
            l_s = len(list_s)
            print l_s
            l_n = len(list1)
            print l_n
            b = []
            #存场景名称，保存后用于对比验证
            if(l_s > 0):
                for i in range(l_n-l_s-1,l_n-1):
                    b.append(list1[i].text)
                print b
            name = self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text
            print name
            self.driver.find_element('name', 'Add New Schedule').click()
            sleep(3)
            #不输入名称保存
            self.driver.find_element('name', 'Save').click()
            sleep(3)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text,name,'名称为空保存失败')
            #输入重名场景
            try:
                self.assertIsNotNone(self.driver.find_element('name', 'Add New Schedule').text, '有添加场景按钮')
                sleep(3)
            except:
                self.find_by_scroll('Add New Schedule')
                sleep(3)
            self.driver.find_element('name', 'Add New Schedule').click()
            sleep(3)
            self.driver.find_element('id', 'com.ge.cbyge:id/add_smart_control_name').send_keys(b[0])
            sleep(3)
            self.driver.find_element('name', 'Save').click()
            sleep(3)
            self.assertIsNotNone(self.driver.find_element('id', 'com.ge.cbyge:id/dialog_tips'),'重名保存失败')
            sleep(3)
            self.driver.find_element('id', 'com.ge.cbyge:id/dialog_btn').click()
            sleep(3)
            #滑动定位到GROUPS
            try:
                self.assertIsNotNone(self.driver.find_element('name', 'GROUPS').text, '有分组')
                sleep(3)
            except:
                # self.find_by_scroll('GROUPS')
                self.swipeUp(1000, 0.5, 0.9, 0.4)
                sleep(3)
            #选择单个星期
            self.driver.find_element('id', 'com.ge.cbyge:id/week_sunday').click()
            sleep(2)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/repeate_value').text,' Sun','单天选择错误')
            #选择整个星期
            self.driver.find_element('id', 'com.ge.cbyge:id/week_monday').click()
            sleep(2)
            self.driver.find_element('id', 'com.ge.cbyge:id/week_tuesday').click()
            sleep(2)
            self.driver.find_element('id', 'com.ge.cbyge:id/week_wednesday').click()
            sleep(2)
            self.driver.find_element('id', 'com.ge.cbyge:id/week_thursday').click()
            sleep(2)
            self.driver.find_element('id', 'com.ge.cbyge:id/week_friday').click()
            sleep(2)
            self.driver.find_element('id', 'com.ge.cbyge:id/week_saturday').click()
            sleep(2)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/repeate_value').text, 'Everyday', '整个星期选择错误')
            try:
                self.assertIsNotNone(self.driver.find_element('name', 'Change Groups').text, '有修改分组按钮')
                sleep(3)
            except:
                # self.find_by_scroll('Change Groups')
                self.swipeUp(1000,0.5,0.9,0.4)
                sleep(3)
            self.driver.find_element('name', 'Change Groups').click()
            sleep(3)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text,'Select Groups','修改分组失败')
            list_name = self.driver.find_elements('id', 'com.ge.cbyge:id/item_select_child_name')
            l_m = len(list_name)
            print l_m
            #分组少于4个，大于1个判断
            if(l_m>1 and l_m<=4):
                for j in range(0,l_m):
                    if(list_name[j].text == name):
                        j = j + 1
                    else:
                        self.driver.find_elements('id', 'com.ge.cbyge:id/item_select_child_checkBox')[j].click()
                        sleep(2)
                #点击取消
                self.driver.find_element('id', 'com.ge.cbyge:id/id_2').click()
                sleep(3)
                l_m1 = len(list_name)
                self.assertEqual(l_m,l_m1,'取消失败')
            #选择大于4个时，验证是否有弹出框信息
            elif(l_m >4 ):
                for j in range(0, 5):
                    if(list_name[j].text == name):
                        j = j + 1
                    else:
                        self.driver.find_elements('id', 'com.ge.cbyge:id/item_select_child_checkBox')[j].click()
                        sleep(2)
                self.assertIsNotNone(self.driver.find_element('id', 'com.ge.cbyge:id/dialog_btn'),'选择超出4个分组时无提示框')
            else:
                # 点击取消
                self.driver.find_element('id', 'com.ge.cbyge:id/id_2').click()
                sleep(3)
        else:
            print u"没有分组"