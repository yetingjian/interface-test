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
    u"""分组场景验证"""
    def Home_Groups_NewSchedule(self):
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
                        name = self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text
                        try:
                            self.assertIsNone(self.driver.find_element('name', 'Add New Schedule').text,',没有添加新分组按钮')
                            self.driver.find_element('name', 'Add New Schedule').click()
                            sleep(3)
                        except:
                            self.swipeUp(1000,0.8,0.8,0.2)
                            sleep(3)
                            self.driver.find_element('name', 'Add New Schedule').click()
                            sleep(3)
                        self.assertEuqal(self.driver.find_element('id', 'com.ge.cbyge:id/id_1').text,'New Schedule','添加场景失败')
                        name1 = self.driver.find_element('id', 'com.ge.cbyge:id/item_detail_smart_nlayout').text
                        self.assertEqual(name1,name,'场景中分组错误')
                    else:
                        print u"没有分组信息"
                        break
            except:
                i = i + 1
                continue
