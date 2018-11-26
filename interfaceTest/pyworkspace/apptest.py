# coding=utf-8

from appium import webdriver
import datetime
from time import sleep

# desired_caps ={
#     'platformName': 'Android',
#     'deviceName': '127.0.0.1:62001',
#     'platformVersion': '4.4.2',
#     'appPackage': 'com.kaercher.smartair',
#     'appActivity': 'cn.xlink.kaichi.ui.module.splash.SplashActivity',
#     'unicodeKeyboard': True,
#     'resetKeyboard': True
# }
#
# driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
# sleep(8)
# driver.find_element_by_id('com.kaercher.smartair:id/login_weixin_button').click()

print datetime.datetime.now().year
print datetime.datetime.now().month
print datetime.datetime.now().day