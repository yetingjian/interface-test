# coding=utf-8

import unittest
from common.driver import *
from common import myunit
from test_case.page_obj.loginPage import Login
from common import exceluitl as EX,  function as func
import sys, time
reload(sys)
sys.setdefaultencoding('utf-8')


class FindPassword(myunit.MyTest):
    u'''忘记密码'''
    data_path = func.find_path() + '/test_data/login/login.xlsx'
    data_sheet1 = 'case1'
    data_sheet2 = 'case2'
    obj = None

    def open_page(self):
        self.obj = Login(self.driver)
        self.obj.open()
        self.obj.wait_element_forget_visible()
        self.obj.click_forget_password()
        time.sleep(1)

    def fill_content(self, value_list):
        self.obj.input_phone(value_list[0])
        self.obj.input_verify_code(value_list[1])
        self.obj.input_phone_password(value_list[2])
        self.obj.input_phone_confirm_password(value_list[3])
        time.sleep(1)

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet1, 'test_find_password_by_email_success') == u'否', u'跳过执行')
    def test_find_password_by_email_success(self):
        u'''输入正确邮箱'''
        func.log(u'--------------test_find_password_by_email_success 开始-------------')
        self.open_page()
        value_list = EX.get_case_list(self.data_path, self.data_sheet1, 'test_find_password_by_email_success')
        try:
            self.obj.input_email(value_list[0])
            self.obj.click_button(u'确定')
            time.sleep(1)
            self.assertEqual(self.obj.find_by_email_success(), value_list[1])
        except Exception as msg:
            func.log(u'【断言失败】密码为空时预期提示信息：' + value_list[1])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_find_password_by_email_success 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet1, 'test_email_empty') == u'否', u'跳过执行')
    def test_email_empty(self):
        u'''邮箱为空'''
        func.log(u'--------------test_email_empty 开始-------------')
        self.open_page()
        value_list = EX.get_case_list(self.data_path, self.data_sheet1, 'test_email_empty')
        try:
            self.obj.input_email(value_list[0])
            self.obj.click_button(u'确定')
            time.sleep(1)
            self.assertEqual(self.obj.email_empty_format_error(), value_list[1])
        except Exception as msg:
            func.log(u'【断言失败】密码为空时预期提示信息：' + value_list[1])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_email_empty 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet1, 'test_email_not_exist') == u'否', u'跳过执行')
    def test_email_not_exist(self):
        u'''邮箱不存在'''
        func.log(u'--------------test_email_not_exist 开始-------------')
        self.open_page()
        value_list = EX.get_case_list(self.data_path, self.data_sheet1, 'test_email_not_exist')
        try:
            self.obj.input_email(value_list[0])
            self.obj.click_button(u'确定')
            self.obj.wait_error_message_visible()
            self.assertEqual(self.obj.email_error(), value_list[1])
        except Exception as msg:
            func.log(u'【断言失败】密码为空时预期提示信息：' + value_list[1])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_email_not_exist 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet1, 'test_email_format_error') == u'否', u'跳过执行')
    def test_email_format_error(self):
        u'''邮箱格式错误'''
        func.log(u'--------------test_email_not_exist 开始-------------')
        self.open_page()
        value_list = EX.get_case_list(self.data_path, self.data_sheet1, 'test_email_format_error')
        try:
            self.obj.input_email(value_list[0])
            self.obj.click_button(u'确定')
            time.sleep(1)
            self.assertEqual(self.obj.email_empty_format_error(), value_list[1])
        except Exception as msg:
            func.log(u'【断言失败】密码为空时预期提示信息：' + value_list[1])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_email_not_exist 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_verify_code_error') == u'否', u'跳过执行')
    def test_z_verify_code_error(self):
        u'''手机找回验证码错误'''
        func.log(u'--------------test_verify_code_error 开始-------------')
        self.open_page()
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_verify_code_error')
        try:
            self.obj.find_by_phone()
            time.sleep(1)
            self.fill_content(value_list)
            self.obj.click_button(u'确定')
            self.obj.wait_error_message_visible()
            self.assertEqual(self.obj.verify_code_error(), value_list[4])
        except Exception as msg:
            func.log(u'【断言失败】密码为空时预期提示信息：' + value_list[4])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_verify_code_error 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_phone_error') == u'否', u'跳过执行')
    def test_z_phone_error(self):
        u'''手机号格式错误'''
        func.log(u'--------------test_phone_error 开始-------------')
        self.open_page()
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_phone_error')
        try:
            self.obj.find_by_phone()
            time.sleep(1)
            self.fill_content(value_list)
            self.obj.click_button(u'确定')
            time.sleep(1)
            self.assertEqual(self.obj.phone_empty_format_error(), value_list[4])
        except Exception as msg:
            func.log(u'【断言失败】密码为空时预期提示信息：' + value_list[4])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_phone_error 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_empty_verify_code') == u'否', u'跳过执行')
    def test_z_empty_verify_code(self):
        u'''验证码为空'''
        func.log(u'--------------test_empty_verify_code 开始-------------')
        self.open_page()
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_empty_verify_code')
        try:
            self.obj.find_by_phone()
            time.sleep(1)
            self.fill_content(value_list)
            self.obj.click_button(u'确定')
            time.sleep(1)
            self.assertEqual(self.obj.empty_verify_code(), value_list[4])
        except Exception as msg:
            func.log(u'【断言失败】密码为空时预期提示信息：' + value_list[4])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_empty_verify_code 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_password_diff') == u'否', u'跳过执行')
    def test_z_password_diff(self):
        u'''确认密码不一致'''
        func.log(u'--------------test_password_diff 开始-------------')
        self.open_page()
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_password_diff')
        try:
            self.obj.find_by_phone()
            time.sleep(1)
            self.fill_content(value_list)
            self.obj.click_button(u'确定')
            time.sleep(1)
            self.assertEqual(self.obj.password_diff(), value_list[4])
        except Exception as msg:
            func.log(u'【断言失败】密码为空时预期提示信息：' + value_list[4])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_password_diff 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_empty_phone') == u'否', u'跳过执行')
    def test_z_empty_phone(self):
        u'''手机号为空'''
        func.log(u'--------------test_empty_phone 开始-------------')
        self.open_page()
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_empty_phone')
        try:
            self.obj.find_by_phone()
            time.sleep(1)
            self.fill_content(value_list)
            self.obj.click_button(u'确定')
            time.sleep(1)
            self.assertEqual(self.obj.phone_empty_format_error(), value_list[4])
        except Exception as msg:
            func.log(u'【断言失败】密码为空时预期提示信息：' + value_list[4])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_empty_phone 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet2, 'test_password_error') == u'否', u'跳过执行')
    def test_z_password_error(self):
        u'''密码格式错误'''
        func.log(u'--------------test_password_error 开始-------------')
        self.open_page()
        value_list = EX.get_case_list(self.data_path, self.data_sheet2, 'test_password_error')
        try:
            self.obj.find_by_phone()
            time.sleep(1)
            self.fill_content(value_list)
            self.obj.click_button(u'确定')
            time.sleep(1)
            self.assertEqual(self.obj.phone_password_error(), value_list[4])
        except Exception as msg:
            func.log(u'【断言失败】密码为空时预期提示信息：' + value_list[4])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_password_error 结束-------------')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    #unittest.main()

    suite = unittest.TestSuite()
    suite.addTest(FindPassword('test_z_empty_phone'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
