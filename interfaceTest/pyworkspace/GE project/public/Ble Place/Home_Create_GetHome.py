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
    u"""创建GetHome"""
    def Home_Create_GetHome(self):
        Time(1)
        self.driver.find_element('name', 'GET HOME').click()
        sleep(3)
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text, 'Scene Setup', 'GetHome打开失败')
        self.driver.find_element('name', 'Cancel').click()
        sleep(3)
        self.assertEqual(self.driver.find_elements('id', 'com.ge.cbyge:id/textview')[0].text, 'Home', 'GetHome取消失败')
        sleep(3)
        # 重新进入GetHome页面
        self.driver.find_element('name', 'GET HOME').click()
        sleep(3)
        # 进入setup选择列表
        self.driver.find_element('id', 'com.ge.cbyge:id/act_scene_setup_start').click()
        sleep(3)
        self.assertEqual(self.driver.find_element('name', 'Cancel').text, 'Cancel', 'GetHome创建页面没有返回功能')
        self.assertEqual(self.driver.find_element('name', 'Next').text, 'Next', 'GetHome创建页面没有下一步功能')
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text, 'Setup (1 of 2)',
                         'GetHome创建页面步骤一显示错误')
        # 不选择灯，直接点击Next按钮
        self.driver.find_element('name', 'Next').click()
        sleep(3)
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/dialog_tips').text,
                         'Please select at least one light you want in this scene!', '警告信息不正确信息不正确')
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/dialog_btn').text, 'Okay, got it',
                         '警告确认按钮名称错误')
        self.driver.find_element('id', 'com.ge.cbyge:id/dialog_btn').click()
        sleep(3)
        # 选择灯
        t = len(self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item_left_image'))
        # print t
        if (t > 1):
            for i in range(0, t):
                self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item_left_image')[i].click()
                # print i
                sleep(2)
            self.driver.find_element('name', 'Next').click()
            sleep(3)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text, 'Setup (2 of 2)', '步骤2页面跳转失败')
            sleep(3)
            # 步骤2返回功能验证
            self.driver.find_element('id', 'com.ge.cbyge:id/id_2').click()
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text, 'Setup (1 of 2)',
                             'GetHome创建页面步骤一显示错误')
            sleep(3)
            self.driver.find_element('name', 'Next').click()
            sleep(3)
            # 编辑功能验证
            self.driver.find_element('id', 'com.ge.cbyge:id/view_scene_edit_start').click()
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text, 'Setup (1 of 2)',
                             'edit编辑失败')
            sleep(3)
            self.driver.find_element('name', 'Next').click()
            sleep(3)
            # 修改灯亮度
            # st2 = len(self.driver.find_elements('id', 'com.ge.cbyge:id/view_scene_edit_detail_list_item_ll'))
            # print st2
            # 滑动标题框
            self.swipeUp(1000, 0.8, 0.36, 0.12)
            sleep(3)
            for i in range(0, t):
                try:
                    # BR30,SLEEP灯，调节控制
                    self.assertIsNotNone(
                        self.driver.find_element('id', 'com.ge.cbyge:id/view_scene_edit_detail_list_item_ll_color'))
                    # 亮度调节
                    # self.swipRight(1000, 0.78, 0.35, 0.50)
                    self.swipLeft(1000, 0.78, 0.50, 0.35)
                    sleep(3)
                    try:
                        self.assertIsNotNone(self.driver.find_element('id', 'com.ge.cbyge:id/tv_2400'))
                        # 调节BR30灯色彩为PLAY类型
                        self.driver.find_element('id', 'com.ge.cbyge:id/tv_3000').click()
                        sleep(3)
                    except:
                        # 调节sleep灯色彩为PM类型
                        self.driver.find_element('id', 'com.ge.cbyge:id/tv_pm').click()
                        sleep(3)
                    self.swipeUp(1000, 0.80, 0.66, 0.12)
                    sleep(3)
                except:
                    # life灯控制
                    self.swipRight(1000, 0.78, 0.35, 0.50)
                    # self.swipLeft(1000,0.78,0.50,0.35)
                    sleep(3)
                    self.swipeUp(1000, 0.80, 0.48, 0.12)
                    sleep(3)
                # print 'life'
            self.driver.find_element('name', 'Save').click()
            sleep(3)
            self.assertEqual(self.driver.find_elements('id', 'com.ge.cbyge:id/textview')[0].text, 'Home',
                             'GetHome创建失败')
        else:
            print u"没有在线的灯"