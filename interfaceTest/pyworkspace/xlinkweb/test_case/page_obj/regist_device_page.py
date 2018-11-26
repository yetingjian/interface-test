# coding=utf-8
from selenium.webdriver.common.by import By
from test_case.page_obj import loginPage
from test_case.page_obj import base
from selenium.common.exceptions import *
from common import exceluitl as EX, function as func
from base import Page
from time import sleep


class RegisterDevicePage(Page):
    obj = None
    data_path = func.find_path() + '/test_data/devplatform/regist_device.xlsx'
    data_sheet = 'locator'

    def click_dev_platform_item(self, name):
        list1 = self.find_elements((By.CLASS_NAME, 'content-text'))
        for i in list1:
            if i.text == name:
                i.click()
                func.log(u'点击：' + name)
                break

    def wait_count_visible(self):
        func.log(u'info')
        msg = self.wait_class_visible('info')
        if msg == 'Y':
            func.log(u'元素已可见')
        else:
            func.log(u'【异常】60秒后元素仍不可见')

    def click_register_type1(self, name):
        list1 = self.find_elements((By.CLASS_NAME, 'x-dropdown-item'))
        for i in list1:
            if i.text == name:
                i.click()
                func.log(u'点击：' + name)
                break

    def click_register_type2(self, name):
            self.click_button(name)

    def wait_x_alert_message_visible(self):
        func.log(u'等待x-form元素可见')
        msg = self.wait_class_visible('x-alert__message')
        if msg == 'Y':
            func.log(u'元素已可见')
        else:
            func.log(u'【异常】60秒后元素仍不可见')

    def input_MAC(self, text):
        if text != '':
            input_text = self.find_element((By.XPATH, u'//input[@placeholder="请输入MAC地址"]'))
            input_text.send_keys(text)
            func.log(u'MAC地址输入：' + text)

    def input_sequence(self, text):
        if text != '':
            input_text = self.find_element((By.XPATH, u'//input[@placeholder="请输入序列号"]'))
            input_text.send_keys(text)
            func.log(u'序列号输入：' + text)

    def input_device_name(self, text):
        if text != '':
            input_text = self.find_element((By.XPATH, u'//input[@placeholder="请输入名字"]'))
            input_text.send_keys(text)
            func.log(u'设备名称输入：' + text)

    def get_success_message(self):
        self.wait_x_alert_message_visible()
        alert_message = self.find_element((By.CLASS_NAME, u'x-alert__message'))
        func.log(u'导入后提示信息：' + alert_message.text)
        return alert_message.text

    def click_view_detail(self):
        self.find_element_by_xpath('//table/tr[1]/td[4]/div/a').click()
        func.log(u'点击查看详情')

    def wait_button_enabled_css(self, text):
        func.log(u'等待' + text + u'按钮可用')
        msg = self.wait_obj_enabled((By.CSS_SELECTOR, '.ml10.x-btn.x-btn--default.x-btn--small'), text)
        if msg == 'Y':
            func.log(text + u'按钮已可用')
            return True
        else:
            func.log(u'【异常】60秒后' + text + u'按钮仍不可用')
            return False

    def get_regist_num(self):
        obj = self.find_element_by_xpath('html/body/div[1]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/header/div[1]/div/div[3]')
        func.log(obj.text)
        return obj.text

    def get_mac(self):
        obj = self.find_element_by_xpath('//table/tr[1]/td[1]/div')
        func.log(u'MAC地址为：'+str(obj.text))
        return obj.text

    def get_sn(self):
        obj = self.find_element_by_xpath('//table/tr[1]/td[3]/div')
        func.log(u'SN为：' + str(obj.text))
        return obj.text

    def click_upload_obj(self, text):
        self.click_obj((By.CSS_SELECTOR, '.x-btn.x-btn--small.x-btn--upload'), text)

    def click_view_record(self, text):
        self.click_obj((By.CSS_SELECTOR, '.hl-primary'), text)











