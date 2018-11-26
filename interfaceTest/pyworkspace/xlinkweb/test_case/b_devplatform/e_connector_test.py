# coding=utf-8

import unittest
from common.driver import *
from common import myunit
from test_case.page_obj.create_product_page import CreateProduct
from test_case.page_obj.product_info_page import ProductInfo
from test_case.page_obj.loginPage import Login
from test_case.page_obj.connector_page import ConnectorPage
from common import driver
from common import exceluitl as EX,  function as func
import sys, time
reload(sys)
sys.setdefaultencoding('utf-8')


class ConnectorTest(unittest.TestCase):
    u'''新增产品'''
    data_path = func.find_path() + '/test_data/devplatform/connector.xlsx'
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

    def open_connector_page(self):
        obj = ProductInfo(self.driver)
        obj1 = Login(self.driver)
        obj2 = CreateProduct(self.driver)
        obj3 = ConnectorPage(self.driver)
        obj.open_url('#/apps/home')
        time.sleep(1)
        obj1.wait_element_visible()
        time.sleep(1)
        obj2.click_dev_plant()
        obj.wait_element_visible_by_class('title1')
        obj3.click_connector_manager()
        time.sleep(1)
        obj3.wait_element_visible_by_class_with_text('main-title', u'连接器管理')

    def edit_connector(self, value_list):
        obj = ConnectorPage(self.driver)
        obj.click_edit()
        obj.wait_dialog_visible()
        obj.clear_connector_name()
        obj.input_connector_name(value_list[1])
        obj.click_button(u'确定修改')

    def delete_connector(self):
        obj = ConnectorPage(self.driver)
        obj.click_delete_connector()
        obj.wait_dialog_visible()
        time.sleep(1)
        obj.input_verify_text()
        obj.click_button(u'确定')

    def create_version(self, value_list):
        path = func.find_path() + r"/test_data/4.png"
        path = path.replace('/', '\\')
        obj = ConnectorPage(self.driver)
        obj.click_button(u'添加新版本')
        time.sleep(1)
        obj.input_version_num(value_list[1])
        if value_list[2] == u'是':
            obj.click_upload_file()
            time.sleep(2)
            obj.upload_file(path)
        time.sleep(2)
        obj.input_comments(value_list[3])
        time.sleep(1)
        obj.click_button(u'确定')

    def release_version(self):
        obj = ConnectorPage(self.driver)
        obj.click_release()
        obj.wait_dialog_visible()
        time.sleep(1)
        obj.input_remarks()
        obj.click_button(u'确定')

    def offline_version(self):
        obj = ConnectorPage(self.driver)
        obj.click_release()
        obj.wait_dialog_visible()
        time.sleep(1)
        obj.input_verify_text()
        obj.click_button(u'确定')

    def delete_version(self):
        obj = ConnectorPage(self.driver)
        obj.click_delete()
        obj.wait_dialog_visible()
        time.sleep(1)
        obj.input_verify_text()
        obj.click_button(u'确定')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_create_connector_success') == u'否', u'跳过执行')
    def test_a1_create_connector_success(self):
        u'''创建连接器成功'''
        func.log(u'--------------test_a1_create_connector_success 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_create_connector_success')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.click_button(u'创建连接器')
            obj.wait_dialog_visible()
            obj.input_connector_name(value_list[0])
            obj.click_button(u'完成并创建')
            obj.wait_message_visible()
            self.assertEqual(obj.get_message(), value_list[1])
        except Exception:
            func.log(u'【断言失败】：创建连接器失败,预期提示为：' + value_list[1])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            obj.close_dialog()
            func.log(u'--------------test_a1_create_connector_success 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_connector_name_empty') == u'否', u'跳过执行')
    def test_a2_connector_name_empty(self):
        u'''创建连接器名称为空'''
        func.log(u'--------------test_a2_connector_name_empty 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_connector_name_empty')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.click_button(u'创建连接器')
            obj.wait_dialog_visible()
            obj.input_connector_name(value_list[0])
            self.assertEqual(obj.get_attribute('disabled'), 'true')
        except Exception:
            func.log(u'【断言失败】：创建连接器名称为空时,提交按钮应不可点击：')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            obj.close_dialog()
            func.log(u'--------------test_a2_connector_name_empty 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_connector_name_over_length') == u'否', u'跳过执行')
    def test_a3_connector_name_over_length(self):
        u'''创建连接器名称超长'''
        func.log(u'--------------test_a3_connector_name_over_length 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_connector_name_over_length')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.click_button(u'创建连接器')
            obj.wait_dialog_visible()
            obj.input_connector_name(value_list[0])
            obj.click_button(u'完成并创建')
            self.assertEqual(obj.get_error_by_class(), value_list[1])
        except Exception:
            func.log(u'【断言失败】：连接器名称超长时,预期提示为：' + value_list[1])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            obj.close_dialog()
            func.log(u'--------------test_a3_connector_name_over_length 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_connector_name_existed') == u'否', u'跳过执行')
    def test_a4_connector_name_existed(self):
        u'''创建连接器名称已存在'''
        func.log(u'--------------test_a4_connector_name_existed 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_connector_name_existed')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.click_button(u'创建连接器')
            obj.wait_dialog_visible()
            obj.input_connector_name(value_list[0])
            obj.click_button(u'完成并创建')
            time.sleep(1)
            # obj.wait_message_visible()
            self.assertEqual(obj.get_message(), value_list[1])
        except Exception:
            func.log(u'【断言失败】：连接器名称已存在,预期提示为：' + value_list[1])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            obj.close_dialog()
            func.log(u'--------------test_a4_connector_name_existed 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_search_by_full_name') == u'否', u'跳过执行')
    def test_b1_search_by_full_name(self):
        u'''全名搜索连接器'''
        func.log(u'--------------test_b1_search_by_full_name 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_search_by_full_name')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.search_connector(value_list[0])
            time.sleep(1)
            self.assertEqual(obj.get_row_text(), value_list[1])
        except Exception:
            func.log(u'【断言失败】：全名搜索连接器,预期记录为：' + value_list[1])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            obj.close_dialog()
            func.log(u'--------------test_b1_search_by_full_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_search_by_fuzzy_name') == u'否', u'跳过执行')
    def test_b2_search_by_fuzzy_name(self):
        u'''模糊搜索连接器'''
        func.log(u'--------------test_b2_search_by_fuzzy_name 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_search_by_fuzzy_name')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.search_connector(value_list[0])
            time.sleep(1)
            self.assertEqual(obj.get_row_text(), value_list[1])
        except Exception:
            func.log(u'【断言失败】：模糊搜索连接器,预期记录为：' + value_list[1])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            obj.close_dialog()
            func.log(u'--------------test_b2_search_by_fuzzy_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_search_by_error_name') == u'否', u'跳过执行')
    def test_b3_search_by_error_name(self):
        u'''模糊搜索连接器'''
        func.log(u'--------------test_b3_search_by_error_name 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_search_by_error_name')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.search_connector(value_list[0])
            time.sleep(1)
            self.assertEqual(obj.get_row_text(), value_list[1])
        except Exception:
            func.log(u'【断言失败】：模糊搜索连接器,预期记录为：' + value_list[1])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            obj.close_dialog()
            func.log(u'--------------test_b3_search_by_error_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet1, 'test_edit_name') == u'否', u'跳过执行')
    def test_c1_edit_name(self):
        u'''编辑连接器名称'''
        func.log(u'--------------test_c1_edit_name 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet1, 'test_edit_name')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.search_connector(value_list[0])
            time.sleep(1)
            obj.click_manage()
            obj.wait_class_visible('detail-title')
            self.edit_connector(value_list)
            obj.wait_message_visible()
            self.assertEqual(obj.get_connector_name(), value_list[2])
        except Exception:
            func.log(u'【断言失败】：编辑连接器名称,预期结果为：' + value_list[2])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_c1_edit_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_create_new_version') == u'否', u'跳过执行')
    def test_d1_create_new_version(self):
        u'''创建新版本'''
        func.log(u'--------------test_d1_create_new_version 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_create_new_version')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.search_connector(value_list[0])
            time.sleep(1)
            obj.click_manage()
            obj.wait_class_visible('detail-title')
            self.create_version(value_list)
            obj.wait_message_visible()
            self.assertEqual(obj.get_message(), value_list[4])
        except Exception:
            func.log(u'【断言失败】：创建新版本预期结果为：' + value_list[4])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_d1_create_new_version 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_empty_version_num') == u'否', u'跳过执行')
    def test_d2_empty_version_num(self):
        u'''添加版本-版本号为空'''
        func.log(u'--------------test_d2_empty_version_num 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_empty_version_num')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.search_connector(value_list[0])
            time.sleep(1)
            obj.click_manage()
            obj.wait_class_visible('detail-title')
            self.create_version(value_list)
            self.assertEqual(obj.get_error_by_class(), value_list[4])
        except Exception:
            func.log(u'【断言失败】：版本号为空预期结果为：' + value_list[4])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_d2_empty_version_num 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_empty_upload') == u'否', u'跳过执行')
    def test_d3_empty_version_num(self):
        u'''添加版本-上传文件为空'''
        func.log(u'--------------test_d3_empty_version_num 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_empty_upload')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.search_connector(value_list[0])
            time.sleep(1)
            obj.click_manage()
            obj.wait_class_visible('detail-title')
            self.create_version(value_list)
            self.assertEqual(obj.get_error_by_class(), value_list[4])
        except Exception:
            func.log(u'【断言失败】：上传文件为空预期结果为：' + value_list[4])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_d3_empty_version_num 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_empty_comment') == u'否', u'跳过执行')
    def test_d4_empty_comment(self):
        u'''添加版本-说明为空'''
        func.log(u'--------------test_d4_empty_comment 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_empty_comment')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.search_connector(value_list[0])
            time.sleep(1)
            obj.click_manage()
            obj.wait_class_visible('detail-title')
            self.create_version(value_list)
            self.assertEqual(obj.get_error_by_class(), value_list[4])
        except Exception:
            func.log(u'【断言失败】：说明为空预期结果为：' + value_list[4])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_d4_empty_comment 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_error_version_num') == u'否', u'跳过执行')
    def test_d5_error_version_num(self):
        u'''添加版本-版本号格式错误'''
        func.log(u'--------------test_d5_error_version_num 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_error_version_num')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.search_connector(value_list[0])
            time.sleep(1)
            obj.click_manage()
            obj.wait_class_visible('detail-title')
            self.create_version(value_list)
            self.assertEqual(obj.get_error_by_class(), value_list[4])
        except Exception:
            func.log(u'【断言失败】：版本号格式错误预期结果为：' + value_list[4])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_d5_error_version_num 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_exist_version_num') == u'否', u'跳过执行')
    def test_d6_exist_version_num(self):
        u'''添加版本-已存在的版本号'''
        func.log(u'--------------test_d6_exist_version_num 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_exist_version_num')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.search_connector(value_list[0])
            time.sleep(1)
            obj.click_manage()
            obj.wait_class_visible('detail-title')
            self.create_version(value_list)
            self.assertEqual(obj.get_error_by_class(), value_list[4])
        except Exception:
            func.log(u'【断言失败】：已存在的版本号预期结果为：' + value_list[4])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_d6_exist_version_num 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_lower_version') == u'否', u'跳过执行')
    def test_d7_lower_version(self):
        u'''添加版本-版本号比当前版本低'''
        func.log(u'--------------test_d7_lower_version 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_lower_version')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.search_connector(value_list[0])
            time.sleep(1)
            obj.click_manage()
            obj.wait_class_visible('detail-title')
            self.create_version(value_list)
            self.assertEqual(obj.get_error_by_class(), value_list[4])
        except Exception:
            func.log(u'【断言失败】：版本号比当前版本低预期结果为：' + value_list[4])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_d7_lower_version 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_release_version') == u'否', u'跳过执行')
    def test_e1_release_version(self):
        u'''发布版本'''
        func.log(u'--------------test_e1_release_version 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet3, 'test_release_version')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.search_connector(value_list[0])
            time.sleep(1)
            obj.click_manage()
            obj.wait_class_visible('detail-title')
            self.release_version()
            obj.wait_message_visible()
            time.sleep(1)
            self.assertEqual(obj.get_version_status(), value_list[1])
        except Exception:
            func.log(u'【断言失败】：发布版本后版本状态预期结果为：' + value_list[1])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e1_release_version 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_offline_version') == u'否', u'跳过执行')
    def test_e2_offline_version(self):
        u'''下线版本'''
        func.log(u'--------------test_e2_offline_version 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet3, 'test_offline_version')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.search_connector(value_list[0])
            time.sleep(1)
            obj.click_manage()
            obj.wait_class_visible('detail-title')
            self.offline_version()
            obj.wait_message_visible()
            time.sleep(1)
            self.assertEqual(obj.get_version_status(), value_list[1])
        except Exception:
            func.log(u'【断言失败】：下线版本后版本状态预期结果为：' + value_list[1])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e2_offline_version 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_delete_version') == u'否', u'跳过执行')
    def test_e3_delete_version(self):
        u'''删除版本'''
        func.log(u'--------------test_e4_delete_version 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet3, 'test_delete_version')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.search_connector(value_list[0])
            time.sleep(1)
            obj.click_manage()
            obj.wait_class_visible('detail-title')
            self.delete_version()
            obj.wait_message_visible()
            time.sleep(1)
            self.assertEqual(obj.get_empty_table(), u'暂无数据')
        except Exception:
            func.log(u'【断言失败】：删除版本后预期记录数为：0')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e4_delete_version 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet1, 'test_delete_connector') == u'否', u'跳过执行')
    def test_f1_delete_connector(self):
        u'''删除连接器'''
        func.log(u'--------------test_f1_delete_connector 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet1, 'test_delete_connector')
        try:
            obj = ConnectorPage(self.driver)
            self.open_connector_page()
            obj.search_connector(value_list[0])
            time.sleep(1)
            obj.click_manage()
            obj.wait_class_visible('detail-title')
            self.delete_connector()
            obj.wait_message_visible()
            self.assertEqual(obj.get_message(), value_list[2])
        except Exception:
            func.log(u'【断言失败】：删除连接器,预期结果为：' + value_list[2])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_f1_delete_connector 结束-------------')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(ConnectorTest('test_a4_connector_name_existed'))
    #suite.addTest(ProductInfoTest('test_h1_config_attr'))
    runner = unittest.TextTestRunner()
    runner.run(suite)