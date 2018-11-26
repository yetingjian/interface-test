# coding=utf-8
from selenium.webdriver.common.by import By
from test_case.page_obj import loginPage
from test_case.page_obj import base
from selenium.common.exceptions import *
from common import exceluitl as EX, function as func
from base import Page
from time import sleep


class ConnectorPage(Page):
    obj = None
    data_path = func.find_path() + '/test_data/devplatform/connector.xlsx'
    data_sheet = 'locator'

    def click_connector_manager(self):
        lists = self.find_elements((By.CLASS_NAME, 'secondary-nav-item-root'))
        try:
            for i in lists:
                if i.text == u'物联网连接器':
                    i.click()
                    func.log(u'点击物联网连接器')
                    sleep(1)
                    objs = self.find_elements((By.CLASS_NAME, 'item-second-nav'))
                    for j in objs:
                        if j.text == u'连接器管理':
                            j.click()
                            func.log(u'点击连接器管理')
                    break
        except Exception:
            func.log(u'【异常】连接器管理未找到')
            raise

    def input_connector_name(self, text):
        if text != '':
            input_text = self.find_element((By.XPATH, u'//input[@placeholder="连接器名称"]'))
            input_text.send_keys(text)
            func.log(u'连接器名称输入：' + text)

    def get_attribute(self, obj):
        element = self.find_element((By.CSS_SELECTOR, '.x-btn.x-btn--primary.x-btn--long'))
        return element.get_attribute(obj)

    def search_connector(self, text):
        if text != '':
            input_text = self.find_element((By.XPATH, u'//input[@placeholder="搜索连接器名称"]'))
            input_text.send_keys(text)
            func.log(u'搜索条件输入：' + text)
        element = self.find_element((By.CSS_SELECTOR, '.x-search-box__button.x-btn.x-btn--default.x-btn--normal'))
        element.click()
        func.log(u'点击搜索')

    def get_row_text(self):
        rows = self.find_element((By.XPATH, '//table/tbody/tr/td[1]'))
        return rows.text

    def click_manage(self):
        obj = self.find_element((By.XPATH, '//table/tbody/tr/td[5]/div/a'))
        obj.click()
        func.log(u'点击管理')

    def click_edit(self):
        self.click_obj_by_css('.x-btn.x-btn--default.x-btn--small')
        items = self.find_elements((By.CLASS_NAME, 'x-dropdown-item'))
        for i in items:
            if i.text == u'编辑':
                i.click()
                func.log(u'点击编辑')
                break

    def click_delete_connector(self):
        self.click_obj_by_css('.x-btn.x-btn--default.x-btn--small')
        items = self.find_elements((By.CLASS_NAME, 'x-dropdown-item'))
        for i in items:
            if i.text == u'删除':
                i.click()
                func.log(u'点击删除')
                break

    def click_upload_file(self):
        self.find_element((By.CLASS_NAME, 'x-upload__btn-file')).click()
        func.log(u'点击上传文件')

    def clear_connector_name(self):
        input_text = self.find_element((By.XPATH, u'//input[@placeholder="连接器名称"]'))
        self.clear(input_text)

    def get_connector_name(self):
        obj = self.find_child_element((By.CLASS_NAME, 'detail-title'), (By.TAG_NAME, 'h4'))
        return obj.text

    def input_version_num(self, text):
        if text != '':
            input_text = self.find_element((By.XPATH, u'//input[@placeholder="请输入版本号"]'))
            input_text.send_keys(text)
            func.log(u'版本号输入：' + text)

    def input_comments(self, text):
        if text != '':
            input_text = self.find_element((By.CLASS_NAME, 'w-e-text'))
            input_text.send_keys(text)
            func.log(u'说明输入：' + text)

    def click_release(self):
        obj = self.find_element((By.XPATH, '//tbody/tr/td[6]/div/div/div[1]/a'))
        obj.click()
        func.log(u'点击：' + obj.text)

    def input_remarks(self):
        input_text = self.find_element((By.XPATH, u'//textarea[@placeholder="发布备注"]'))
        input_text.send_keys(u'备注')
        func.log(u'输入发布备注')

    def get_version_status(self):
        status = self.find_element((By.XPATH, '//tbody/tr/td[2]/div/span'))
        return status.text

    def input_verify_text(self):
        input_text = self.find_elements((By.XPATH, u'//input[@placeholder="立即执行"]'))
        for i in input_text:
            if i.is_displayed():
                i.send_keys(u'立即执行')
                func.log(u'输入立即执行')
                break

    def click_delete(self):
        obj = self.find_element((By.XPATH, '//tbody/tr/td[6]/div/div/div[3]/a'))
        obj.click()
        func.log(u'点击：' + obj.text)

    def get_empty_table(self):
        status = self.find_element((By.XPATH, '//tbody/tr/td/div/div'))
        return status.text
