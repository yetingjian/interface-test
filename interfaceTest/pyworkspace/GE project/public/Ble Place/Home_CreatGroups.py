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
    u"""创建NewScene"""
    def Home_Create_NewScene(self):
        Time(1)
        sleep(30)
        # self.swipRight(1000,0.15,0.90,0.30)
        self.swipLeft(1000,0.90,0.15,0.30)
        sleep(3)
        self.driver.find_element('name', 'NEW SCENE').click()
        sleep(3)
        self.assetEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text,'Select Bulbs','NewScene打开失败')
        #不勾选为空，错误检查
        self.driver.find_element('name', 'Next').click()
        sleep(3)
        self.assetEqual(self.driver.find_element('id', 'com.ge.cbyge:id/dialog_tips').text, 'Please select at least one light you want in this scene!', 'NewScene提示信息错误')
        self.driver.find_element('id', 'com.ge.cbyge:id/dialog_btn').click()
        sleep(3)
        #返回功能验证
        self.driver.find_element('id', 'com.ge.cbyge:id/id_2').click()
        sleep(3)
        self.assertEqual(self.driver.find_elements('id', 'com.ge.cbyge:id/textview')[0].text, 'Home', 'NewScene取消失败')
        #重新进入NEW SCENE
        self.driver.find_element('name', 'NEW SCENE').click()
        sleep(3)
        t = len(self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item_left_image'))
        print t
        for i in range(0, t):
            self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item_left_image')[i].click()
            # print i
            sleep(2)
        self.driver.find_element('name', 'Next').click()
        sleep(5)
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text, 'New Scene name', 'NewScene创建失败')
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/fg_scene_name_edittext').text, 'Scene Name', 'NewScene提示名称错误')
        #名称为空检查
        self.driver.find_element('name', 'Next').click()
        sleep(3)
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/dialog_tips').text, 'The scene name you entered can not be empty, please retry!', 'NewScene名称为空提示信息不正确')
        self.driver.find_element('id', 'com.ge.cbyge:id/dialog_btn').click()
        sleep(3)
        #正常输入名称
        self.driver.find_element('id', 'com.ge.cbyge:id/fg_scene_name_edittext').sendkeys(u"NewScene测试")
        sleep(3)
        self.driver.find_element('name', 'Next').click()
        sleep(5)
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text, 'Edit Scene', 'NewScene创建失败2')
        #编辑修改功能检查
        self.driver.find_element('id', 'com.ge.cbyge:id/view_scene_edit_start').click()
        sleep(3)
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text, 'Setup (1 of 3)', 'NewScene编辑失败')
        self.driver.find_element('name', 'Next').click()
        sleep(3)
        for j in range(0, t):
            try:
                self.assertIsNotNone(self.driver.find_elements('id', 'com.ge.cbyge:id/view_scene_detail_list_item_bg')[j])
                self.swipRight(1000, 0.78, 0.35, 0.50)
                sleep(3)
                self.swipeUp(1000, 0.80, 0.48, 0.12)
                sleep(3)
                print j
            except:
        # life灯控制
                self.driver.find_elements('id', 'com.ge.cbyge:id/view_scene_edit_detail_list_item_ll')[j].click()
                sleep(3)
                print j
                try:
                    self.assertIsNotNone(
                        self.driver.find_elements('id', 'com.ge.cbyge:id/view_scene_edit_detail_list_item_ll_color')[
                            j].text)
                    print '1'
                    # self.assertIsNone(self.driver.find_elements('id', 'com.ge.cbyge:id/view_scene_edit_detail_list_item_ll_color')[j].text)
                except:
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
        self.driver.find_element('name', 'Next').click()
        sleep(3)
        self.assertEqual(self.driver.find_elements('id', 'com.ge.cbyge:id/textview')[0].text, 'Home',
                         'NewScene保存失败')
