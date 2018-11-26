# coding=utf-8

import unittest
from common.driver import *
from common import myunit
from test_case.page_obj.create_product_page import CreateProduct
from test_case.page_obj.product_info_page import ProductInfo
from test_case.page_obj.loginPage import Login
from test_case.page_obj.gateway_page import GatewayPage
from common import driver
from common import exceluitl as EX,  function as func
import sys, time
reload(sys)
sys.setdefaultencoding('utf-8')


class GatewayTest(unittest.TestCase):
    u'''新增产品'''
    data_path = func.find_path() + '/test_data/devplatform/gateway.xlsx'
    data_sheet = 'case'
    data_sheet1 = 'case1'
    data_sheet2 = 'case2'
    data_sheet3 = 'case3'
    data_sheet4 = 'case4'
    min_value = None
    max_value = None
    url = None
    url1 = None
    url2 = None

    # @classmethod
    # func.log(u'----------------------------------RegisterDeviceTest 开始-----------------------------------')
    # def setUpClass(cls):
    #     cls.driver = Broswer.get_instance()

    @classmethod
    def setUpClass(cls):
        func.log(u'----------------------------------RegisterDeviceTest 开始-----------------------------------')
        login_data_path = func.find_path() + '/test_data/login/login.xlsx'
        login_data_sheet = 'case'
        cls.driver = broswer_no_remote()
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        value_list = EX.get_case_list(login_data_path, login_data_sheet, 'test_login_success')
        obj1 = Login(cls.driver)
        obj1.user_login(username=value_list[0], password=value_list[1])
        time.sleep(2)
        obj1.wait_element_visible()
        time.sleep(2)

    def open_gateway_page(self):
        obj = ProductInfo(self.driver)
        obj1 = Login(self.driver)
        obj2 = CreateProduct(self.driver)
        obj3 = GatewayPage(self.driver)
        obj.open_url('#/apps/home')
        time.sleep(1)
        obj1.wait_element_visible()
        time.sleep(1)
        obj2.click_dev_plant()
        obj.wait_element_visible_by_class('title1')
        obj3.click_apps_gateway()
        time.sleep(1)
        obj3.wait_element_visible_by_css_with_text('.inline-middle.header-title', u'应用网关')

    def new_apps(self, value_list):
        obj = GatewayPage(self.driver)
        obj.click_new_app()
        obj.wait_dialog_visible()
        obj.input_app_name(value_list[0])
        obj.click_app_flag(int(value_list[1]))
        obj.input_app_desc(value_list[2])
        obj.click_button(u'完成并创建')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_create_ios_app') == u'否', u'跳过执行')
    def test_a1_create_ios_app(self):
        u'''创建ios应用'''
        func.log(u'--------------test_a1_create_ios_app 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_create_ios_app')
        try:
            obj = GatewayPage(self.driver)
            self.open_gateway_page()
            apps_num = obj.get_total_apps()
            self.new_apps(value_list)
            time.sleep(2)
            apps_num_new = obj.get_total_apps()
            self.assertEqual(apps_num, apps_num_new - 1)
        except Exception:
            func.log(u'【断言失败】：创建ios应用失败,应用总数没有增加')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a1_create_ios_app 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_create_android_app') == u'否', u'跳过执行')
    def test_a2_create_android_app(self):
        u'''创建android应用'''
        func.log(u'--------------test_a2_create_android_app 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_create_android_app')
        try:
            obj = GatewayPage(self.driver)
            self.open_gateway_page()
            apps_num = obj.get_total_apps()
            self.new_apps(value_list)
            time.sleep(2)
            apps_num_new = obj.get_total_apps()
            self.assertEqual(apps_num, apps_num_new - 1)
        except Exception:
            func.log(u'【断言失败】：创建android应用失败,应用总数没有增加')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a2_create_android_app 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_create_wechat_app') == u'否', u'跳过执行')
    def test_a3_create_wechat_app(self):
        u'''创建微信应用'''
        func.log(u'--------------test_a3_create_wechat_app 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_create_wechat_app')
        try:
            obj = GatewayPage(self.driver)
            self.open_gateway_page()
            apps_num = obj.get_total_apps()
            self.new_apps(value_list)
            time.sleep(2)
            apps_num_new = obj.get_total_apps()
            self.assertEqual(apps_num, apps_num_new - 1)
        except Exception:
            func.log(u'【断言失败】：创建微信应用失败,应用总数没有增加')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a3_create_wechat_app 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_create_connector_app') == u'否', u'跳过执行')
    def test_a4_create_connector_app(self):
        u'''创建连接器应用'''
        func.log(u'--------------test_a4_create_connector_app 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_create_connector_app')
        try:
            obj = GatewayPage(self.driver)
            self.open_gateway_page()
            apps_num = obj.get_total_apps()
            self.new_apps(value_list)
            time.sleep(2)
            apps_num_new = obj.get_total_apps()
            self.assertEqual(apps_num, apps_num_new - 1)
        except Exception:
            func.log(u'【断言失败】：创建连接器应用失败,应用总数没有增加')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a4_create_connector_app 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_create_other_app') == u'否', u'跳过执行')
    def test_a5_create_other_app(self):
        u'''创建其他应用'''
        func.log(u'--------------test_a5_create_other_app 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_create_other_app')
        try:
            obj = GatewayPage(self.driver)
            self.open_gateway_page()
            apps_num = obj.get_total_apps()
            self.new_apps(value_list)
            time.sleep(2)
            apps_num_new = obj.get_total_apps()
            self.assertEqual(apps_num, apps_num_new - 1)
        except Exception:
            func.log(u'【断言失败】：创建其他应用失败,应用总数没有增加')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a5_create_other_app 结束-------------')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(GatewayTest('test_a5_create_other_app'))
    runner = unittest.TextTestRunner()
    runner.run(suite)