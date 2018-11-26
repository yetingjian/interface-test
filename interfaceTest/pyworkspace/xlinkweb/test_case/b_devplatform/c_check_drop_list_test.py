# coding=utf-8

import unittest
from common.driver import *
from common import myunit
from test_case.page_obj.check_drop_list_page import CheckDropList
from test_case.page_obj.product_info_page import ProductInfo
from test_case.page_obj.loginPage import Login
from common import driver
from common import exceluitl as EX,  function as func
import sys, time
reload(sys)
sys.setdefaultencoding('utf-8')


class CheckDropListTest(unittest.TestCase):
    u'''新增产品'''
    data_path = func.find_path() + '/test_data/devplatform/check_drop_list.xlsx'
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
    # func.log(u'----------------------------------CheckDropListTest 开始-----------------------------------')
    # def setUpClass(cls):
    #     cls.driver = Broswer.get_instance()

    @classmethod
    def setUpClass(cls):
        func.log(u'----------------------------------CheckDropListTest 开始-----------------------------------')
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

    def open_base_page(self):
        obj = CheckDropList(self.driver)
        obj1 = Login(self.driver)
        obj.open_url('#/apps/home')
        time.sleep(1)
        obj1.wait_element_visible()
        time.sleep(1)

    def _search_product(self, value_list):
        obj = ProductInfo(self.driver)
        obj1 = Login(self.driver)
        obj.open_url('#/apps/home')
        time.sleep(1)
        obj1.wait_element_visible()
        time.sleep(1)
        obj.click_dev_plant()
        time.sleep(1)
        obj.wait_element_visible_by_class('title1')
        obj.click_button(u'查看所有产品')
        time.sleep(1)
        obj.wait_element_visible_by_class('main-title-content')
        obj.search_product(value_list)

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_set_base_page') == u'否', u'跳过执行')
    def test_a1_set_base_page(self):
        u'''设置为首页产品'''
        func.log(u'--------------test_b_set_base_page 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_set_base_page')
        try:
            obj1 = CheckDropList(self.driver)
            self._search_product(value_list)
            obj1.set_base_product()
            obj1.wait_message_visible()
            self.assertEqual(obj1.error_message(), u'设置成功')
        except Exception:
            func.log(u'【断言失败】：设置为首页产品后预期提示：' + u'设置成功')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_b_set_base_page 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_dev_platform_list') == u'否', u'跳过执行')
    def test_a2_dev_platform_list(self):
        u'''检查开发平台功能列表'''
        func.log(u'--------------test_a_dev_platform_list 开始-------------')
        func_list = [u'当前产品', u'最近浏览', u'其他功能', u'查看所有产品', u'创建产品', u'开发指南', u'物联网连接器',
                     u'应用网关', u'智能互联', u'物联云盘']
        try:
            obj1 = CheckDropList(self.driver)
            obj = ProductInfo(self.driver)
            self.open_base_page()
            obj1.click_dev_platform(u'开发平台')
            obj.wait_quota_visible()
            obj.click_quota()
            time.sleep(1)
            items = obj1.check_list_item(u'开发平台')
            for i in func_list:
                self.assertIn(i, items)
        except Exception:
            func.log(u'【断言失败】：开发平台下拉列表缺少：'+i)
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a_dev_platform_list 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_check_base_product') == u'否', u'跳过执行')
    def test_a3_check_base_product(self):
        u'''检查首页产品是否正确'''
        func.log(u'--------------test_a2_check_base_product 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_check_base_product')
        name = value_list[0] + func.get_now_date()
        try:
            obj1 = CheckDropList(self.driver)
            obj = ProductInfo(self.driver)
            self.open_base_page()
            obj1.click_dev_platform(u'开发平台')
            obj.wait_quota_visible()
            time.sleep(1)
            self.assertEqual(obj1.get_current_product_name(), name)
        except Exception:
            func.log(u'【断言失败】：首页产品预期为：'+ name)
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a2_check_base_product 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_check_classify') == u'否', u'跳过执行')
    def test_b1_check_classify(self):
        u'''检查导航栏中产品是否在分类中'''
        func.log(u'--------------test_b1_check_classify 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_check_classify')
        name = value_list[0] + func.get_now_date()
        try:
            obj1 = CheckDropList(self.driver)
            obj = ProductInfo(self.driver)
            self.open_base_page()
            obj1.click_dev_platform(u'开发平台')
            obj.wait_quota_visible()
            time.sleep(1)
            obj1.click_picker()
            obj1.click_picker_classify(value_list[1])
            self.assertTrue(obj1.check_product_in_list(name))
        except Exception:
            func.log(u'【断言失败】产品：' + name + u'不在分类 '+value_list[1]+u'中')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_b1_check_classify 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_picker_search_product') == u'否', u'跳过执行')
    def test_b2_picker_search_product(self):
        u'''导航栏中搜索产品'''
        func.log(u'--------------test_b2_picker_search_product 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_picker_search_product')
        name = value_list[0] + func.get_now_date()
        try:
            obj1 = CheckDropList(self.driver)
            obj = ProductInfo(self.driver)
            self.open_base_page()
            obj1.click_dev_platform(u'开发平台')
            obj.wait_quota_visible()
            time.sleep(1)
            obj1.click_picker()
            self.assertTrue(obj1.search_product(name))
        except Exception:
            func.log(u'【断言失败】搜索产品：' + name + u'未找到')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_b2_picker_search_product 结束-------------')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(CheckDropListTest('test_b2_picker_search_product'))
    #suite.addTest(ProductInfoTest('test_h1_config_attr'))
    runner = unittest.TextTestRunner()
    runner.run(suite)