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
    u"""创建Bedtime"""
    def Home_Create_Bedtime(self):
        Time(1)
        #不添加所以信息，提示信息检查
        self.driver.find_element('name', 'BEDTIME').click()
        sleep(3)
        self.driver.find_element('id', 'com.ge.cbyge:id/act_scene_setup_start').click()
        sleep(3)
        self.driver.find_element('name', 'Next').click()
        sleep(3)
        self.driver.find_element('name', 'Next').click()
        sleep(3)
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/dialog_tips').text,'Please select at least one light you want in this scene!','不添加设备提示信息错误')
        self.driver.find_element('id', 'com.ge.cbyge:id/dialog_btn').click()
        sleep(3)
        self.driver.find_element('id', 'com.ge.cbyge:id/id_2').click()
        sleep(3)
        self.driver.find_element('id', 'com.ge.cbyge:id/id_2').click()
        sleep(3)
        #正常流程验证
        self.driver.find_element('name', 'BEDTIME').click()
        sleep(3)
        self.driver.find_element('id', 'com.ge.cbyge:id/act_scene_setup_start').click()
        sleep(3)
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text,'Setup (1 of 3)','开始设置失败')
        sleep(3)
        #Setup1取消功能判断
        self.driver.find_element('id', 'com.ge.cbyge:id/id_2').click()
        sleep(3)
        self.assertEqual(self.driver.find_elements('id', 'com.ge.cbyge:id/textview')[0].text, 'Home',
                         'Setup (1 of 3)取消失败')
        #再次进入Setep1页面
        self.driver.find_element('name', 'BEDTIME').click()
        sleep(3)
        self.driver.find_element('id', 'com.ge.cbyge:id/act_scene_setup_start').click()
        sleep(3)
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text, 'Setup (1 of 3)', '开始设置失败')
        #Setup1不选择灯，点击next
        self.driver.find_element('name', 'Next').click()
        sleep(3)
        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/fg_new_scene_bulb_select_tips2').text,'ON for BEDTIME','Setup1不选择灯操作失败')
        #etup1选择1个灯，点击next
        self.driver.find_element('id', 'com.ge.cbyge:id/id_2').click()
        sleep(3)
        #t为Setup1中设备数量
        t = len(self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item_left_image'))
        print t
        # for i in range(0,t):
        if(t>=1):
            self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item_left_image')[0].click()
            sleep(2)
            self.driver.find_element('name', 'Next').click()
            sleep(3)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/fg_new_scene_bulb_select_tips2').text,
                             'ON for BEDTIME', 'Setup1选择单灯灯操作失败')
            #Setup2中不添加设备点击下一步
            self.driver.find_element('name', 'Next').click()
            sleep(5)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text,'Setup (3 of 3)','Setup2不添加设备操作失败')
            #t1为Setup2中设备数量
            #返回Setup2
            self.driver.find_element('id', 'com.ge.cbyge:id/id_2').click()
            sleep(3)
            t1 = len(self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item_left_image'))
            #Setup2添加1个设备检查
            if(t1>=1):
                self.driver.find_elements('id', 'com.ge.cbyge:id/view_scenes_item_left_image')[0].click()
                sleep(2)
            else:
                print u"没有可添加的灯设备2"
            self.driver.find_element('name', 'Next').click()
            sleep(5)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text,'Setup (3 of 3)','Setup2添加1个设备操作失败')
            self.driver.find_element('id', 'com.ge.cbyge:id/view_scene_edit_start').click()
            sleep(3)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text, 'Setup (1 of 3)',
                             'Setup2不添加设备操作失败')
            self.driver.find_element('name', 'Next').click()
            sleep(3)
            self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text, 'Setup (2 of 3)',
                             'Setup2不添加设备操作失败')
            self.driver.find_element('name', 'Next').click()
            sleep(5)
            #灯调节控制
            for i in range(0,t):
                try:
                    #BR30,SLEEP灯，调节控制
                    self.assertIsNotNone(self.driver.find_element('id', 'com.ge.cbyge:id/view_scene_edit_detail_list_item_ll_color'))
                    #亮度调节
                    # self.swipRight(1000, 0.78, 0.35, 0.50)
                    self.swipLeft(1000, 0.78, 0.50, 0.35)
                    sleep(3)
                    try:
                        self.assertIsNotNone(self.driver.find_element('id', 'com.ge.cbyge:id/tv_2400'))
                        #调节BR30灯色彩为PLAY类型
                        self.driver.find_element('id', 'com.ge.cbyge:id/tv_3000').click()
                        sleep(3)
                    except:
                        #调节sleep灯色彩为PM类型
                        self.driver.find_element('id', 'com.ge.cbyge:id/tv_pm').click()
                        sleep(3)
                    self.swipeUp(1000,0.80,0.66,0.12)
                    sleep(3)
                except:
                    #life灯控制
                    self.swipRight(1000,0.78,0.35,0.50)
                    # self.swipLeft(1000,0.78,0.50,0.35)
                    sleep(3)
                    self.swipeUp(1000,0.80,0.48,0.12)
                    sleep(3)
            self.driver.find_element('name', 'Save').click()
            sleep(3)
            self.assertEqual(self.driver.find_elements('id', 'com.ge.cbyge:id/textview')[0].text, 'Home', 'Bedtime创建失败')
        else:
            print u"没有可添加的灯设备1"

if __name__=='__main__':
    suite = unittest.TestSuite()
    suite.addTest(ContactsAndroid("Home_Create_Bedtime"))
    runner = unittest.TextTestRunner()
    runner.run(suite)