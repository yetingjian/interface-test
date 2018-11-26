# coding=utf-8
from selenium import webdriver
import unittest
from test_case.page_obj.base import Page
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from time import sleep
import SendKeys
import os
from common import exceluitl as EX, function as func


import logging


base_dir = os.path.dirname(os.path.dirname(__file__))
base_dir = str(base_dir)


# data_path = func.find_path() + '/test_data/login/login.xlsx'
# data_sheet = 'locator'
# stc = './/*[@id=\'login\']/div[2]/form/div[1]/div/div[2]'
# stc3 = EX.get_locator_value(data_path, data_sheet, 'user_empty_loc')
driver = webdriver.Chrome()
driver.maximize_window()
url = "https://admin.xlink.cn/#!"
url1 = "http://dev-admin.xlink.cn/v5.3.2/#/apps/develop/dev-products/1607d2b6f9ad00011607d2b6f9ada801/product-info"
driver.get(url)
driver.implicitly_wait(10)
driver.find_element_by_name('model.account').send_keys('gyb@xlink.cn')
#driver.find_element_by_name('account').send_keys('wq@xlink.cn')
driver.find_element_by_name('model.password').send_keys('Test1234')
# driver.find_element_by_css_selector('.submit.x-btn.x-btn--primary.x-btn--large').click()
# sleep(5)
driver.find_element_by_xpath('.//*[@id="app"]/div/div/div[1]/div[2]/form/div[4]/button').click()
sleep(5)
driver.get('https://admin.xlink.cn/#!/dev/home')
sleep(3)
d = driver.find_element_by_class_name('title1')
sleep(1)
print d.text

# driver.find_element_by_class_name('gateway-name').click()
# sleep(2)
# objs = driver.find_elements_by_css_selector('.app-type-icon')
# print len(objs)
# objs[1].click()



# lis1 = []
# lis1 = driver.find_elements_by_class_name('x-tabs__item')
# for i in range(len(lis1)):
#     print lis1[i].text
#
# lis1[0].click()
# sleep(4)
#
# link = driver.find_element_by_xpath('//a[@href="http://support.xlink.cn/hc/kb/article/210598"]')
# print link.text
# link1 = driver.find_element_by_partial_link_text(u'[更新说明]')
# link1.click()


# lis2 = []
# lis2 = driver.find_elements_by_css_selector(".bottom-button-box")
# #lis2[0].click()
# sleep(2)
# # lis = []
# # lis = driver.find_elements_by_css_selector(".nav-item")
# # print len(lis)
# # print lis[0].text
# driver.execute_script("arguments[0].scrollIntoView();", lis2[0])
# lis2[0].click()
# driver.find_element_by_css_selector(".x-btn.x-btn--primary.x-btn--large").click()
# lis5 = []
# lis5 = driver.find_elements_by_css_selector(".x-form-item__label")
# for i in range(len(lis5)):
#     if lis5[i].text == u'产品名称':
#         aaa = driver.find_element_by_xpath("//form/div["+str(i+1)+"]/div/div/input")
#         aaa.send_keys(u"1412")
#         sleep(2)
#         break
#
# lis8 = driver.find_elements_by_css_selector(".x-form-item__label")
# for i in range(len(lis8)):
#     if lis8[i].text == u'连接类型':
#         aaa = driver.find_element_by_xpath("//form/div["+str(i+1)+"]/div/div/div")
#         aaa.click()
#         sleep(1)
#         break
#
# lis9 = driver.find_elements_by_css_selector(".x-select-item")
# print len(lis9)
# for i in range(len(lis9)):
#     print lis9[i].text
#     driver.execute_script("arguments[0].scrollIntoView();", lis9[i])
#     if lis9[i].text == u'Zigbee设备':
#
#         lis9[i].click()
#         sleep(1)
#         break
#
# lis10 = driver.find_elements_by_css_selector(".x-radio-input")
# lis10[0].click()



# lis6 = []
# lis6 = driver.find_elements_by_css_selector(".x-btn.x-btn--primary.x-btn--large")
# print len(lis6)
# for i in range(len(lis6)):
#     print lis6[i].text
#     if lis6[i].text == u'创建':
#         lis6[i].click()
#         break
# sleep(2)
# lis7 = []
# lis7 = driver.find_elements_by_css_selector(".x-btn.x-btn--primary")
# print len(lis7)
# for i in range(len(lis7)):
#     print lis7[i].text
#     if lis7[i].text == u'配置完成，下一步':
#         lis7[i].click()
#         break


# driver.find_element_by_id("forget-link").click()
# sleep(1)
# driver.find_element_by_css_selector(".register").click()
# sleep(1)
# driver.find_element(By.XPATH, u'//input[@placeholder="手机号码"]').send_keys('123')
# print len(lis5)
# print lis5[0].get_attribute('placeholder')
# print lis5[1].get_attribute('placeholder')
# print lis5[2].get_attribute('placeholder')
# print lis5[3].get_attribute('placeholder')
# lis5[2].send_keys('132')
# sleep(1)
# sleep(5)
# loc = ('class', 'currentName')
# loct = 'currentName'
# for i in range(20):
#     elem = driver.page_source
#     if EC.visibility_of_element_located((By.CLASS_NAME, loct)):
#         break
#     else:
#         sleep(1)
#
# sleep(1)
#


