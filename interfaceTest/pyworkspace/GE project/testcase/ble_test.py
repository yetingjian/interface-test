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
sys.path.append("C:\Users\Demon\Desktop\GE project\public\Ble Place")
from Start import ContactsAndroid
from TimeOut import Time
import Home_Create_Bedtime
import Home_Create_GetHome
import Scenes_CreateNewScene

if __name__ =='__main__':
    suite = unittest.TestSuite()
    #调用顺序为py文件名-类名-执行方法

    # suite.addTest(ContactsAndroid("Home_Create_Bedtime.Home_Create_Bedtime()"))
    # suite.addTest(Home_Create_Bedtime.ContactsAndroidTests("Home_Create_Bedtime"))
    suite.addTest(Scenes_CreateNewScene.ContactsAndroidTests("Scenes_CreateNewScene"))
    runner = unittest.TextTestRunner()
    runner.run(suite)

