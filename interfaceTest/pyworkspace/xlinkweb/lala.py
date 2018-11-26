# coding=utf-8

import random
from common.function import random_string
from time import sleep
from selenium import webdriver
from common import exceluitl as EX,function as func
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import imaplib
import re

r = imaplib.IMAP4_SSL('smtp.exmail.qq.com')
r.login('wangqi@xlink.cn', '120211Qq')
x, y = r.status('INBOX', '(MESSAGES UNSEEN)')
allmes, unseenmes = re.match(r'.*\s+(\d+)\s+.*\s+(\d+)', y[0]).groups()
tomail = ('%s have  %s message, %s is unseenmes'  % ('wangqi@xlink.cn', allmes, unseenmes))
print unseenmes


# r.list()
# r.select('inbox')
# typ, data = r.search(None, 'UNSEEN')
# for num in data[0].split():
#     typ, data = r.fetch(num, '(BODY.PEEK[])')
#     # r.store(num,'+FLAGS','\Seen')
#     for i in data:
#         # print str(i).find('Subject')
#         # ind = int(str(i).find('Subject'))
#         # print str(i).find('\\n', ind)
#         # ind2 = int(str(i).find('\\n', ind))
#         # print str(i)[ind+9:ind2]
#         print 'Message %s\n%s\n' % (num, repr(data))


# x1, y = r.status('INBOX', '(MESSAGES UNSEEN)')
# allmes, unseenmes = re.match(r'.*\s+(\d+)\s+.*\s+(\d+)', y[0]).groups()
# tomail1 = ('%s have  %s message, %s is unseenmes'  % ('wangqi@xlink.cn', allmes, unseenmes))
# print tomail1

# r.close()
# r.logout()

# data_path = func.find_path() + '/test_data/devplatform/create_product.xlsx'
# data_sheet = 'case'
# data_sheet1 = 'case1'
# value_list = EX.get_case_list(data_path, data_sheet1, 'test_data_type_2')
# print value_list[8].split(',')[0]
#
#
# def click_main_tab(self, name):
#     try:
#         lists = self.find_elements(self.dev_platform_loc)
#         for i in range(len(lists)):
#             if lists[i].text == name:
#                 lists[i].click()
#                 func.log(u'点击：' + name)
#                 sleep(2)
#                 break
#             elif i == len(lists) - 1:
#                 func.log(u'模块【' + name + u'】未找到')
#     except Exception:
#         func.log(u'【异常】模块【' + name + u'】未找到')
#         raise