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
    u"""Add New Schedule-完整创建一个关于scene的schedule"""
    def Scenes_AddNewSchedule_GetHome(self):
        Time(1)
        self.driver.find_element('name', 'Scenes').click()
        sleep(3)
        list = self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item_text')
        # 计算列表长度
        l = len(list)
        # print l
        if (l > 4):
            # 点击最后一个场景，打开场景详情
            self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item_right_image')[l - 1].click()
            sleep(3)
            self.driver.find_element('id', 'com.ge.cbyge:id/act_scene_control_text').click()
            sleep(3)
            self.driver.find_element('id', 'com.ge.cbyge:id/add_smart_control_name').send_keys(u"scene1")
            name = self.driver.find_element('id', 'com.ge.cbyge:id/add_smart_control_name').text
            sleep(3)
            try:
                self.assertIsNotNone(self.driver.find_element('name', 'Change Scene'), '有场景按钮')
                sleep(3)
            except:
                self.find_by_scroll('Change Scene')
                # self.swipeUp(1000, 0.5, 0.9, 0.4)
                sleep(3)
            self.driver.find_element('name', 'Change Scene').click()
            sleep(3)
            scene_list = self.driver.find_elements('id', 'com.ge.cbyge:id/item_select_child_name')
            scene_num = len(scene_list)
            a = []
            for i in range(0,scene_num):
                if(scene_list[i].text =='GET HOME'):
                    a.append(i)
                    sleep(2)
            #选择GET HOME类型
            self.driver.find_elements('id', 'com.ge.cbyge:id/item_select_child_checkBox')[a[0]].click()
            sleep(3)
            self.driver.find_element('name', 'Done').click()
            sleep(5)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/item_detail_smart_ctrl_name').text,'GET HOME','返回页面错误')

            self.driver.find_element('name', 'Save').click()
            sleep(5)
            try:
                self.assertIsNotNone(self.driver.find_element('id', 'com.ge.cbyge:id/dialog_tips'),'不存在同名时间表信息')
                print u"存在同名时间表信息"
                sleep(2)
                self.driver.find_element('id', 'com.ge.cbyge:id/dialog_btn').click()
            except:
                self.assertIsNotNone(self.driver.find_element('id', 'com.ge.cbyge:id/act_scene_control_check_tips'),'场景添加失败')
        else:
            print u"不存在可编辑的分组"
