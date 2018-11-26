# coding=utf-8

import unittest
from common.driver import *
from common import myunit
from test_case.page_obj.registerPage import Register
from common import exceluitl as EX,  function as func
import sys, time
reload(sys)
sys.setdefaultencoding('utf-8')


class RegisterAccount(myunit.MyTest):
    u'''注册企业账户'''
    data_path = func.find_path() + '/test_data/login/register.xlsx'
    data_sheet = 'case'
    obj = None

    def open_page(self):
        self.obj = Register(self.driver)
        self.obj.open()
        self.obj.wait_element_register_visible()
        self.obj.click_register()
        time.sleep(1)

    def fill_content(self, value_list):
        self.obj.input_email(str(value_list[0]))
        self.obj.input_password(str(value_list[1]))
        self.obj.input_confirm_password(str(value_list[2]))
        self.obj.input_name(str(value_list[3]))
        self.obj.input_phone(str(value_list[4]))
        self.obj.input_company(str(value_list[5]))
        self.obj.select_type(str(value_list[6]))
        self.obj.click_checkbox(str(value_list[7]))
        self.obj.click_button(u'注册账号')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_a_register_success') == u'否', u'跳过执行')
    def test_z_register_success(self):
        u'''注册成功'''
        func.log(u'--------------test_a_register_success 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_a_register_success')
        try:
            self.open_page()
            self.fill_content(value_list)
            time.sleep(1)
            self.obj.wait_register_message_visible()
            self.assertEqual(self.obj.register_message(), value_list[8])
        except Exception as msg:
            func.log(u'【断言失败】成功注册预期提示信息：' + value_list[8])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a_register_success 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_empty_email') == u'否', u'跳过执行')
    def test_z_empty_email(self):
        u'''邮箱为空'''
        func.log(u'--------------test_empty_email 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_empty_email')
        try:
            self.open_page()
            self.fill_content(value_list)
            time.sleep(1)
            self.assertEqual(self.obj.empty_error_email(), value_list[8])
        except Exception as msg:
            func.log(u'【断言失败】邮箱为空预期提示信息：' + value_list[8])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_empty_email 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_error_email') == u'否', u'跳过执行')
    def test_error_email(self):
        u'''邮箱格式错误'''
        func.log(u'--------------test_error_email 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_error_email')
        try:
            self.open_page()
            self.fill_content(value_list)
            time.sleep(1)
            self.assertEqual(self.obj.empty_error_email(), value_list[8])
        except Exception as msg:
            func.log(u'【断言失败】邮箱格式错误预期提示信息：' + value_list[8])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_error_email 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_existed_email') == u'否', u'跳过执行')
    def test_existed_email(self):
        u'''邮箱已存在'''
        func.log(u'--------------test_existed_email 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_existed_email')
        try:
            self.open_page()
            self.fill_content(value_list)
            self.obj.wait_error_message_visible()
            self.assertEqual(self.obj.error_message(), value_list[8])
        except Exception as msg:
            func.log(u'【断言失败】邮箱已存在预期提示信息：' + value_list[8])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_existed_email 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_error_password') == u'否', u'跳过执行')
    def test_error_password(self):
        u'''密码格式错误'''
        func.log(u'--------------test_error_password 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_error_password')
        try:
            self.open_page()
            self.fill_content(value_list)
            time.sleep(1)
            self.assertEqual(self.obj.empty_error_password(), value_list[8])
        except Exception as msg:
            func.log(u'【断言失败】密码格式错误预期提示信息：' + value_list[8])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_error_password 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_empty_confirm_password') == u'否', u'跳过执行')
    def test_empty_confirm_password(self):
        u'''确认密码为空'''
        func.log(u'--------------test_empty_confirm_password 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_empty_confirm_password')
        try:
            self.open_page()
            self.fill_content(value_list)
            time.sleep(1)
            self.assertEqual(self.obj.confirm_password_error(), value_list[8])
        except Exception as msg:
            func.log(u'【断言失败】确认密码为空预期提示信息：' + value_list[8])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_empty_confirm_password 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_error_confirm_password') == u'否', u'跳过执行')
    def test_error_confirm_password(self):
        u'''确认密码不一致'''
        func.log(u'--------------test_error_confirm_password 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_error_confirm_password')
        try:
            self.open_page()
            self.fill_content(value_list)
            time.sleep(1)
            self.assertEqual(self.obj.confirm_password_error(), value_list[8])
        except Exception as msg:
            func.log(u'【断言失败】确认密码不一致预期提示信息：' + value_list[8])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_error_confirm_password 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_empty_name') == u'否', u'跳过执行')
    def test_empty_name(self):
        u'''姓名为空'''
        func.log(u'--------------test_empty_name 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_empty_name')
        try:
            self.open_page()
            self.fill_content(value_list)
            time.sleep(1)
            self.assertEqual(self.obj.name_empty(), value_list[8])
        except Exception as msg:
            func.log(u'【断言失败】姓名为空预期提示信息：' + value_list[8])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_empty_name 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_empty_phone') == u'否', u'跳过执行')
    def test_empty_phone(self):
        u'''手机号为空'''
        func.log(u'--------------test_empty_phone 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_empty_phone')
        try:
            self.open_page()
            self.fill_content(value_list)
            time.sleep(1)
            self.assertEqual(self.obj.phone_empty(), value_list[8])
        except Exception as msg:
            func.log(u'【断言失败】手机号为空预期提示信息：' + value_list[8])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_empty_phone 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_error_phone') == u'否', u'跳过执行')
    def test_error_phone(self):
        u'''手机号格式错误'''
        func.log(u'--------------test_error_phone 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_error_phone')
        try:
            self.open_page()
            self.fill_content(value_list)
            time.sleep(1)
            self.assertEqual(self.obj.phone_empty(), value_list[8])
        except Exception as msg:
            func.log(u'【断言失败】手机号格式错误预期提示信息：' + value_list[8])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_error_phone 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_empty_company') == u'否', u'跳过执行')
    def test_empty_company(self):
        u'''公司名称为空'''
        func.log(u'--------------test_empty_company 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_empty_company')
        try:
            self.open_page()
            self.fill_content(value_list)
            time.sleep(1)
            self.assertEqual(self.obj.company_empty(), value_list[8])
        except Exception as msg:
            func.log(u'【断言失败】公司名称为空预期提示信息：' + value_list[8])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_empty_company 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_error_company') == u'否', u'跳过执行')
    def test_error_company(self):
        u'''公司名称格式错误'''
        func.log(u'--------------test_error_company 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_error_company')
        try:
            self.open_page()
            self.fill_content(value_list)
            time.sleep(1)
            self.assertEqual(self.obj.company_empty(), value_list[8])
        except Exception as msg:
            func.log(u'【断言失败】公司名称格式错误预期提示信息：' + value_list[8])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_error_company 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_uncheck') == u'否', u'跳过执行')
    def test_uncheck(self):
        u'''不勾选"同意"'''
        func.log(u'--------------test_uncheck 开始-------------')
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_uncheck')
        try:
            self.open_page()
            self.fill_content(value_list)
            time.sleep(1)
            self.obj.wait_register_message_visible()
            self.assertEqual(self.obj.register_message(), value_list[8])
        except Exception as msg:
            func.log(u'【断言失败】不勾选"同意"预期提示信息：' + value_list[8])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_uncheck 结束-------------')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    #unittest.main()

    suite = unittest.TestSuite()
    suite.addTest(RegisterAccount('test_z_empty_email'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
