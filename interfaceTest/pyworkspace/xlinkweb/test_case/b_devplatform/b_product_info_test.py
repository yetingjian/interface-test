# coding=utf-8

import unittest
from common.driver import *
from common import myunit
from test_case.page_obj.product_info_page import ProductInfo
from test_case.page_obj.loginPage import Login
from test_case.page_obj.regist_device_page import RegisterDevicePage
from common import driver
from common import exceluitl as EX,  function as func
import sys, time
reload(sys)
sys.setdefaultencoding('utf-8')


class ProductInfoTest(unittest.TestCase):
    u'''新增产品'''
    data_path = func.find_path() + '/test_data/devplatform/product_info.xlsx'
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
    # func.log(u'----------------------------------ProductInfoTest 开始-----------------------------------')
    # def setUpClass(cls):
    #     cls.driver = Broswer.get_instance()

    @classmethod
    def setUpClass(cls):
        func.log(u'----------------------------------ProductInfoTest 开始-----------------------------------')
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

    def edit_product_info(self, value_list):
        obj = ProductInfo(self.driver)
        obj.input_text(u'产品名称', value_list[2])
        obj.input_text(u'产品型号', value_list[3])
        obj.select_text1(u'产品分类', value_list[4])
        obj.select_text2(u'连接类型', value_list[3])
        obj.click_button(u'提交')

    def upload_img(self, path):
        obj = ProductInfo(self.driver)
        obj.click_upload_img()
        time.sleep(3)
        obj.upload_file(path)

    def add_text_attr(self, value_list):
        obj = ProductInfo(self.driver)
        obj.add_attr()
        obj.click_tab_item(value_list)
        time.sleep(1)
        obj.input_para_name(value_list[2])
        obj.input_attr_name(value_list[3])
        obj.input_text_len(value_list[4])
        obj.input_init_value(value_list[5])
        obj.input_descript(value_list[8])
        obj.click_button(u'保存')

    def add_number_attr(self, value_list):
        obj = ProductInfo(self.driver)
        obj.add_attr()
        obj.click_tab_item(value_list)
        time.sleep(1)
        obj.input_para_name(value_list[2])
        obj.input_attr_name(value_list[3])
        obj.input_init_value(value_list[5])
        obj.input_float_len(value_list[6])
        obj.input_unit(value_list[7])
        obj.input_descript(value_list[8])
        obj.click_button(u'保存')

    def add_date_attr(self, value_list):
        obj = ProductInfo(self.driver)
        obj.add_attr()
        obj.click_tab_item(value_list)
        time.sleep(1)
        obj.input_para_name(value_list[2])
        obj.input_attr_name_date(value_list[3])
        obj.input_date(value_list[5], u'选择日期和时间')
        obj.input_descript_date(value_list[8])
        obj.click_button(u'保存')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_check_quota') == u'否', u'跳过执行')
    def test_a_check_quota(self):
        u'''检查配额数量'''
        func.log(u'--------------test_a_check_quota 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_check_quota')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            self.assertEqual(obj1.get_quota(), '100')
        except Exception:
            func.log(u'【断言失败】：产品配额预期结果为：100')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a_check_quota 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_check_secret_key') == u'否', u'跳过执行')
    def test_a_check_secret_key(self):
        u'''检查产品密钥'''
        func.log(u'--------------test_a_check_secret_key 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_check_secret_key')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            result = obj1.get_secret_key()
            self.assertNotEqual(result, '')
        except Exception:
            func.log(u'【断言失败】：产品密钥不能为空')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a_check_secret_key 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_check_qrcode') == u'否', u'跳过执行')
    def test_a_check_qrcode(self):
        u'''检查产品二维码'''
        func.log(u'--------------test_a_check_qrcode 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_check_qrcode')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            result = obj1.get_qrcode()
            self.assertNotEqual(result, '')
        except Exception:
            func.log(u'【断言失败】：产品二维码不能为空')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a_check_qrcode 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_product_release') == u'否', u'跳过执行')
    def test_a_product_release(self):
        u'''发布产品'''
        func.log(u'--------------test_a_product_release 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_product_release')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.release_product()
            obj1.wait_message_visible()
            result = obj1.get_product_release_text()
            self.assertEqual(result, u'已发布')
        except Exception:
            func.log(u'【断言失败】：发布产品产品成功后预期结果为：已发布')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a_product_release 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_register_device') == u'否', u'跳过执行')
    def test_a_register_device_page(self):
        u'''设备注册页面跳转'''
        func.log(u'--------------test_a_register_device_page 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_register_device')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.click_button(u'设备注册')
            state = obj1.wait_register_page()
            time.sleep(1)
            self.assertEqual(state, True)
        except Exception:
            func.log(u'【断言失败】：设备注册页面状态预期提示为：True')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a_register_device_page 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet1, 'test_edit_product_name_success') == u'否', u'跳过执行')
    def test_b_edit_product_name_success(self):
        u'''修改产品名称'''
        func.log(u'--------------test_b_edit_product_name_success 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet1, 'test_edit_product_name_success')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.edit_product_info(value_list)
            obj1.wait_message_visible()
            self.assertEqual(obj1.get_message(), value_list[7])
        except Exception:
            func.log(u'【断言失败】：修改产品名称成功后预期结果为：' + value_list[7])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_b_edit_product_name_success 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet1, 'test_edit_empty_product_name') == u'否', u'跳过执行')
    def test_b_edit_product_name_empty(self):
        u'''修改产品名称为空'''
        func.log(u'--------------test_b_edit_product_name_empty 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet1, 'test_edit_empty_product_name')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.edit_product_info(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_error_message(u'产品名称'), value_list[7])
        except Exception:
            func.log(u'【断言失败】：修改产品名称为空后预期结果为：' + value_list[7])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_b_edit_product_name_empty 结束-------------')

    def test_b_upload(self):
        u'''上传图片'''
        func.log(u'--------------test_b_upload 开始-------------')
        obj1 = ProductInfo(self.driver)
        path = func.find_path() + r"\test_data\4.png"
        path = path.replace('/', '\\')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_upload')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            time.sleep(1)
            self.upload_img(path)
            time.sleep(2)
            self.assertEqual(obj1.get_upload_file_src(), True)
        except Exception:
            func.log(u'【断言失败】：图片上传失败')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_b_upload 结束-------------')

    def test_b_upload_error_file(self):
        u'''上传错误文件'''
        func.log(u'--------------test_b_upload_error_file 开始-------------')
        obj1 = ProductInfo(self.driver)
        path = func.find_path() + r"\test_data\devplatform\product_info.xlsx"
        path = path.replace('/', '\\')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_upload_error_file')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            time.sleep(1)
            self.upload_img(path)
            obj1.wait_message_visible()
            self.assertEqual(obj1.get_message(), value_list[2])
        except Exception:
            func.log(u'【断言失败】：上传错误文件后预期结果为：' + value_list[2])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_b_upload_error_file 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_text_attr_success') == u'否', u'跳过执行')
    def test_c1_add_text_attr_success(self):
        u'''添加文本属性成功'''
        func.log(u'--------------test_c_add_text_attr_success 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_text_attr_success')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_text_attr(value_list)
            obj1.wait_message_visible()
            time.sleep(1)
            self.assertEqual(obj1.get_attr_value(value_list[3]), value_list[5])
        except Exception:
            func.log(u'【断言失败】：' + u'属性名【' + value_list[3] + u'】的值预期为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_c_add_text_attr_success 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_text_attr_same_para_name') == u'否', u'跳过执行')
    def test_c2_add_text_attr_same_para_name(self):
        u'''添加文本属性，字段名重名'''
        func.log(u'--------------test_c2_add_text_attr_same_para_name 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_text_attr_same_para_name')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_text_attr(value_list)
            obj1.wait_message_visible()
            self.assertEqual(obj1.get_message(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：字段名重名后预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_c2_add_text_attr_same_para_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_text_attr_error_para_name') == u'否', u'跳过执行')
    def test_c3_add_text_attr_error_para_name(self):
        u'''添加文本属性，字段名格式错误'''
        func.log(u'--------------test_c3_add_text_attr_error_para_name 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_text_attr_error_para_name')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_text_attr(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_error_by_class(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：字段名格式错误提示预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_c3_add_text_attr_error_para_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_text_attr_empty_para_name') == u'否', u'跳过执行')
    def test_c4_add_text_attr_empty_para_name(self):
        u'''添加文本属性，字段名为空'''
        func.log(u'--------------test_c4_add_text_attr_empty_para_name 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_text_attr_empty_para_name')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_text_attr(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_error_by_class(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：字段名为空提示预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_c4_add_text_attr_empty_para_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_text_attr_empty_attr_name') == u'否', u'跳过执行')
    def test_c5_add_text_attr_empty_attr_name(self):
        u'''添加文本属性，属性名为空'''
        func.log(u'--------------test_c5_add_text_attr_empty_attr_name 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_text_attr_empty_attr_name')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_text_attr(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_error_by_class(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：属性名为空错误提示预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_c5_add_text_attr_empty_attr_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_text_attr_empty_text_len') == u'否', u'跳过执行')
    def test_c6_add_text_attr_empty_text_len(self):
        u'''添加文本属性，文本长度为空'''
        func.log(u'--------------test_c6_add_text_attr_empty_text_len 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_text_attr_empty_text_len')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_text_attr(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_error_by_class(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：文本长度为空提示预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_c6_add_text_attr_empty_text_len 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_text_attr_empty_init_value') == u'否', u'跳过执行')
    def test_c7_add_text_attr_empty_init_value(self):
        u'''添加文本属性，初始值为空'''
        func.log(u'--------------test_c7_add_text_attr_empty_init_value 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_text_attr_empty_init_value')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_text_attr(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_error_by_class(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：初始值为空错误提示预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_c7_add_text_attr_empty_init_value 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_text_attr_error_len') == u'否', u'跳过执行')
    def test_c8_add_text_attr_error_len(self):
        u'''添加文本属性，文本超度超过32'''
        func.log(u'--------------test_c8_add_text_attr_error_len 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_text_attr_error_len')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_text_attr(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_error_by_class(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：文本长度超过32错误提示预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_c8_add_text_attr_error_len 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_text_attr_error_init_value') == u'否', u'跳过执行')
    def test_c9_add_text_attr_error_init_value(self):
        u'''添加文本属性，文本长度小于初始值长度'''
        func.log(u'--------------test_c9_add_text_attr_error_init_value 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_text_attr_error_init_value')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_text_attr(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_error_by_class(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：文本长度小于初始值长度错误提示预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_c9_add_text_attr_error_init_value 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_number_attr_success') == u'否', u'跳过执行')
    def test_d1_add_number_attr_success(self):
        u'''添加数字属性成功'''
        func.log(u'--------------test_d1_add_number_attr_success 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_number_attr_success')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_number_attr(value_list)
            obj1.wait_message_visible()
            time.sleep(1)
            self.assertEqual(int(obj1.get_attr_value(value_list[3])), int(value_list[5]))
        except Exception:
            func.log(u'【断言失败】：' + u'属性名【' + value_list[3] + u'】的值预期为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_d1_add_number_attr_success 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_number_attr_same_para_name') == u'否', u'跳过执行')
    def test_d2_add_number_attr_same_para_name(self):
        u'''添加数字属性，字段重名'''
        func.log(u'--------------test_d2_add_number_attr_same_para_name 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_number_attr_same_para_name')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_number_attr(value_list)
            obj1.wait_message_visible()
            self.assertEqual(obj1.get_message(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：字段名重名预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_d2_add_number_attr_same_para_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_number_attr_error_para_name') == u'否', u'跳过执行')
    def test_d3_add_number_attr_error_para_name(self):
        u'''添加数字属性，字段格式错误'''
        func.log(u'--------------test_d3_add_number_attr_error_para_name 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_number_attr_error_para_name')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_number_attr(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_error_by_class(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：字段格式错误预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_d3_add_number_attr_error_para_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_number_attr_empty_para_name') == u'否',
                     u'跳过执行')
    def test_d4_add_number_attr_empty_para_name(self):
        u'''添加数字属性，字段名为空'''
        func.log(u'--------------test_d4_add_number_attr_empty_para_name 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_number_attr_empty_para_name')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_number_attr(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_error_by_class(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：字段名为空预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_d4_add_number_attr_empty_para_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_number_attr_empty_attr_name') == u'否',
                     u'跳过执行')
    def test_d5_add_number_attr_empty_attr_name(self):
        u'''添加数字属性，属性名为空'''
        func.log(u'--------------test_d5_add_number_attr_empty_attr_name 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_number_attr_empty_attr_name')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_number_attr(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_error_by_class(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：属性名为空预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_d5_add_number_attr_empty_attr_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_number_attr_empty_float_len') == u'否',
                     u'跳过执行')
    def test_d6_add_number_attr_empty_float_len(self):
        u'''添加数字属性，小数长度为空'''
        func.log(u'--------------test_d6_add_number_attr_empty_float_len 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_number_attr_empty_float_len')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_number_attr(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_error_by_class(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：小数长度为空预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_d6_add_number_attr_empty_float_len 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_number_attr_empty_init_value') == u'否',
                     u'跳过执行')
    def test_d7_add_number_attr_empty_init_value(self):
        u'''添加数字属性，初始值为空'''
        func.log(u'--------------test_d7_add_number_attr_empty_init_value 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_number_attr_empty_init_value')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_number_attr(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_error_by_class(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：初始值为空预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_d7_add_number_attr_empty_init_value 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_number_attr_error_init_value') == u'否',
                     u'跳过执行')
    def test_d8_add_number_attr_error_init_value(self):
        u'''添加数字属性，初始值小数位过长'''
        func.log(u'--------------test_d8_add_number_attr_error_init_value 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_number_attr_error_init_value')
        for i in value_list:
            print i
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_number_attr(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_error_by_class(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：初始值小数位过长预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_d8_add_number_attr_error_init_value 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_date_attr_success') == u'否',
                     u'跳过执行')
    def test_e1_add_date_attr_success(self):
        u'''添加日期属性成功'''
        func.log(u'--------------test_e1_add_date_attr_success 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_date_attr_success')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_date_attr(value_list)
            obj1.wait_message_visible()
            time.sleep(1)
            self.assertIn(value_list[4], obj1.get_date_attr_value(value_list[3]))
        except Exception:
            func.log(u'【断言失败】：' + u'属性名【' + value_list[3] + u'】的值预期为：' + func.get_now_date())
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e1_add_date_attr_success 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_date_attr_same_para_name') == u'否',
                     u'跳过执行')
    def test_e2_add_date_attr_same_para_name(self):
        u'''添加日期属性，字段重名'''
        func.log(u'--------------test_e2_add_date_attr_same_para_name 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_date_attr_same_para_name')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_date_attr(value_list)
            obj1.wait_message_visible()
            self.assertEqual(obj1.get_message(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：字段名重名预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e2_add_date_attr_same_para_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_date_attr_error_para_name') == u'否',
                     u'跳过执行')
    def test_e3_add_date_attr_error_para_name(self):
        u'''添加日期属性，字段格式错误'''
        func.log(u'--------------test_e3_add_date_attr_error_para_name 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_date_attr_error_para_name')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_date_attr(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_error_by_class(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：字段格式错误预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e3_add_date_attr_error_para_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_date_attr_empty_para_name') == u'否',
                     u'跳过执行')
    def test_e4_add_date_attr_empty_para_name(self):
        u'''添加日期属性，字段名为空'''
        func.log(u'--------------test_e4_add_date_attr_empty_para_name 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_date_attr_empty_para_name')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_date_attr(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_error_by_class(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：字段名为空预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e4_add_date_attr_empty_para_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_date_attr_empty_attr_name') == u'否',
                     u'跳过执行')
    def test_e5_add_date_attr_empty_attr_name(self):
        u'''添加日期属性，属性名为空'''
        func.log(u'--------------test_e5_add_date_attr_empty_attr_name 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_date_attr_empty_attr_name')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_date_attr(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_error_by_class(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：属性名为空预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e5_add_date_attr_empty_attr_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_add_date_attr_empty_init_value') == u'否',
                     u'跳过执行')
    def test_e6_add_date_attr_empty_init_value(self):
        u'''添加日期属性，初始值为空'''
        func.log(u'--------------test_e6_add_date_attr_empty_init_value 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_add_date_attr_empty_init_value')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            self.add_date_attr(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_error_by_class(), value_list[9])
        except Exception:
            func.log(u'【断言失败】：初始值为空预期结果为：' + value_list[9])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_e6_add_date_attr_empty_init_value 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_delete_attr') == u'否',
                     u'跳过执行')
    def test_f1_delete_attr(self):
        u'''删除自定义属性'''
        func.log(u'--------------test_f1_delete_attr 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet3, 'test_delete_attr')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            obj1.delete_attr(value_list)
            obj1.wait_message_visible()
            time.sleep(1)
            self.assertEqual(obj1.check_lable_in_page(value_list[1]), False)
        except Exception:
            func.log(u'【断言失败】：删除自定义属性失败，' + value_list[1] + u'属性仍存在')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_f1_delete_attr 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_delete_attr_error_input') == u'否',
                     u'跳过执行')
    def test_f2_delete_attr_error_input(self):
        u'''删除自定义属性_输入错误执行命令'''
        func.log(u'--------------test_f2_delete_attr_error_input 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet3, 'test_delete_attr_error_input')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            obj1.delete_attr(value_list)
            time.sleep(1)
            message = obj1.get_error_by_class()
            obj1.close_dialog()
            self.assertEqual(message, value_list[12])
        except Exception:
            func.log(u'【断言失败】：输入错误执行命令预期结果为：' + value_list[12])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_f2_delete_attr_error_input 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_edit_attr') == u'否',
                     u'跳过执行')
    def test_f3_edit_attr(self):
        u'''编辑自定义属性'''
        func.log(u'--------------test_f3_edit_attr 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet3, 'test_edit_attr')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            obj1.edit_attr(value_list)
            time.sleep(1)
            self.assertEqual(obj1.get_attr_value(value_list[6]), value_list[12])
        except Exception:
            func.log(u'【断言失败】：' + u'属性名【' + value_list[6] + u'】的值预期为：' + value_list[12])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_f3_edit_attr 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_product_delete') == u'否',
                     u'跳过执行')
    def test_g1_delete_product_success(self):
        u'''删除产品'''
        func.log(u'--------------test_g1_delete_product_success 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_product_delete')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            obj1.delete_product()
            obj1.wait_message_visible()
            time.sleep(1)
            self.assertEqual(obj1.get_message(), value_list[2])
        except Exception:
            func.log(u'【断言失败】：删除产品预期提示为：' + value_list[2])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_g1_delete_product_success 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_product_delete_released') == u'否', u'跳过执行')
    def test_g2_delete_product_released(self):
        print EX.get_case_status(self.data_path, self.data_sheet, 'test_product_delete_released')
        u'''删除产品_已发布产品无发删除'''
        func.log(u'--------------test_g2_delete_product_released 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_product_delete_released')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.edit_product()
            obj1.wait_edit_product_page()
            time.sleep(1)
            self.assertEqual(obj1.delete_checkbox_check(), False)
        except Exception:
            func.log(u'【断言失败】：删除产品checkbox状态预期提示为：False')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_g2_delete_product_released 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet3, 'test_config_attr') == u'否', u'跳过执行')
    def test_h1_config_attr(self):
        u'''配置显示自定义属性'''
        func.log(u'--------------test_h1_config_attr 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet3, 'test_config_attr')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.config_attr(value_list[1])
            time.sleep(2)
            obj1.click_trigger()
            self.assertEqual(obj1.get_lable_text(value_list[1]), value_list[12])
        except Exception:
            func.log(u'【断言失败】：自定义属性配置失败')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_h1_config_attr 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet4, 'test_register_device') == u'否', u'跳过执行')
    def test_i1_register_device(self):
        u'''注册设备页面跳转'''
        func.log(u'--------------test_i1_register_device 开始-------------')
        obj1 = ProductInfo(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet4, 'test_register_device')
        try:
            self.open_product_base_info(value_list)
            obj1.wait_quota_visible()
            time.sleep(1)
            obj1.click_button(u'设备注册')
            time.sleep(1)
            self.assertEqual(obj1.wait_count_visible(), True)
        except Exception:
            func.log(u'【断言失败】：页面未跳转到设备注册页面')
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_i1_register_device 结束-------------')






if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(ProductInfoTest('test_i1_register_device'))
    #suite.addTest(ProductInfoTest('test_h1_config_attr'))
    runner = unittest.TextTestRunner()
    runner.run(suite)