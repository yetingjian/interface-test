# coding=utf-8
from selenium.webdriver.common.by import By
from test_case.page_obj import base
from base import Page
from common import exceluitl as EX, function as func


class Login(Page):
    data_path = func.find_path() + '/test_data/login/login.xlsx'
    data_sheet = 'locator'
    user_loc = (By.NAME, EX.get_locator_value(data_path, data_sheet, 'user_loc'))
    password_loc = (By.NAME, EX.get_locator_value(data_path, data_sheet, 'password_loc'))
    remember_check_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'remember_check_loc'))
    submit_loc = (By.ID, EX.get_locator_value(data_path, data_sheet, 'submit_loc'))
    user_password_error_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'user_password_error_loc'))
    check_error_message = EX.get_locator_value(data_path, data_sheet, 'user_password_error_loc')
    user_empty_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'user_empty_loc'))
    password_empty_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'password_empty_loc'))
    login_success_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'login_success_loc'))
    check_page_success = EX.get_locator_value(data_path, data_sheet, 'login_success_loc')
    check_page_forget = EX.get_locator_value(data_path, data_sheet, 'forget_password_loc')
    forget_password_loc = (By.CSS_SELECTOR, EX.get_locator_value(data_path, data_sheet, 'forget_password_loc'))
    input_email_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'input_email_loc'))
    email_empty_format_error_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet,
                                                                        'email_empty_format_error_loc'))
    email_error_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'email_error_loc'))
    find_by_email_success_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet,
                                                                     'find_by_email_success_loc'))
    verify_code_error_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'verify_code_error_loc'))
    phone_empty_error_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'phone_empty_error_loc'))
    empty_verify_code_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'empty_verify_code_loc'))
    password_error_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'password_error_loc'))
    password_diff_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'password_diff_loc'))
    find_by_phone_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'find_by_phone_loc'))
    phone_loc = (By.XPATH, u'//input[@placeholder="手机号码"]')
    verify_code_loc = (By.XPATH, u'//input[@placeholder="请输入短信验证码"]')
    phone_password_loc = (By.XPATH, u'//input[@placeholder="密码"]')
    phone_confirm_password_loc = (By.XPATH, u'//input[@placeholder="确认密码"]')

    # 输入用户名
    def login_username(self, username):
        try:
            obj = self.find_element(self.user_loc)
            obj.clear()
            obj.send_keys(username)
            func.log(u'输入用户名：' + username)
        except Exception:
            func.log(u'【异常】用户名输入框未找到')
            raise

    # 输入密码
    def login_password(self, password):
        try:
            self.find_element(self.password_loc).send_keys(password)
            func.log(u'输入密码：' + password)
        except Exception:
            func.log(u'【异常】密码输入框未找到')
            raise

    # 记住密码checkbox
    def login_checkbox(self):
        try:
            self.find_element(self.remember_check_loc).click()
            func.log(u'点击记住密码')
        except Exception:
            func.log(u'【异常】记住密码checkbox未找到')
            raise

    # 统一登录入口
    def user_login(self, username=None, password=None):
        self.open()
        self.login_username(username)
        self.login_password(password)
        self.login_checkbox()
        self.click_button(u'登录')

    def user_error(self):
        try:
            text = self.find_element(self.user_password_error_loc).text
            func.log(u'用户错误提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】用户错误提示未找到')
            raise

    def password_error(self):
        try:
            text = self.find_element(self.user_password_error_loc).text
            func.log(u'密码错误提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】密码错误提示未找到')
            raise

    def email_error(self):
        try:
            text = self.find_element(self.email_error_loc).text
            func.log(u'邮箱错误提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】邮箱错误提示未找到')
            raise

    def user_empty(self):
        try:
            text = self.find_element(self.user_empty_loc).text
            func.log(u'用户为空时提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】用户为空提示未找到')
            raise

    def password_empty(self):
        try:
            text = self.find_element(self.password_empty_loc).text
            func.log(u'密码为空时提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】密码为空提示未找到')
            raise

    def email_empty_format_error(self):
        try:
            text = self.find_element(self.email_empty_format_error_loc).text
            func.log(u'邮箱为空或格式错误时提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】邮箱为空或格式错误提示未找到')
            raise

    def verify_code_error(self):
        try:
            text = self.find_element(self.verify_code_error_loc).text
            func.log(u'错误提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】错误提示未找到')
            raise

    def phone_empty_format_error(self):
        try:
            text = self.find_element(self.phone_empty_error_loc).text
            func.log(u'手机号输入为空或格式错误时提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】手机号输入为空或格式错误提示未找到')
            raise

    def empty_verify_code(self):
        try:
            text = self.find_element(self.empty_verify_code_loc).text
            func.log(u'短信验证码为空时提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】短信验证码为空错误提示未找到')
            raise

    def phone_password_error(self):
        try:
            text = self.find_element(self.password_error_loc).text
            func.log(u'密码错误时提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】密码错误提示未找到')
            raise

    def password_diff(self):
        try:
            text = self.find_element(self.password_diff_loc).text
            func.log(u'确认密码不一致时提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】确认密码不一致提示未找到')
            raise

    def user_login_success(self):
        try:
            text = self.find_element(self.login_success_loc).text
            func.log(u'成功登录后的用户为：' + text)
            return text
        except Exception:
            func.log(u'【异常】成功登录后的用户名称元素未找到')
            raise

    def find_by_email_success(self):
        try:
            text = self.find_element(self.find_by_email_success_loc).text
            func.log(u'邮箱找回密码成功后提示信息为：' + text)
            return text
        except Exception:
            func.log(u'【异常】邮箱找回密码成功后提示未找到')
            raise

    def wait_element_visible(self):
        func.log(u'等待' + Login.check_page_success + u'元素可见')
        msg = self.wait_class_visible(self.check_page_success)
        if msg == 'Y':
            func.log(u'元素已可见')
        else:
            func.log(u'【异常】60秒后元素仍不可见')

    def wait_element_forget_visible(self):
        func.log(u'等待' + Login.check_page_forget + u'元素可见')
        msg = self.wait_css_visible(self.check_page_forget)
        if msg == 'Y':
            func.log(u'元素已可见')
        else:
            func.log(u'【异常】60秒后元素仍不可见')

    def wait_error_message_visible(self):
        func.log(u'等待' + Login.check_error_message + u'元素可见')
        msg = self.wait_class_visible(self.check_error_message)
        if msg == 'Y':
            func.log(u'元素已可见')
        else:
            func.log(u'【异常】60秒后元素仍不可见')

    def page_refresh(self):
        self.refresh_page()
        func.log(u'刷新页面')

    def click_forget_password(self):
        try:
            self.find_element(self.forget_password_loc).click()
            func.log(u'点击忘记密码')
        except Exception:
            func.log(u'【异常】忘记密码未找到')
            raise

    def find_by_phone(self):
        try:
            self.find_element(self.find_by_phone_loc).click()
            func.log(u'点击手机找回密码')
        except Exception:
            func.log(u'【异常】手机找回密码未找到')
            raise

    def input_email(self, text):
        try:
            self.find_element(self.input_email_loc).send_keys(text)
            func.log(u'输入邮箱：' + text)
        except Exception:
            func.log(u'【异常】邮箱输入框未找到')
            raise

    def input_phone(self, text):
        try:
            self.find_element(self.phone_loc).send_keys(text)
            func.log(u'输入手机号：' + text)
        except Exception:
            func.log(u'【异常】手机号输入框未找到')
            raise

    def input_verify_code(self, text):
        try:
            self.find_element(self.verify_code_loc).send_keys(text)
            func.log(u'输入验证码：' + text)
        except Exception:
            func.log(u'【异常】验证码输入框未找到')
            raise

    def input_phone_password(self, text):
        try:
            self.find_element(self.phone_password_loc).send_keys(text)
            func.log(u'输入登录密码：' + text)
        except Exception:
            func.log(u'【异常】登录密码输入框未找到')
            raise

    def input_phone_confirm_password(self, text):
        try:
            self.find_element(self.phone_confirm_password_loc).send_keys(text)
            func.log(u'输入登录确认密码：' + text)
        except Exception:
            func.log(u'【异常】登录确认密码输入框未找到')
            raise
