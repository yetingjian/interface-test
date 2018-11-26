# coding=utf-8
from selenium.webdriver.common.by import By
from test_case.page_obj import loginPage
from test_case.page_obj import base
from selenium.common.exceptions import *
from common import exceluitl as EX, function as func
from base import Page
from time import sleep


class CheckDropList(Page):
    obj = None
    data_path = func.find_path() + '/test_data/devplatform/check_drop_list.xlsx'
    data_sheet = 'locator'

    def click_dev_platform(self, name):
        list1 = self.find_elements((By.CLASS_NAME, 'x-tabs__item'))
        for i in list1:
            if i.text == name:
                i.click()
                func.log(u'点击：' + name)
                break

    def check_list_item(self, name):
        list1 = self.find_elements((By.CLASS_NAME, 'x-tabs__item'))
        for i in list1:
            if i.text == name:
                self.mouse_move_to(i)
                break
        lists = []
        list2 = self.find_elements((By.CLASS_NAME, 'list-title'))
        for i in list2:
            lists.append(i.text)
        list2 = self.find_elements((By.CLASS_NAME, 'default-item'))
        for i in list2:
            lists.append(i.text)
        list2 = self.find_elements((By.CLASS_NAME, 'list-item'))
        for i in list2:
            lists.append(i.text)
        return lists

    def set_base_product(self):
        lists = self.find_elements((By.XPATH, '//tbody/tr'))
        button = self.find_element((By.XPATH, '//table/tbody/tr[%d]/td[6]/div/span' % len(lists)))
        button.click()
        func.log(u'点击设置为首页产品')

    def get_current_product_name(self):
        name = self.find_element((By.CLASS_NAME, 'info-title'))
        func.log(u'当前产品为：' + name.text)
        return name.text

    def click_picker(self):
        self.find_element((By.CLASS_NAME, 'picker-trigger__label')).click()
        sleep(1)
        func.log(u'点击分类导航')

    def click_picker_classify(self, name):
        lists = self.find_elements((By.CLASS_NAME, 'x-tree-title'))
        for i in lists:
            if i.text == name:
                i.click()
                sleep(1)
                func.log(u'点击分类：'+name)
                break

    def check_product_in_list(self, name):
        lists = self.find_elements((By.CLASS_NAME, 'label'))
        for i in lists:
            if i.text == name:
                return True
        return False

    def search_product(self, name):
        input_text = self.find_element((By.XPATH, u'//input[@placeholder="输入关键词"]'))
        input_text.send_keys(name)
        sleep(1)
        lists = self.find_elements((By.CLASS_NAME, 'label'))
        for i in lists:
            if i.text == name:
                return True
        return False













