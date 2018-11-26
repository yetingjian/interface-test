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
    u"""分组添加灯"""
    def Home_Groups_AddBulbs(self):
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
                        self.driver.find_elements('id', 'com.ge.cbyge:id/view_groups_item_right_image')[1].click()
                        sleep(3)
                        self.swipeUp(1000, 0.8, 0.8, 0.2)
                        sleep(3)
                        self.driver.find_element('name', 'Add bulbs to Group').click()
                        sleep(3)
                        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/view_new_group_first_tips1').text,'Select the bulbs you want in this group:','添加灯失败')
                    else:
                        print u"没有分组信息"
                        break
            except:
                i = i + 1
                continue
