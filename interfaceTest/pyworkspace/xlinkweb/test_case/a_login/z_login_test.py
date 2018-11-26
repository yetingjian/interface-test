# coding=utf-8

import unittest
from common.driver import *
from common import myunit
from test_case.page_obj.loginPage import Login
from common import exceluitl as EX,  function as func
import sys, time



class LoginTest(myunit.MyTest):
    u'''登录'''
    data_path = func.find_path() + '/test_data/login/login.xlsx'
    data_sheet = 'case'
    # 测试用户登录

    def user_login_test(self, username='', password=''):
        Login(self.driver).user_login(username, password)

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_empty_password') == u'否', u'跳过执行')
    def test_empty_password(self):
        u'''密码为空'''
        func.log(u'--------------test_empty_user_password 开始-------------')
        obj = Login(self.driver)
        obj.page_refresh()
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_empty_password')
        try:
            self.user_login_test(username=value_list[0], password=value_list[1])
            self.assertEqual(obj.password_empty(), value_list[2])
        except Exception as msg:
            func.log(u'【断言失败】密码为空时预期提示信息：' + value_list[2])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_empty_user_password 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_empty_user') == u'否', u'跳过执行')
    def test_empty_user(self):
        u'''用户为空'''
        func.log(u'--------------test_empty_user 开始-------------')
        obj = Login(self.driver)
        obj.page_refresh()
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_empty_user')
        try:
            self.user_login_test(username=value_list[0], password=value_list[1])
            self.assertEqual(obj.user_empty(), value_list[2])
        except Exception as msg:
            func.log(u'【断言失败】用户为空时预期提示信息：' + value_list[2])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_empty_user 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_error_password') == u'否', u'跳过执行')
    def test_error_password(self):
        u'''密码错误'''
        func.log(u'--------------test_error_password 开始-------------')
        obj = Login(self.driver)
        obj.page_refresh()
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_error_password')
        try:
            self.user_login_test(username=value_list[0], password=value_list[1])
            obj.wait_error_message_visible()
            self.assertEqual(obj.password_error(), value_list[2])
        except Exception as msg:
            func.log(u'【断言失败】密码错误时预期提示信息：' + value_list[2])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_error_password 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_error_user') == u'否', u'跳过执行')
    def test_error_user(self):
        u'''用户错误'''
        func.log(u'--------------test_error_user 开始-------------')
        obj = Login(self.driver)
        obj.page_refresh()
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_error_user')
        try:
            self.user_login_test(username=value_list[0], password=value_list[1])
            obj.wait_error_message_visible()
            self.assertEqual(obj.user_error(), value_list[2])
        except Exception as msg:
            func.log(u'【断言失败】用户错误时预期提示信息：' + value_list[2])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_error_user 结束-------------')

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_login_success') == u'否', u'跳过执行')
    def test_z_login_success(self):
        u'''成功登录'''
        func.log(u'--------------test_login_success 开始-------------')
        obj = Login(self.driver)
        obj.page_refresh()
        value_list = EX.get_case_list(self.data_path, self.data_sheet, 'test_login_success')
        try:
            self.user_login_test(username=value_list[0], password=value_list[1])
            obj.wait_element_visible()
            time.sleep(1)
            self.assertEqual(obj.user_login_success(), value_list[2])
        except Exception as msg:
            func.log(u'【断言失败】成功登录后预期用户为：' + value_list[2])
            func.scream_shot(self.driver, 'login/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_login_success 结束-------------')


if __name__ == '__main__':
    # unittest.main()

    suite = unittest.TestSuite()
    suite.addTest(LoginTest('test_empty_password'))
    suite.addTest(LoginTest('test_empty_user'))
    runner = unittest.TextTestRunner()
    runner.run(suite)