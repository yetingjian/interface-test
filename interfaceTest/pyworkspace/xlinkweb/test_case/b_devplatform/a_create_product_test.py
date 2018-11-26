# coding=utf-8

import unittest
from common.driver import *
from common import myunit
from test_case.page_obj.create_product_page import CreateProduct
from test_case.page_obj.loginPage import Login
from common import driver
from common import exceluitl as EX,  function as func
import sys, time
import gc
reload(sys)
sys.setdefaultencoding('utf-8')


class CreateProductTest(unittest.TestCase):
    u'''新增产品'''
    data_path = func.find_path() + '/test_data/devplatform/create_product.xlsx'
    data_sheet = 'case'
    data_sheet1 = 'case1'
    data_sheet2 = 'case2'
    data_sheet3 = 'case3'
    data_sheet4 = 'case4'
    min_value = None
    max_value = None
    #obj1 = None
    url = 'http://test.xlink.cn/v5/#/apps/develop/create-product/1607d2b68e5d00011607d2b68e5d4401/data-points'
    url1 = 'http://test.xlink.cn/v5/#/apps/develop/create-product/1607d2b666c100011607d2b666c14a01/data-points'
    url2 = 'http://test.xlink.cn/v5/#/apps/develop/create-product/1607d2b666c100011607d2b666c14a01/data-points'

    # @classmethod
    # def setUpClass(cls):
    #     func.log(u'----------------------------------CreateProductTest 开始-----------------------------------')
    #     cls.driver = Broswer.get_instance()

    @classmethod
    def setUpClass(cls):
        func.log(u'----------------------------------CreateProductTest 开始-----------------------------------')
        login_data_path = func.find_path() + '/test_data/login/login.xlsx'
        login_data_sheet = 'case'
        cls.driver = broswer_no_remote()
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        value_list = EX.get_case_list(login_data_path, login_data_sheet, 'test_login_success')
        obj = Login(cls.driver)
        obj.user_login(username=value_list[0], password=value_list[1])
        time.sleep(2)
        obj.wait_element_visible()
        time.sleep(2)
        
    def setUp(self):
        self.obj1 = CreateProduct(self.driver)
        
    def tearDown(self):
        del self.obj1
        gc.collect()

    def new_product(self, value_list):
        obj = CreateProduct(self.driver)
        obj.open_home_page()
        time.sleep(1)
        # obj.click_main_tab(u'开发平台')
        # obj.wait_add_product_visible()
        obj.click_dev_plant()
        obj.wait_element_visible_by_class('title1')
        obj.click_add_product()
        time.sleep(1)
        # obj.wait_button_visibled(u'立即创建产品')
        # obj.click_button(u'立即创建产品')
        obj.wait_element_visible_by_css('.tab-s2-key.active.unclickable')
        if value_list[0] != '':
            value_list[0] = value_list[0] + func.get_now_date()
        obj.input_text(u'产品名称', value_list[0])
        obj.input_text(u'产品型号', value_list[1])
        obj.select_text1(u'产品分类', value_list[2])
        obj.select_text2(u'连接类型', value_list[3])
        obj.is_gateway(value_list[4])
        obj.click_button(u'下一步')
        del obj

    def add_data_point(self, value_list1, case_name):
        obj = CreateProduct(self.driver)
        obj.click_button(u'添加数据端点')
        obj.wait_button_disabled_css(u'添加数据端点')
        obj.point_type_select(u'端点类型', value_list1[0], 'devplatform/' + case_name)
        if value_list1[0] == u'系统':
            obj.sys_point_id_select(u'字段名称', value_list1[1], 'devplatform/' + case_name)
            obj.input_point_name(value_list1[2])
            obj.input_descript(value_list1[7])
        else:
            obj.input_point_id(value_list1[1])
            obj.input_point_name(value_list1[2])
            obj.data_type_select(u'数据类型', value_list1[3], 'devplatform/' + case_name)
            if value_list1[3]!=u'布尔类型' and value_list1[3]!=u'字符串' and value_list1[3]!='':
                CreateProductTest.min_value = str(obj.get_min_value())
                CreateProductTest.max_value = str(obj.get_max_value())
            obj.input_min_value(value_list1[4])
            obj.input_max_value(value_list1[5])
            if value_list1[3] != u'布尔类型' and value_list1[3] != '':
                obj.input_unit(value_list1[6])
            obj.input_descript(value_list1[7])
            obj.read_select(u'读写', value_list1[8], 'devplatform/' + case_name)
        obj.click_save(u'保存')
        time.sleep(1)
        del obj

    def open_mod_page(self):
        #obj1 = CreateProduct(self.driver)
        self.obj1.open_home_page()
        self.obj1.open_url_with_host(CreateProductTest.url2)
        self.obj1.wait_button_css_visible()
        time.sleep(1)
        self.obj1.click_button(u'按设备类型匹配')
        self.obj1.wait_mod_page_displayed()
        time.sleep(1)

    def open_data_point_edit_page(self):
        #obj1 = CreateProduct(self.driver)
        self.obj1.open_home_page()
        self.obj1.open_url_with_host(CreateProductTest.url1)
        time.sleep(1)
        self.obj1.wait_button_css_visible()
        time.sleep(1)

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_create_product_success') == u'否', u'跳过执行')
    def test_a_create_product_success(self):
        u'''创建产品成功'''
        func.log(u'--------------test_a_create_product_success 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_create_product_success')
        try:
            self.new_product(value_list)
            time.sleep(1)
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            CreateProductTest.url = self.obj1.get_current_url()
            self.obj1.click_button(u'匹配完成，下一步')
            time.sleep(1)
            self.obj1.wait_success_tips_visible()
            self.assertEqual(self.obj1.create_success_message(), value_list[5])
        except Exception:
            func.log(u'【断言失败】创建产品成功后预期提示信息为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a_create_product_success 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_only_product_name') == u'否', u'跳过执行')
    def test_a_only_product_name(self):
        u'''创建产品只输入产品名称'''
        func.log(u'--------------test_a_only_product_name 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_only_product_name')
        try:
            self.new_product(value_list)
            time.sleep(1)
            self.obj1.click_button(u'匹配完成，下一步')
            time.sleep(1)
            self.obj1.wait_success_tips_visible()
            self.assertEqual(self.obj1.create_success_message(), value_list[5])
        except Exception:
            func.log(u'【断言失败】创建产品成功后预期提示信息为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a_only_product_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_product_is_gateway') == u'否', u'跳过执行')
    def test_a_product_is_gateway(self):
        u'''创建网关产品'''
        func.log(u'--------------test_a_product_is_gateway 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_product_is_gateway')
        try:
            self.new_product(value_list)
            time.sleep(1)
            self.obj1.click_button(u'匹配完成，下一步')
            time.sleep(1)
            self.obj1.wait_success_tips_visible()
            self.assertEqual(self.obj1.create_success_message(), value_list[5])
        except Exception:
            func.log(u'【断言失败】创建产品成功后预期提示信息为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a_product_is_gateway 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_skip_data_point') == u'否', u'跳过执行')
    def test_a_skip_data_point(self):
        u'''跳过数据端点配置'''
        func.log(u'--------------test_a_skip_data_point 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_skip_data_point')
        try:
            self.new_product(value_list)
            time.sleep(1)
            CreateProductTest.url2 = self.obj1.get_current_url()
            self.obj1.click_button(u'跳过')
            time.sleep(1)
            self.obj1.wait_success_tips_visible()
            self.assertEqual(self.obj1.create_success_message(), value_list[5])
        except Exception:
            func.log(u'【断言失败】创建产品成功后预期提示信息为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a_skip_data_point 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_empty_product_name') == u'否', u'跳过执行')
    def test_b_empty_product_name(self):
        u'''创建产品名称为空'''
        func.log(u'--------------test_b_empty_product_name 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_empty_product_name')
        try:
            self.new_product(value_list)
            time.sleep(1)
            self.assertEqual(self.obj1.get_error_message(u'产品名称'), value_list[5])
        except Exception:
            func.log(u'【断言失败】产品名称为空预期提示信息为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_b_empty_product_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet1, 'test_empty_point_id') == u'否', u'跳过执行')
    def test_b_empty_point_ID(self):
        u'''字段名称为空'''
        func.log(u'--------------test_b_empty_point_ID 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_empty_point_id')
        try:
            self.obj1.open_url_with_host(CreateProductTest.url)
            time.sleep(3)
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list1, sys._getframe().f_code.co_name)
            self.obj1.wait_error_message_visible()
            self.assertEqual(self.obj1.error_message(), value_list1[9])
            self.obj1.click_button(u'匹配完成，下一步')
        except Exception:
            func.log(u'【断言失败】字段名称为空预期提示信息为：' + value_list1[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_b_empty_point_ID 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet1, 'test_error_point_id') == u'否', u'跳过执行')
    def test_b_error_point_id(self):
        u'''数据端点输入非法'''
        func.log(u'--------------test_b_error_point_id 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_error_point_id')
        try:
            self.obj1.open_url_with_host(CreateProductTest.url)
            time.sleep(3)
            self.obj1.wait_add_data_point_button_visible()
            time.sleep(1)
            self.add_data_point(value_list1, sys._getframe().f_code.co_name)
            self.obj1.wait_error_message_visible()
            self.assertEqual(self.obj1.error_message(), value_list1[9])
            self.obj1.click_cancel(u'取消')
            self.obj1.click_button(u'匹配完成，下一步')
        except Exception:
            func.log(u'【断言失败】数据端点输入非法预期提示信息为：' + value_list1[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_b_error_point_id 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet1, 'test_existed_point_id') == u'否', u'跳过执行')
    def test_b_existed_point_id(self):
        u'''数据端点重复'''
        func.log(u'--------------test_b_existed_point_id 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_existed_point_id')
        try:
            self.obj1.open_url_with_host(CreateProductTest.url)
            time.sleep(2)
            self.obj1.wait_button_css_visible()
            self.add_data_point(value_list1, sys._getframe().f_code.co_name)
            time.sleep(1)
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list1, sys._getframe().f_code.co_name)
            self.obj1.wait_error_message_visible()
            self.assertEqual(self.obj1.error_message(), value_list1[9])
            self.obj1.click_button(u'匹配完成，下一步')
        except Exception:
            func.log(u'【断言失败】数据端点重复预期提示信息为：' + value_list1[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_b_existed_point_id 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet1, 'test_empty_point_name') == u'否', u'跳过执行')
    def test_b_empty_point_name(self):
        u'''端点名称为空'''
        func.log(u'--------------test_b_empty_point_name 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_empty_point_name')
        try:
            self.obj1.open_url_with_host(CreateProductTest.url)
            time.sleep(3)
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list1, sys._getframe().f_code.co_name)
            self.obj1.wait_error_message_visible()
            self.assertEqual(self.obj1.error_message(), value_list1[9])
            self.obj1.click_button(u'匹配完成，下一步')
        except Exception:
            func.log(u'【断言失败】端点名称为空预期提示信息为：' + value_list1[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_b_empty_point_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet1, 'test_add_sys_point') == u'否', u'跳过执行')
    def test_bb_add_sys_point(self):
        u'''添加系统数据端点'''
        func.log(u'--------------test_add_sys_point 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_add_data_point_4')
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_add_sys_point')
        try:
            self.new_product(value_list)
            time.sleep(1)
            self.add_data_point(value_list1, sys._getframe().f_code.co_name)
            time.sleep(1)
            result = self.obj1.get_point_id_value("0")
            self.assertEqual(result, value_list1[9])
            func.log(u'添加系统数据端点成功')
        except Exception:
            func.log(u'【断言失败】添加系统数据端预期结果为：' + value_list1[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_add_sys_point 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_add_data_type_all') == u'否', u'跳过执行')
    def test_bb_add_all_data_type(self):
        u'''添加所有数据类型端点'''
        func.log(u'--------------test_add_all_data_type 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_add_data_type_all')
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_data_type_1')
        value_list2 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_data_type_2')
        value_list3 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_data_type_3')
        value_list4 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_data_type_4')
        value_list5 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_data_type_5')
        value_list6 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_data_type_6')
        value_list7 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_data_type_7')
        value_list8 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_data_type_8')
        try:
            self.new_product(value_list)
            time.sleep(1)
            self.obj1.wait_add_data_point_button_visible()
            time.sleep(1)
            CreateProductTest.url1 = self.obj1.get_current_url()
            self.add_data_point(value_list1, sys._getframe().f_code.co_name)
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list2, sys._getframe().f_code.co_name)
            self.assertEqual(CreateProductTest.min_value, value_list2[9].split(',')[0])
            func.log(u'该数据类型最小值显示验证通过')
            self.assertEqual(CreateProductTest.max_value, value_list2[9].split(',')[1])
            func.log(u'该数据类型最大值显示验证通过')
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list3, sys._getframe().f_code.co_name)
            self.assertEqual(CreateProductTest.min_value, value_list3[9].split(',')[0])
            func.log(u'该数据类型最小值显示验证通过')
            self.assertEqual(CreateProductTest.max_value, value_list3[9].split(',')[1])
            func.log(u'该数据类型最大值显示验证通过')
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list4, sys._getframe().f_code.co_name)
            self.assertEqual(CreateProductTest.min_value, value_list4[9].split(',')[0])
            func.log(u'该数据类型最小值显示验证通过')
            self.assertEqual(CreateProductTest.max_value, value_list4[9].split(',')[1])
            func.log(u'该数据类型最大值显示验证通过')
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list5, sys._getframe().f_code.co_name)
            self.assertEqual(CreateProductTest.min_value, value_list5[9].split(',')[0])
            func.log(u'该数据类型最小值显示验证通过')
            self.assertEqual(CreateProductTest.max_value, value_list5[9].split(',')[1])
            func.log(u'该数据类型最大值显示验证通过')
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list6, sys._getframe().f_code.co_name)
            self.assertEqual(CreateProductTest.min_value, value_list6[9].split(',')[0])
            func.log(u'该数据类型最小值显示验证通过')
            self.assertEqual(CreateProductTest.max_value, value_list6[9].split(',')[1])
            func.log(u'该数据类型最大值显示验证通过')
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list7, sys._getframe().f_code.co_name)
            self.assertEqual(CreateProductTest.min_value, value_list7[9].split(',')[0])
            func.log(u'该数据类型最小值显示验证通过')
            self.assertEqual(CreateProductTest.max_value, value_list7[9].split(',')[1])
            func.log(u'该数据类型最大值显示验证通过')
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list8, sys._getframe().f_code.co_name)
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(2)
            count = self.obj1.count_data_point()
            self.assertEqual(count, 8)
        except Exception:
            func.log(u'【断言失败】数据类型添加失败，预期数据端点数：8')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_add_all_data_type 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet1, 'test_error_min_value1') == u'否', u'跳过执行')
    def test_bb_error_min_max_value(self):
        u'''数据类型取值范围错误'''
        func.log(u'--------------test_error_min_max_value 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_error_min_value1')
        value_list2 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_error_max_value1')
        value_list3 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_error_min_value2')
        value_list4 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_error_max_value2')
        value_list5 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_error_min_value3')
        value_list6 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_error_max_value3')
        value_list7 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_error_min_value4')
        value_list8 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_error_max_value4')
        value_list9 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_error_min_value5')
        value_list10 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_error_max_value5')
        value_list11 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_error_min_value6')
        value_list12 = EX.get_case_list(self.data_path, self.data_sheet1, 'test_error_max_value6')
        try:
            self.obj1.open_url_with_host(CreateProductTest.url)
            time.sleep(3)
            self.obj1.wait_add_data_point_button_visible()
            time.sleep(1)
            self.add_data_point(value_list1, sys._getframe().f_code.co_name)
            self.assertEqual(self.obj1.error_message(), value_list1[9])
            self.obj1.click_cancel(u'取消')
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list2, sys._getframe().f_code.co_name)
            self.assertEqual(self.obj1.error_message(), value_list2[9])
            self.obj1.click_cancel(u'取消')
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list3, sys._getframe().f_code.co_name)
            self.assertEqual(self.obj1.error_message(), value_list3[9])
            self.obj1.click_cancel(u'取消')
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list4, sys._getframe().f_code.co_name)
            self.assertEqual(self.obj1.error_message(), value_list4[9])
            self.obj1.click_cancel(u'取消')
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list5, sys._getframe().f_code.co_name)
            self.assertEqual(self.obj1.error_message(), value_list5[9])
            self.obj1.click_cancel(u'取消')
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list6, sys._getframe().f_code.co_name)
            self.assertEqual(self.obj1.error_message(), value_list6[9])
            self.obj1.click_cancel(u'取消')
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list7, sys._getframe().f_code.co_name)
            self.assertEqual(self.obj1.error_message(), value_list7[9])
            self.obj1.click_cancel(u'取消')
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list8, sys._getframe().f_code.co_name)
            self.assertEqual(self.obj1.error_message(), value_list8[9])
            self.obj1.click_cancel(u'取消')
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list9, sys._getframe().f_code.co_name)
            self.assertEqual(self.obj1.error_message(), value_list9[9])
            self.obj1.click_cancel(u'取消')
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list10, sys._getframe().f_code.co_name)
            self.assertEqual(self.obj1.error_message(), value_list10[9])
            self.obj1.click_cancel(u'取消')
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list11, sys._getframe().f_code.co_name)
            self.assertEqual(self.obj1.error_message(), value_list11[9])
            self.obj1.click_cancel(u'取消')
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            self.add_data_point(value_list12, sys._getframe().f_code.co_name)
            self.assertEqual(self.obj1.error_message(), value_list12[9])
            self.obj1.click_cancel(u'取消')
        except Exception:
            func.log(u'【断言失败】数据类型取值范围提示，预期提示信息为：'+value_list1[9]+','+value_list2[8])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_error_min_max_value 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_edit_point_id') == u'否', u'跳过执行')
    def test_c1_edit_point_id(self):
        u'''编辑字段名称'''
        func.log(u'--------------test_c_edit_point_id 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet2, 'test_edit_point_id')
        try:
            self.open_data_point_edit_page()
            self.obj1.edit_data_point(value_list1, sys._getframe().f_code.co_name)
            time.sleep(1)
            value = self.obj1.get_point_id_value(value_list1[0])
            self.assertEqual(value, value_list1[10])
        except Exception:
            func.log(u'【断言失败】字段名称预期结果为：' + value_list1[10])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_c_edit_point_id 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_edit_existed_point_id') == u'否', u'跳过执行')
    def test_c2_edit_existed_point_id(self):
        u'''编辑已存在字段名称'''
        func.log(u'--------------test_c_edit_existed_point_id 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet2, 'test_edit_existed_point_id')
        try:
            self.open_data_point_edit_page()
            self.obj1.edit_data_point(value_list1, sys._getframe().f_code.co_name)
            self.obj1.wait_error_message_visible()
            self.assertEqual(self.obj1.error_message(), value_list1[10])
        except Exception:
            func.log(u'【断言失败】字段名称已存在预期提示为：' + value_list1[10])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_c_edit_existed_point_id 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_edit_error_point_id') == u'否', u'跳过执行')
    def test_c3_edit_error_point_id(self):
        u'''编辑错误格式的字段名称'''
        func.log(u'--------------test_c_edit_error_point_id 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet2, 'test_edit_error_point_id')
        try:
            self.open_data_point_edit_page()
            self.obj1.edit_data_point(value_list1, sys._getframe().f_code.co_name)
            self.obj1.wait_error_message_visible()
            self.assertEqual(self.obj1.error_message(), value_list1[10])
        except Exception:
            func.log(u'【断言失败】字段名称已存在预期提示为：' + value_list1[10])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_c_edit_error_point_id 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_edit_unit') == u'否', u'跳过执行')
    def test_c4_edit_unit(self):
        u'''编辑数据端点单位'''
        func.log(u'--------------test_c_edit_unit 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet2, 'test_edit_unit')
        try:
            self.open_data_point_edit_page()
            self.obj1.edit_data_point(value_list1, sys._getframe().f_code.co_name)
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            result = self.obj1.get_unit_value()
            self.assertEqual(result, value_list1[10])
        except Exception:
            func.log(u'【断言失败】数据端点单位预期结果为：' + value_list1[10])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_c_edit_unit 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_edit_unit_length') == u'否', u'跳过执行')
    def test_c5_edit_unit_length(self):
        u'''编辑数据端点单位长度限制'''
        func.log(u'--------------test_c_edit_unit_length 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet2, 'test_edit_unit_length')
        try:
            self.open_data_point_edit_page()
            self.obj1.edit_data_point(value_list1, sys._getframe().f_code.co_name)
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            result = self.obj1.get_unit_value()
            self.assertEqual(result, value_list1[10])
        except Exception:
            func.log(u'【断言失败】数据端点单位预期结果为：' + value_list1[10])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_c_edit_unit_length 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_edit_cancel') == u'否', u'跳过执行')
    def test_c6_edit_cancel(self):
        u'''编辑数据端点点击取消'''
        func.log(u'--------------test_c_edit_cancel 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet2, 'test_edit_cancel')
        try:
            self.open_data_point_edit_page()
            self.obj1.edit_data_point(value_list1, sys._getframe().f_code.co_name)
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(1)
            result = self.obj1.get_unit_value()
            self.assertNotEqual(result, value_list1[10])
        except Exception:
            func.log(u'【断言失败】数据端点单位预期结果为：' + value_list1[10])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_c_edit_cancel 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_edit_empty_point_name') == u'否', u'跳过执行')
    def test_c7_edit_empty_point_name(self):
        u'''编辑端点名称为空'''
        func.log(u'--------------test_c7_edit_empty_point_name 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet2, 'test_edit_empty_point_name')
        try:
            self.open_data_point_edit_page()
            self.obj1.edit_data_point(value_list1, sys._getframe().f_code.co_name)
            time.sleep(1)
            self.assertEqual(self.obj1.error_message(), value_list1[10])
        except Exception:
            func.log(u'【断言失败】端点名称为空预期结果为：' + value_list1[10])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_c7_edit_empty_point_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_edit_delete') == u'否', u'跳过执行')
    def test_d_edit_delete(self):
        u'''删除数据端点'''
        func.log(u'--------------test_d_edit_delete 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet2, 'test_edit_delete')
        try:
            self.open_data_point_edit_page()
            self.obj1.delete_data_point(value_list1)
            time.sleep(1)
            count = self.obj1.count_data_point()
            self.assertEqual(str(count), value_list1[10])
        except Exception:
            func.log(u'【断言失败】数据端点剩余数量预期结果为：' + value_list1[10])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_d_edit_delete 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_edit_delete_cancle') == u'否', u'跳过执行')
    def test_d_edit_delete_cancle(self):
        u'''取消删除数据端点'''
        func.log(u'--------------test_d_edit_delete_cancle 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet2, 'test_edit_delete_cancle')
        try:
            self.open_data_point_edit_page()
            self.obj1.delete_data_point(value_list1)
            time.sleep(1)
            count = self.obj1.count_data_point()
            self.assertEqual(str(count), value_list1[10])
        except Exception:
            func.log(u'【断言失败】数据端点剩余数量预期结果为：' + value_list1[10])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_d_edit_delete_cancle 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_mod_library_save_as_custom_mod') == u'否', u'跳过执行')
    def test_e1_mod_library_save_as_custom_mod(self):
        u'''系统数据模板存为自定义模板'''
        func.log(u'--------------test_e1_mod_library_save_as_custom_mod 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet3, 'test_mod_library_save_as_custom_mod')
        try:
            self.open_mod_page()
            self.obj1.save_as_custom_mod(value_list1)
            self.assertTrue(self.obj1.check_new_custom_mod_point_num(value_list1), CreateProduct.mod_data_point_count)
        except Exception:
            func.log(u'【断言失败】自定义模板的数据端点个数预期结果为：'+str(CreateProduct.mod_data_point_count))
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e1_mod_library_save_as_custom_mod 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_mod_library_save_cancel_custom_mod') == u'否', u'跳过执行')
    def test_e2_mod_library_save_cancel_custom_mod(self):
        u'''取消系统数据模板存为自定义模板'''
        func.log(u'--------------test_e2_mod_library_save_cancel_custom_mod 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet3, 'test_mod_library_save_cancel_custom_mod')
        try:
            self.open_mod_page()
            num = self.obj1.get_mod_count()
            self.obj1.save_as_custom_mod(value_list1)
            time.sleep(1)
            num2 = self.obj1.get_mod_count()
            self.assertEqual(num, num2)
        except Exception:
            func.log(u'【断言失败】：存为自定义模板取消后模板数量有误，预期结果为'+str(num))
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e2_mod_library_save_cancel_custom_mod 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_mod_library_accept_mod_success') == u'否',u'跳过执行')
    def test_e3_mod_library_accept_mod_success(self):
        u'''应用模板'''
        func.log(u'--------------test_e3_mod_library_accept_mod_success 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet3, 'test_mod_library_accept_mod_success')
        try:
            self.open_mod_page()
            self.obj1.accept_mod(value_list1)
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(2)
            count = self.obj1.count_data_point()
            self.assertEqual(count, CreateProduct.mod_data_point_count)
        except Exception:
            func.log(u'【断言失败】：应用模板后数据端点数量有误，预期结果为'+str(CreateProduct.mod_data_point_count))
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e3_mod_library_accept_mod_success 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_mod_library_accept_mod_cancel') == u'否',
                     u'跳过执行')
    def test_e4_mod_library_accept_mod_cancel(self):
        u'''取消应用模板'''
        func.log(u'--------------test_e4_mod_library_accept_mod_cancel 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet3, 'test_mod_library_accept_mod_cancel')
        try:
            self.open_mod_page()
            self.obj1.accept_mod(value_list1)
            time.sleep(2)
            result = self.obj1.wait_mod_page_displayed()
            self.assertEqual(result, True)
        except Exception:
            func.log(u'【断言失败】：取消应用模板后页面不应跳转')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e4_mod_library_accept_mod_cancel 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_mod_library_create_custom_mod') == u'否',
                     u'跳过执行')
    def test_e5_mod_library_create_custom_mod(self):
        u'''创建自定义模板'''
        func.log(u'--------------test_e5_mod_library_create_custom_mod 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet3, 'test_mod_library_create_custom_mod')
        try:
            self.open_mod_page()
            num = self.obj1.get_mod_count()
            self.obj1.add_custom_mod(value_list1)
            time.sleep(2)
            num2 = self.obj1.get_mod_count()
            self.assertEqual(num, num2 - 1)
        except Exception:
            func.log(u'【断言失败】：创建自定义模板成功后模板数量预期为：' + str(num))
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e5_mod_library_create_custom_mod 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_mod_library_accept_mod_attribute') == u'否',
                     u'跳过执行')
    def test_e6_mod_library_accept_mod_attribute(self):
        u'''模板数据端点为空时应用模板不可用'''
        func.log(u'--------------test_e6_mod_library_accept_mod_attribute 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet3, 'test_mod_library_accept_mod_attribute')
        try:
            self.open_mod_page()
            self.obj1.accept_mod(value_list1)
            result = self.obj1.get_button_attribute(u'应用', 'disabled')
            self.assertEqual(result, 'true')
        except Exception:
            func.log(u'【断言失败】：模板数据端点为空时应用模板disabled属性不正确')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e6_mod_library_accept_mod_attribute 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_mod_library_create_custom_mod_cancel') == u'否',
                     u'跳过执行')
    def test_e7_mod_library_create_custom_mod_cancel(self):
        u'''取消创建自定义模板'''
        func.log(u'--------------test_e7_mod_library_create_custom_mod_cancel 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet3, 'test_mod_library_create_custom_mod_cancel')
        try:
            self.open_mod_page()
            num = self.obj1.get_mod_count()
            self.obj1.add_custom_mod(value_list1)
            time.sleep(2)
            num2 = self.obj1.get_mod_count()
            self.assertEqual(num, num2)
        except Exception:
            func.log(u'【断言失败】：取消创建自定义模板后模板数量预期为：' + str(num))
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e7_mod_library_create_custom_mod_cancel 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_mod_library_edit_custom_mod') == u'否',
                     u'跳过执行')
    def test_e8_mod_library_edit_custom_mod(self):
        u'''编辑自定义模板'''
        func.log(u'--------------test_e8_mod_library_edit_custom_mod 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet3, 'test_mod_library_edit_custom_mod')
        try:
            self.open_mod_page()
            self.obj1.edit_custom_mod_name(value_list1)
            time.sleep(2)
            result = self.obj1.check_mod_name_edit(value_list1)
            self.assertTrue(result, True)
        except Exception:
            func.log(u'【断言失败】：编辑模板后名称预期为：' + (value_list1[2] + "edited"))
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e8_mod_library_edit_custom_mod 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_mod_library_delete_custom_mod') == u'否',
                     u'跳过执行')
    def test_e9_mod_library_delete_custom_mod(self):
        u'''删除自定义模板'''
        func.log(u'--------------test_e9_mod_library_delete_custom_mod 开始-------------')
        num2 = None
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet3, 'test_mod_library_delete_custom_mod')
        try:
            self.open_mod_page()
            num = self.obj1.get_mod_count()
            self.obj1.delete_custom_mod(value_list1)
            time.sleep(2)
            num2 = self.obj1.get_mod_count()
            self.assertEqual(num, num2 + 1)
        except Exception:
            func.log(u'【断言失败】：删除自定义模板后模板数量预期为：' + str(num2))
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e9_mod_library_delete_custom_mod 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet4, 'test_mod_library_add_data_point') == u'否',
                     u'跳过执行')
    def test_f_mod_library_add_data_point(self):
        u'''自定义模板添加数据端点'''
        func.log(u'--------------test_f_mod_library_add_data_point 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet4, 'test_mod_library_add_data_point')
        try:
            self.open_mod_page()
            self.obj1.mod_library_add_data_point(value_list1, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            time.sleep(2)
            count = self.obj1.count_mod_data_point()
            self.assertEqual(count, CreateProduct.mod_data_point_count + 1)
        except Exception:
            func.log(u'【断言失败】：自定义模板数据端点数量预期为：' + str(count))
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_f_mod_library_add_data_point 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet4, 'test_mod_library_add_empty_point_ID') == u'否',
                     u'跳过执行')
    def test_g1_mod_library_add_empty_point_ID(self):
        u'''自定义模板添加数据端点-字段名称为空'''
        func.log(u'--------------test_g1_mod_library_add_empty_point_ID 开始-------------')
        
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet4, 'test_mod_library_add_empty_point_ID')
        try:
            self.open_mod_page()
            self.obj1.mod_library_add_data_point(value_list1, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            time.sleep(1)
            self.assertEqual(self.obj1.get_error_message(u'字段名称'), value_list1[13])
        except Exception:
            func.log(u'【断言失败】：数据端点为空时预期提示为：' + value_list1[13])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_g1_mod_library_add_empty_point_ID 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet4, 'test_mod_library_add_empty_point_name') == u'否',
                     u'跳过执行')
    def test_g1_mod_library_add_empty_point_name(self):
        u'''自定义模板添加数据端点-端点名称为空'''
        func.log(u'--------------test_g1_mod_library_add_empty_point_name 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet4, 'test_mod_library_add_empty_point_name')
        try:
            self.open_mod_page()
            self.obj1.mod_library_add_data_point(value_list1, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            time.sleep(1)
            self.assertEqual(self.obj1.get_error_message(u'端点名称'), value_list1[13])
        except Exception:
            func.log(u'【断言失败】：端点名称为空时预期提示为：' + value_list1[13])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_g1_mod_library_add_empty_point_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet4, 'test_mod_library_add_existed_point') == u'否',
                     u'跳过执行')
    def test_g2_mod_library_add_existed_point(self):
        u'''自定义模板添加数据端点-字段名称已存在'''
        func.log(u'--------------test_g2_mod_library_add_existed_point 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet4, 'test_mod_library_add_existed_point')
        try:
            self.open_mod_page()
            self.obj1.mod_library_add_data_point(value_list1, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            self.assertEqual(self.obj1.error_message(), value_list1[13])
        except Exception:
            func.log(u'【断言失败】：字段名称已存在时预期提示为：' + value_list1[13])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_g2_mod_library_add_existed_point 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet4, 'test_mod_library_add_existed_index') == u'否',
                     u'跳过执行')
    def test_g3_mod_library_add_existed_index(self):
        u'''自定义模板添加数据端点-索引已存在'''
        func.log(u'--------------test_g3_mod_library_add_existed_index 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet4, 'test_mod_library_add_existed_index')
        try:
            self.open_mod_page()
            self.obj1.mod_library_add_data_point(value_list1, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            self.assertEqual(self.obj1.error_message(), value_list1[13])
        except Exception:
            func.log(u'【断言失败】：索引已存在时预期提示为：' + value_list1[13])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_g3_mod_library_add_existed_index 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet4, 'test_mod_library_add_sys_data_point') == u'否',
                     u'跳过执行')
    def test_g4_mod_library_add_sys_data_point(self):
        u'''自定义模板添加系统数据端点'''
        func.log(u'--------------test_g4_mod_library_add_sys_data_point 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet4, 'test_mod_library_add_sys_data_point')
        try:
            self.open_mod_page()
            self.obj1.mod_library_add_data_point(value_list1, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            time.sleep(2)
            count = self.obj1.count_mod_data_point()
            self.assertEqual(count, CreateProduct.mod_data_point_count + 1)
        except Exception:
            func.log(u'【断言失败】：自定义模板数据端点数量预期为：' + str(count))
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_g4_mod_library_add_sys_data_point 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet4, 'test_mod_library_add_data_point_formula') == u'否',
                     u'跳过执行')
    def test_g5_mod_library_add_data_point_formula(self):
        u'''自定义模板添加数据端点_数据来源公式计算'''
        func.log(u'--------------test_g5_mod_library_add_data_point_formula 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet4, 'test_mod_library_add_data_point_formula')
        try:
            self.open_mod_page()
            self.obj1.mod_library_add_data_point(value_list1, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            time.sleep(2)
            count = self.obj1.count_mod_data_point()
            self.assertEqual(count, CreateProduct.mod_data_point_count + 1)
        except Exception:
            func.log(u'【断言失败】：自定义模板数据端点数量预期为：' + str(count))
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_g5_mod_library_add_data_point_formula 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet4, 'test_mod_library_add_data_point_empty_formula') == u'否',
                     u'跳过执行')
    def test_g6_mod_library_add_data_point_empty_formula(self):
        u'''自定义模板添加数据端点-公式为空'''
        func.log(u'--------------test_g6_mod_library_add_data_point_empty_formula 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet4, 'test_mod_library_add_data_point_empty_formula')
        try:
            self.open_mod_page()
            self.obj1.mod_library_add_data_point(value_list1, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            time.sleep(1)
            self.assertEqual(self.obj1.get_error_message(u'计算公式'), value_list1[13])
        except Exception:
            func.log(u'【断言失败】：公式为空时预期提示为：' + value_list1[13])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_g6_mod_library_add_data_point_empty_formula 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet4, 'test_mod_library_edit_data_point') == u'否',u'跳过执行')
    def test_h1_mod_library_edit_data_point(self):
        u'''编辑自定义模板数据端点ID'''
        func.log(u'--------------test_h1_mod_library_edit_data_point 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet4, 'test_mod_library_edit_data_point')
        try:
            self.open_mod_page()
            self.obj1.mod_library_add_data_point(value_list1, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            time.sleep(4)
            result = self.obj1.get_mod_library_point_id_value()
            self.assertEqual(result, value_list1[13])
        except Exception:
            func.log(u'【断言失败】：数据端点ID预期结果为：' + value_list1[13])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_h1_mod_library_edit_data_point 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet4, 'test_mod_library_delete_data_point') == u'否', u'跳过执行')
    def test_h2_mod_library_delete_data_point(self):
        u'''删除自定义模板数据端点'''
        func.log(u'--------------test_h2_mod_library_delete_data_point 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet4, 'test_mod_library_delete_data_point')
        try:
            self.open_mod_page()
            self.obj1.mod_library_add_data_point(value_list1, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            time.sleep(4)
            count = self.obj1.count_mod_data_point()
            self.assertEqual(count, CreateProduct.mod_data_point_count - 1)
        except Exception:
            func.log(u'【断言失败】：删除数据端点后预期记录数为：' + str(count))
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_h2_mod_library_delete_data_point 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_mod_library_accept_custom_mod_success') == u'否', u'跳过执行')
    def test_i_mod_library_accept_custom_mod_success(self):
        u'''应用自定义模板'''
        func.log(u'--------------test_i_mod_library_accept_custom_mod_success 开始-------------')
        #obj1 = CreateProduct(self.driver)
        value_list1 = EX.get_case_list(self.data_path, self.data_sheet3, 'test_mod_library_accept_custom_mod_success')
        try:
            self.open_mod_page()
            self.obj1.accept_mod(value_list1)
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            time.sleep(2)
            count = self.obj1.count_data_point()
            self.assertEqual(count, CreateProduct.mod_data_point_count)
        except Exception:
            func.log(u'【断言失败】：应用模板后数据端点数量有误，预期结果为'+str(CreateProduct.mod_data_point_count))
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_i_mod_library_accept_custom_mod_success 结束-------------')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    #suite.addTest(CreateProductTest('test_a_create_product_success'))
    suite.addTest(CreateProductTest('test_e9_mod_library_delete_custom_mod'))
    #suite.addTest(CreateProductTest('test_g1_mod_library_add_empty_point_name'))
    runner = unittest.TextTestRunner()
    runner.run(suite)