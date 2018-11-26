# coding=utf-8
from selenium.webdriver.common.by import By
from test_case.page_obj import loginPage
from test_case.page_obj import base
from selenium.common.exceptions import *
from common import exceluitl as EX, function as func
from base import Page
from time import sleep


class GatewayPage(Page):
    obj = None
    data_path = func.find_path() + '/test_data/devplatform/connector.xlsx'
    data_sheet = 'locator'

    def click_apps_gateway(self):
        lists = self.find_elements((By.CLASS_NAME, 'secondary-nav-item-root'))
        try:
            for i in lists:
                if i.text == u'应用网关':
                    i.click()
                    func.log(u'点击应用网关')
                    break
        except Exception:
            func.log(u'【异常】连应用网关未找到')
            raise

    def click_new_app(self):
        self.find_element((By.CLASS_NAME, 'gateway-name')).click()
        func.log(u'点击新建应用')

    def input_app_name(self, text):
        if text != '':
            input_text = self.find_element((By.XPATH, u'//input[@placeholder="请输入应用名称"]'))
            input_text.send_keys(text)
            func.log(u'应用名称输入：' + text)

    def click_app_flag(self, num):
        flags = self.find_elements((By.CLASS_NAME, 'app-type-icon'))
        flags[num].click()
        if num == 0:
            func.log(u'点击ios图标')
        elif num == 1:
            func.log(u'点击android图标')
        elif num == 2:
            func.log(u'点击微信图标')
        elif num == 3:
            func.log(u'点击连接器图标')
        elif num == 4:
            func.log(u'点击其他图标')

    def input_app_desc(self, text):
        if text != '':
            input_text = self.find_element((By.XPATH, u'//textarea[@placeholder="请输入应用描述"]'))
            input_text.send_keys(text)
            func.log(u'应用描述输入：' + text)

    def get_total_apps(self):
        total = self.find_elements((By.CSS_SELECTOR, '.shuffle-list-item.gateway-item'))
        return len(total)
