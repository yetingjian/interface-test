# coding=utf-8

import unittest
from common.driver import *
from common import myunit
from test_case.page_obj.check_drop_list_page import CheckDropList
from test_case.page_obj.product_info_page import ProductInfo
from test_case.page_obj.loginPage import Login
from test_case.page_obj.regist_device_page import RegisterDevicePage
from common import driver
from common import exceluitl as EX,  function as func
import sys, time
reload(sys)
sys.setdefaultencoding('utf-8')


class RegisterDeviceTest(unittest.TestCase):
    u'''新增产品'''
    data_path = func.find_path() + '/test_data/devplatform/regist_device.xlsx'
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

    def open_product_base_info(self, value_list):
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
        obj.search_product_and_click(value_list)

    def open_device_register_page(self, value_list):
        obj = ProductInfo(self.driver)
        obj1 = Login(self.driver)
        obj2 = RegisterDevicePage(self.driver)
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
        obj.search_product_and_click(value_list)
        obj.wait_quota_visible()
        time.sleep(1)
        obj2.click_dev_platform_item(u'设备注册')
        obj2.wait_count_visible()
        time.sleep(1)

    def register_device(self, value_list):
        obj1 = RegisterDevicePage(self.driver)
        #obj1.click_button(u'设备注册')
        obj1.click_register_type2(value_list[1])
        time.sleep(1)
        obj1.wait_dialog_visible()
        time.sleep(1)
        obj1.input_MAC(value_list[2])
        obj1.input_sequence(value_list[3])
        obj1.input_device_name(value_list[4])
        obj1.click_button(u'确定')
        time.sleep(1)

    def register_device_mult(self, value_list):
        obj1 = RegisterDevicePage(self.driver)
        #obj1.click_button(u'设备注册')
        obj1.click_register_type2(value_list[1])
        time.sleep(1)
        obj1.wait_dialog_visible()
        time.sleep(1)
        obj1.click_upload_obj(u'批量导入')
        time.sleep(2)

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_regist_device_success') == u'否', u'跳过执行')
    def test_a1_regist_device_success(self):
        u'''手动注册设备'''
        func.log(u'--------------test_a_regist_device_success 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_regist_device_success')
        try:
            obj1 = RegisterDevicePage(self.driver)
            self.open_device_register_page(value_list)
            self.register_device(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_success_message(), value_list[5])
        except Exception:
            func.log(u'【断言失败】：手动注册设备失败,预期信息为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            obj1.close_dialog()
            func.log(u'--------------test_a_regist_device_success 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_view_detail') == u'否', u'跳过执行')
    def test_a2_view_detail(self):
        u'''查看注册详情'''
        func.log(u'--------------test_a2_view_detail 开始-------------')
        a = 0
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_view_detail')
        try:
            obj1 = RegisterDevicePage(self.driver)
            self.open_device_register_page(value_list)
            obj1.click_view_detail()
            time.sleep(1)
            obj1.wait_button_enabled_css(u'批量导出二维码')
            num = obj1.get_regist_num()
            mac = obj1.get_mac()
            sn = obj1.get_sn()
            self.assertEqual(num, u'导入数量： 1')
            a = 1
            func.log(u'【断言成功】：导入数量预期信息为：导入数量： 1')
            self.assertEqual(mac, value_list[2])
            a = 2
            func.log(u'【断言成功】：MAC地址信息为：'+value_list[2])
            self.assertEqual(sn, value_list[3])
            func.log(u'【断言成功】：SN信息为：' + value_list[3])
        except Exception:
            if a == 0:
                func.log(u'【断言失败】：导入数量预期信息为：导入数量： 1')
            elif a == 1:
                func.log(u'【断言失败】：MAC地址预期信息为：'+value_list[2])
            elif a == 2:
                func.log(u'【断言失败】：SN预期信息为：' + value_list[3])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a2_view_detail 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_empty_MAC') == u'否', u'跳过执行')
    def test_a3_empty_MAC(self):
        u'''手动注册，MAC地址为空'''
        func.log(u'--------------test_a1_empty_MAC 开始-------------')
        obj1 = RegisterDevicePage(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_empty_MAC')
        try:

            self.open_device_register_page(value_list)
            self.register_device(value_list)
            self.assertEqual(obj1.get_error_by_class(), value_list[5])
        except Exception:
            func.log(u'【断言失败】：MAC地址为空预期提示信息为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            obj1.close_dialog()
            func.log(u'--------------test_a1_empty_MAC 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_same_MAC') == u'否', u'跳过执行')
    def test_a4_same_MAC(self):
        u'''手动注册，MAC地址重复'''
        func.log(u'--------------test_a2_same_MAC 开始-------------')
        obj1 = RegisterDevicePage(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_same_MAC')
        try:

            self.open_device_register_page(value_list)
            self.register_device(value_list)
            obj1.wait_message_visible()
            self.assertEqual(obj1.get_message(), value_list[5])
        except Exception:
            func.log(u'【断言失败】：MAC地址重复期提示信息为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            obj1.close_dialog()
            func.log(u'--------------test_a2_same_MAC 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_error_MAC') == u'否', u'跳过执行')
    def test_a5_error_MAC(self):
        u'''手动注册，MAC地址格式错误'''
        func.log(u'--------------test_a3_error_MAC 开始-------------')
        obj1 = RegisterDevicePage(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_error_MAC')
        try:

            self.open_device_register_page(value_list)
            self.register_device(value_list)
            self.assertEqual(obj1.get_error_by_class(), value_list[5])
        except Exception:
            func.log(u'【断言失败】：MAC地址格式错误预期提示信息为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            obj1.close_dialog()
            func.log(u'--------------test_a3_error_MAC 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_same_MAC_diff_product') == u'否', u'跳过执行')
    def test_a6_same_MAC_diff_product(self):
        u'''手动注册设备，相同MAC不同的产品'''
        func.log(u'--------------test_a4_same_MAC_diff_product 开始-------------')
        obj1 = RegisterDevicePage(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_same_MAC_diff_product')
        try:
            self.open_device_register_page(value_list)
            self.register_device(value_list)
            self.assertEqual(obj1.get_success_message(), value_list[5])
        except Exception:
            func.log(u'【断言失败】：手动注册设备失败,预期信息为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            obj1.close_dialog()
            func.log(u'--------------test_a4_same_MAC_diff_product 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_same_SN') == u'否', u'跳过执行')
    def test_a7_same_SN(self):
        u'''手动注册，SN重复'''
        func.log(u'--------------test_a5_same_SN 开始-------------')
        obj1 = RegisterDevicePage(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_same_SN')
        try:

            self.open_device_register_page(value_list)
            self.register_device(value_list)
            obj1.wait_message_visible()
            self.assertEqual(obj1.get_message(), value_list[5])
        except Exception:
            func.log(u'【断言失败】：SN重复期提示信息为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            obj1.close_dialog()
            func.log(u'--------------test_a5_same_SN 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_regist_device_mult_success') == u'否', u'跳过执行')
    def test_b1_regist_device_mult_success(self):
        u'''批量注册设备'''
        func.log(u'--------------test_b1_regist_device_mult_success 开始-------------')
        path = func.find_path() + r"/test_data/reg_device_2.csv"
        path = path.replace('/', '\\')
        obj1 = RegisterDevicePage(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_regist_device_mult_success')
        try:

            self.open_device_register_page(value_list)
            self.register_device_mult(value_list)
            obj1.upload_file(path)
            time.sleep(1)
            obj1.click_button(u'确定')
            time.sleep(1)
            self.assertEqual(obj1.get_success_message(), value_list[5])
        except Exception:
            func.log(u'【断言失败】：批量注册设备失败,预期信息为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            obj1.close_dialog()
            func.log(u'--------------test_b1_regist_device_mult_success 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_view_detail_mult') == u'否', u'跳过执行')
    def test_b2_view_detail_mult(self):
        u'''查看批量导入注册详情'''
        func.log(u'--------------test_b2_view_detail_mult 开始-------------')
        a = 0
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_view_detail_mult')
        try:
            obj1 = RegisterDevicePage(self.driver)
            self.open_device_register_page(value_list)
            obj1.click_view_detail()
            time.sleep(1)
            obj1.wait_button_enabled_css(u'批量导出二维码')
            num = obj1.get_regist_num()
            self.assertEqual(num, u'导入数量： 2')
        except Exception:
            func.log(u'【断言失败】：导入数量预期信息为：导入数量： 2')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_b2_view_detail_mult 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_view_detail_after_regitser') == u'否', u'跳过执行')
    def test_c1_view_detail_after_regitser(self):
        u'''查看批量导入注册详情'''
        func.log(u'--------------test_c1_view_detail_after_regitser 开始-------------')
        a = 0
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_view_detail_after_regitser')
        try:
            obj1 = RegisterDevicePage(self.driver)
            self.open_device_register_page(value_list)
            self.register_device(value_list)
            time.sleep(1)
            obj1.click_view_record(u'查看导入记录')
            obj1.wait_button_enabled_css(u'批量导出二维码')
            num = obj1.get_regist_num()
            self.assertEqual(num, u'导入数量： 1')
        except Exception:
            func.log(u'【断言失败】：导入数量预期信息为：导入数量： 1')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_c1_view_detail_after_regitser 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_regist_device_over_quota') == u'否', u'跳过执行')
    def test_d1_regist_device_over_quota(self):
        u'''设备超过产品限额'''
        func.log(u'--------------test_d1_regist_device_over_quota 开始-------------')
        path = func.find_path() + r"/test_data/reg_device_100.csv"
        path = path.replace('/', '\\')
        obj1 = RegisterDevicePage(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_regist_device_over_quota')
        try:

            self.open_device_register_page(value_list)
            self.register_device_mult(value_list)
            obj1.upload_file(path)
            time.sleep(1)
            obj1.click_button(u'确定')
            time.sleep(1)
            obj1.wait_message_visible()
            self.assertEqual(obj1.get_message(), value_list[5])
        except Exception:
            func.log(u'【断言失败】：设备超过产品限额,预期信息为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            obj1.close_dialog()
            func.log(u'--------------test_d1_regist_device_over_quota 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_error_import_file') == u'否', u'跳过执行')
    def test_d2_error_import_file(self):
        u'''导入非文本文件'''
        func.log(u'--------------test_d2_error_import_file 开始-------------')
        path = func.find_path() + r"/test_data/4.png"
        path = path.replace('/', '\\')
        obj1 = RegisterDevicePage(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_error_import_file')
        try:

            self.open_device_register_page(value_list)
            self.register_device_mult(value_list)
            obj1.upload_file(path)
            time.sleep(1)
            obj1.click_button(u'确定')
            time.sleep(1)
            obj1.wait_message_visible()
            self.assertEqual(obj1.get_message(), value_list[5])
        except Exception:
            func.log(u'【断言失败】：导入非文本文件,预期信息为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            obj1.close_dialog()
            func.log(u'--------------test_d2_error_import_file 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_search_by_user') == u'否', u'跳过执行')
    def test_d2_search_by_user(self):
        u'''通过添加人查询导入记录'''
        func.log(u'--------------test_d3_search_by_user 开始-------------')
        obj1 = RegisterDevicePage(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_search_by_user')
        try:

            self.open_device_register_page(value_list)
            time.sleep(1)
            obj1.click_button(u'确定')
            time.sleep(1)
            obj1.wait_message_visible()
            self.assertEqual(obj1.get_message(), value_list[5])
        except Exception:
            func.log(u'【断言失败】：导入非文本文件,预期信息为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            obj1.close_dialog()
            func.log(u'--------------test_d3_search_by_user 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet1, 'test_view_device_by_MAC') == u'否', u'跳过执行')
    def test_e1_view_device_by_MAC(self):
        u'''点击mac查看设备详情'''
        func.log(u'--------------test_e1_view_device_by_MAC 开始-------------')
        obj1 = RegisterDevicePage(self.driver)
        obj2 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet1, 'test_view_device_by_MAC')
        try:
            self.open_product_base_info(value_list)
            obj2.wait_quota_visible()
            time.sleep(1)
            obj2.click_mac(value_list[1])
            obj2.wait_class_visible_text('main-title', u'设备详情')
            self.assertEqual(obj1.get_obj_text_by_class('txt'), value_list[4])
        except Exception:
            func.log(u'【断言失败】：点击mac页面没有跳转至设备详情页')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            obj1.close_dialog()
            func.log(u'--------------test_e1_view_device_by_MAC 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet1, 'test_modity_sn') == u'否', u'跳过执行')
    def test_e2_modity_sn(self):
        u'''修改sn'''
        func.log(u'--------------test_e2_modity_sn 开始-------------')
        obj2 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet1, 'test_modity_sn')
        try:
            self.open_product_base_info(value_list)
            obj2.wait_quota_visible()
            time.sleep(1)
            obj2.click_sn(value_list[1])
            obj2.input_sn(value_list[3])
            time.sleep(1)
            self.assertEqual(obj2.get_sn(value_list[1]), value_list[4])
        except Exception:
            func.log(u'【断言失败】：修改sn后，sn预期显示为：' + value_list[4])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e2_modity_sn 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_search_by_MAC') == u'否', u'跳过执行')
    def test_f1_search_by_MAC(self):
        u'''通过MAC查询设备'''
        func.log(u'--------------test_f1_search_by_MAC 开始-------------')
        obj2 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_search_by_MAC')
        try:
            self.open_product_base_info(value_list)
            obj2.wait_quota_visible()
            time.sleep(1)
            obj2.click_search_type(value_list[1])
            obj2.input_search_text(value_list[2])
            obj2.click_search_button()
            time.sleep(1)
            row = obj2.get_result_rows()
            self.assertEqual(str(row), str(value_list[5]))
        except Exception:
            func.log(u'【断言失败】：查询结果记录数预期为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_f1_search_by_MAC 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_search_by_MAC_error_MAC') == u'否', u'跳过执行')
    def test_f2_search_by_MAC_error_MAC(self):
        u'''查询不存在的MAC'''
        func.log(u'--------------test_f2_search_by_MAC_error_MAC 开始-------------')
        obj2 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_search_by_MAC_error_MAC')
        try:
            self.open_product_base_info(value_list)
            obj2.wait_quota_visible()
            time.sleep(1)
            obj2.click_search_type(value_list[1])
            obj2.input_search_text(value_list[2])
            obj2.click_search_button()
            time.sleep(1)
            row = obj2.get_result_rows()
            self.assertEqual(str(row), str(value_list[5]))
        except Exception:
            func.log(u'【断言失败】：查询结果记录数预期为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_f2_search_by_MAC_error_MAC 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_search_by_MAC_fuzzy') == u'否', u'跳过执行')
    def test_f3_search_by_MAC_fuzzy(self):
        u'''通过MAC模糊查询设备'''
        func.log(u'--------------test_f3_search_by_MAC_fuzzy 开始-------------')
        obj2 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_search_by_MAC_fuzzy')
        try:
            self.open_product_base_info(value_list)
            obj2.wait_quota_visible()
            time.sleep(1)
            obj2.click_search_type(value_list[1])
            obj2.input_search_text(value_list[2])
            obj2.click_search_button()
            time.sleep(1)
            row = obj2.get_result_rows()
            self.assertEqual(str(row), str(value_list[5]))
        except Exception:
            func.log(u'【断言失败】：查询结果记录数预期为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_f3_search_by_MAC_fuzzy 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_search_by_SN') == u'否', u'跳过执行')
    def test_f4_search_by_SN(self):
        u'''通过SN查询设备'''
        func.log(u'--------------test_f4_search_by_SN 开始-------------')
        obj2 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_search_by_SN')
        try:
            self.open_product_base_info(value_list)
            obj2.wait_quota_visible()
            time.sleep(1)
            obj2.click_search_type(value_list[1])
            obj2.input_search_text(value_list[4])
            obj2.click_search_button()
            time.sleep(1)
            row = obj2.get_result_rows()
            self.assertEqual(str(row), str(value_list[5]))
        except Exception:
            func.log(u'【断言失败】：查询结果记录数预期为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_f4_search_by_SN 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_search_by_SN_error_SN') == u'否', u'跳过执行')
    def test_f5_search_by_SN_error_SN(self):
        u'''查询不存在的SN'''
        func.log(u'--------------test_f5_search_by_SN_error_SN 开始-------------')
        obj2 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_search_by_SN_error_SN')
        try:
            self.open_product_base_info(value_list)
            obj2.wait_quota_visible()
            time.sleep(1)
            obj2.click_search_type(value_list[1])
            obj2.input_search_text(value_list[4])
            obj2.click_search_button()
            time.sleep(1)
            row = obj2.get_result_rows()
            self.assertEqual(str(row), str(value_list[5]))
        except Exception:
            func.log(u'【断言失败】：查询结果记录数预期为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_f5_search_by_SN_error_SN 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_search_by_SN_fuzzy') == u'否', u'跳过执行')
    def test_f6_search_by_SN_fuzzy(self):
        u'''通过Sn模糊查询'''
        func.log(u'--------------test_f6_search_by_SN_fuzzy 开始-------------')
        obj2 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_search_by_SN_fuzzy')
        try:
            self.open_product_base_info(value_list)
            obj2.wait_quota_visible()
            time.sleep(1)
            obj2.click_search_type(value_list[1])
            obj2.input_search_text(value_list[4])
            obj2.click_search_button()
            time.sleep(1)
            row = obj2.get_result_rows()
            self.assertEqual(str(row), str(value_list[5]))
        except Exception:
            func.log(u'【断言失败】：查询结果记录数预期为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_f6_search_by_SN_fuzzy 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_search_by_ID') == u'否', u'跳过执行')
    def test_f7_search_by_ID(self):
        u'''通过ID查询'''
        func.log(u'--------------test_f7_search_by_ID 开始-------------')
        obj2 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_search_by_ID')
        try:
            self.open_product_base_info(value_list)
            obj2.wait_quota_visible()
            time.sleep(1)
            obj2.click_search_type(value_list[1])
            obj2.input_device_id(value_list[3])
            obj2.click_search_button()
            time.sleep(1)
            row = obj2.get_result_rows()
            self.assertEqual(str(row), str(value_list[5]))
        except Exception:
            func.log(u'【断言失败】：查询结果记录数预期为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_f7_search_by_ID 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_search_by_ID_error_ID') == u'否', u'跳过执行')
    def test_f8_search_by_ID_error_ID(self):
        u'''查询不存在的ID'''
        func.log(u'--------------test_f8_search_by_ID_error_ID 开始-------------')
        obj2 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_search_by_ID_error_ID')
        try:
            self.open_product_base_info(value_list)
            obj2.wait_quota_visible()
            time.sleep(1)
            obj2.click_search_type(value_list[1])
            obj2.input_device_id(value_list[3])
            obj2.click_search_button()
            time.sleep(1)
            row = obj2.get_result_rows()
            self.assertEqual(str(row), str(value_list[5]))
        except Exception:
            func.log(u'【断言失败】：查询结果记录数预期为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_f8_search_by_ID_error_ID 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_search_by_ID_fuzzy') == u'否', u'跳过执行')
    def test_f9_search_by_ID_fuzzy(self):
        u'''通过ID模糊查询'''
        func.log(u'--------------test_f9_search_by_ID_fuzzy 开始-------------')
        obj2 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_search_by_ID_fuzzy')
        try:
            self.open_product_base_info(value_list)
            obj2.wait_quota_visible()
            time.sleep(1)
            obj2.click_search_type(value_list[1])
            obj2.input_device_id(value_list[3])
            obj2.click_search_button()
            time.sleep(1)
            row = obj2.get_result_rows()
            self.assertEqual(str(row), str(value_list[5]))
        except Exception:
            func.log(u'【断言失败】：查询结果记录数预期为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_f9_search_by_ID_fuzzy 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_check_online_records') == u'否', u'跳过执行')
    def test_g1_check_online_records(self):
        u'''查看上下线记录'''
        func.log(u'--------------test_g1_check_online_records 开始-------------')
        obj2 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet3, 'test_check_online_records')
        try:
            self.open_product_base_info(value_list)
            obj2.wait_quota_visible()
            time.sleep(1)
            obj2.click_button(u'查看上下线历史记录')
            time.sleep(1)
            result = obj2.wait_element_visible_by_class_with_text('x-breadcrumb__label', u'设备上下线记录')
            self.assertEqual(result, 'Y')
        except Exception:
            func.log(u'【断言失败】：页面没有跳转到设备上下线记录页面')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_g1_check_online_records 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_check_register_device') == u'否', u'跳过执行')
    def test_g2_check_register_device(self):
        u'''注册设备页面跳转'''
        func.log(u'--------------test_g2_check_register_device 开始-------------')
        obj2 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet3, 'test_check_register_device')
        try:
            self.open_product_base_info(value_list)
            obj2.wait_quota_visible()
            time.sleep(1)
            obj2.click_button(u'查看上下线历史记录')
            time.sleep(1)
            result = obj2.wait_element_visible_by_class_with_text('main-title', u'设备注册')
            self.assertEqual(result, 'Y')
        except Exception:
            func.log(u'【断言失败】：页面没有跳转到注册设备页面')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_g2_check_register_device 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_screen_staute') == u'否', u'跳过执行')
    def test_g3_screen_staute(self):
        u'''通过状态筛选'''
        func.log(u'--------------test_g3_screen_staute 开始-------------')
        obj2 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet3, 'test_screen_staute')
        a = 0
        try:
            self.open_product_base_info(value_list)
            obj2.wait_quota_visible()
            time.sleep(1)
            obj2.click_statue_type(u'全部')
            time.sleep(1)
            row = obj2.get_result_rows()
            self.assertEqual(str(row), '2')
            a = 1
            obj2.click_statue_type(u'在线')
            time.sleep(1)
            row = obj2.get_result_rows()
            self.assertEqual(str(row), '0')
            a = 2
            obj2.click_statue_type(u'下线')
            time.sleep(1)
            row = obj2.get_result_rows()
            self.assertEqual(str(row), '2')
            a = 3
            obj2.click_statue_type(u'激活')
            time.sleep(1)
            row = obj2.get_result_rows()
            self.assertEqual(str(row), '0')
            a = 4
            obj2.click_statue_type(u'未激活')
            time.sleep(1)
            row = obj2.get_result_rows()
            self.assertEqual(str(row), '2')
        except Exception:
            if a == 0:
                func.log(u'【断言失败】：筛选结果记录数预期为：2')
            elif a == 1:
                func.log(u'【断言失败】：筛选结果记录数预期为：0')
            elif a == 2:
                func.log(u'【断言失败】：筛选结果记录数预期为：2')
            elif a == 3:
                func.log(u'【断言失败】：筛选结果记录数预期为：0')
            elif a == 4:
                func.log(u'【断言失败】：筛选结果记录数预期为：2')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_g3_screen_staute 结束-------------')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(RegisterDeviceTest('test_g3_screen_staute'))
    #suite.addTest(ProductInfoTest('test_h1_config_attr'))
    runner = unittest.TextTestRunner()
    runner.run(suite)