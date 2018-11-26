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
    u"""分组删除取消"""
    def Home_Groups_DeleteGroups_Cancel(self):
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
                        name1 = self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text
                        self.driver.find_element('id', 'com.ge.cbyge:id/id_3').click()
                        sleep(3)
                        self.driver.switch_to_alert()
                        # 点击Delete Group按钮
                        self.swipelocation(1, 0.40, 0.91, 0.50, 0.92)
                        sleep(3)
                        self.driver.find_element('id', 'com.ge.cbyge:id/activity_group_delete_cancel').click()
                        sleep(3)
                        self.assertEqual(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text,name1,'取消删除失败')
                    else:
                        print u"没有分组信息"
                        break
            except:
                i = i +1
                continue
