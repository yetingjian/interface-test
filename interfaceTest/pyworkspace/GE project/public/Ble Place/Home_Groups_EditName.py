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
    u"""分组名称修改"""
    def Home_Groups_EditName(self):
        Time(1)
        l = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')
        k = len(l)
        sleep(3)
        for i in range(0, k):
            try:
                if (l[i].text == "Create new group"):
                    sleep(3)
                    if (i > 1):
                        # 打开第一个分组
                        # name1 = self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_text')[1].text
                        self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_right_image')[1].click()
                        sleep(3)
                        self.driver.find_element('id', 'com.ge.cbyge:id/id_3').click()
                        sleep(3)
                        self.driver.switch_to_alert()
                        # 点击Edit Group Name按钮
                        self.swipelocation(1, 0.40, 0.85, 0.50, 0.86)
                        sleep(3)
                        self.driver.find_element('id', 'com.ge.cbyge:id/act_group_name_edittext').send_keys(u"分组名称修改测试")
                        sleep(3)
                        name_edit1 =  self.driver.find_element('id', 'com.ge.cbyge:id/act_group_name_edittext').text
                        self.driver.find_element('name', 'Save').click()
                        sleep(3)
                        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text,name_edit1,'编辑保存失败')
                    else:
                        print u"没有分组信息"
                        break
            except:
                i = i +1
                continue
