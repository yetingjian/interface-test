#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# import HTMLTestRunner
import time
import unittest
from appium import webdriver
from time import sleep
import re
# import xlrd
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

timestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

class ContactsAndroid(unittest.TestCase):
    def setUp(self):
        desired_caps = {'platformName': 'Android',
                        'platformVersion': '5.0',
                        'deviceName': '671fe9df',
                        'appPackage': 'com.ge.cbyge',
                        'appActivity': 'com.ge.cbyge.ui.guide.GuidePager',
                        'unicodeKeyboard': (True,),
                        'resetKeyboard': True}
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub',desired_caps)

    # 获得机器屏幕大小x,y
    def getSize(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        print u'x坐标=', x
        print u'y坐标=', y
        return (x, y)

    def swipelocation(self, t, xb1, yb1, xb2,yb2):
        l = self.getSize()
        x1 = int(l[0] * xb1)  # x坐标
        y1 = int(l[1] * yb1)  # 起始y坐标
        x2 = int(l[0] * xb2)  # x终点坐标
        y2 = int(l[1] * yb2)  # 终点y坐标
        self.driver.swipe(x1, y1, x2, y2, t)

    # 屏幕向上滑动
    def swipeUp(self, t, xb1, yb1, yb2):  # t=拖动时间 ; xb1=X坐标比例位置 ; yb1=起始y坐标比例位置 ;yb2=终点y坐标比例位置
        #备注：xb1,yb1为操作起始点位置坐标比例，xb2,yb2为操作结束点位置坐标比例，都是相对的，不是绝对，根据滑动方向而定
        l = self.getSize()
        x1 = int(l[0] * xb1)  # x坐标
        y1 = int(l[1] * yb1)  # 起始y坐标
        y2 = int(l[1] * yb2)  # 终点y坐标
        self.driver.swipe(x1, y1, x1, y2, t)

    # 屏幕向下滑动
    def swipeDown(self, t, xb1, yb1, yb2):
        l = self.getSize()
        x1 = int(l[0] * xb1)  # x坐标
        y1 = int(l[1] * yb1)  # 起始y坐标
        y2 = int(l[1] * yb2)  # 终点y坐标
        self.driver.swipe(x1, y1, x1, y2, t)

    # 屏幕向左滑动
    def swipLeft(self, t, xb1, yb1, xb2):
        l = self.getSize()
        x1 = int(l[0] * xb1)
        y1 = int(l[1] * yb1)
        x2 = int(l[0] * xb2)
        self.driver.swipe(x1, y1, x2, y1, t)

    # 屏幕向右滑动
    def swipRight(self, t, xb1, yb1, xb2):
        l = self.getSize()
        x1 = int(l[0] * xb1)
        y1 = int(l[1] * yb1)
        x2 = int(l[0] * xb2)
        self.driver.swipe(x1, y1, x2, y1, t)

    def screenshot(self,pngname):
        timestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        img_name = pngname + timestr + '.png'
        png_file = "C:\\Users\\Demon\\Desktop\\appium截图\\png\\"
        self.driver.get_screenshot_as_file('%s%s' % (png_file, img_name))
        print u'截图位置:',png_file
        print u'截图名称:',img_name

    #滑动到指定元素
    def find_by_scroll(self, item_name):
        item = self.driver.find_element_by_android_uiautomator(
            'new UiScrollable(new UiSelector().scrollable(true).instance(0)).getChildByText(new UiSelector().className("android.widget.TextView"), "'
            + item_name + '")')
        # item.click()