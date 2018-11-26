# coding=utf-8
from selenium.webdriver.common.by import By
from base import Page
from common import exceluitl as EX, function as func


class Register(Page):
    data_path = func.find_path() + '/test_data/login/register.xlsx'
    data_sheet = 'locator'
    register_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'register_loc'))
    check_page_register = EX.get_locator_value(data_path, data_sheet, 'register_loc')
    email_loc = (By.XPATH, u'//input[@placeholder="电子邮箱"]')
    password_loc = (By.XPATH, u'//input[@placeholder="请输入8-16位密码(必须包含数字与大小写字母)"]')
    confirm_password_loc = (By.XPATH, u'//input[@placeholder="确认密码"]')
    name_loc = (By.XPATH, u'//input[@placeholder="姓名"]')
    phone_loc = (By.XPATH, u'//input[@placeholder="手机号码"]')
    company_loc = (By.XPATH, u'//input[@placeholder="公司名称"]')
    select_loc = (By.CSS_SELECTOR, EX.get_locator_value(data_path, data_sheet, 'select_loc'))
    select_item_loc = (By.CSS_SELECTOR, EX.get_locator_value(data_path, data_sheet, 'select_item_loc'))
    checkbox_loc = (By.CSS_SELECTOR, EX.get_locator_value(data_path, data_sheet, 'checkbox_loc'))
    empty_email_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'empty_email_loc'))
    empty_error_password_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'empty_error_password_loc'))
    confirm_password_error_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'confirm_password_error_loc'))
    name_empty_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'name_empty_loc'))
    phone_empty_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'phone_empty_loc'))
    company_empty_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'company_empty_loc'))
    error_message_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'error_message_loc'))
    check_error_message = EX.get_locator_value(data_path, data_sheet, 'error_message_loc')
    register_success_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'register_success_loc'))
    check_register_message = EX.get_locator_value(data_path, data_sheet, 'register_success_loc')
    text1 = None

    def click_register(self):
        try:
            self.find_element(self.register_loc).click()
            func.log(u'点击注册企业账户')
        except Exception:
            func.log(u'【异常】注册企业账户链接未找到')
            raise

    def click_checkbox(self, text):
        try:
            if text == u'是':
                self.find_element(self.checkbox_loc).click()
                func.log(u'勾选同意云智易的使用条款和隐私权政策')
        except Exception:
            func.log(u'【异常】同意云智易的使用条款和隐私权政策checkbox未找到')
            raise

    def input_email(self, text):
        try:
            if text == u'随机数':
                text = func.random_string() + '@qq.com'
            self.find_element(self.email_loc).send_keys(text)
            func.log(u'输入邮箱：' + text)
        except Exception:
            func.log(u'【异常】邮箱输入框未找到')
            raise

    def input_password(self, text):
        try:
            self.find_element(self.password_loc).send_keys(text)
            func.log(u'输入密码：' + text)
        except Exception:
            func.log(u'【异常】密码输入框未找到')
            raise

    def input_confirm_password(self, text):
        try:
            self.find_element(self.confirm_password_loc).send_keys(text)
            func.log(u'输入确认密码：' + text)
        except Exception:
            func.log(u'【异常】确认密码输入框未找到')
            raise

    def input_name(self, text):
        try:
            self.find_element(self.name_loc).send_keys(text)
            func.log(u'输入姓名：' + text)
        except Exception:
            func.log(u'【异常】姓名输入框未找到')
            raise

    def input_phone(self, text):
        try:
            if text == u'随机数':
                text = '135' + str(func.random_num())
            self.find_element(self.phone_loc).send_keys(text)
            func.log(u'输入手机号码：' + text)
        except Exception:
            func.log(u'【异常】手机号码输入框未找到')
            raise

    def input_company(self, text):
        try:
            self.find_element(self.company_loc).send_keys(text)
            func.log(u'输入公司名称：' + text)
        except Exception:
            func.log(u'【异常】公司名称输入框未找到')
            raise

    def select_type(self, item):
        try:
            obj = self.find_element(self.select_loc)
            obj.click()
            list1 = self.find_elements(self.select_item_loc)
            for j in range(len(list1)):
                self.move_to_element(list1[j])
                if list1[j].text == item:
                    list1[j].click()
                    func.log(u'应用类型选择：' + item)
                    break
        except Exception:
            func.log(u'【异常】应用类型选择框未找到')
            raise

    def empty_error_email(self):
        try:
            text = self.find_element(self.empty_email_loc).text
            func.log(u'邮件为空或格式错误时提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】邮件为空或格式错误提示未找到')
            raise

    def empty_error_password(self):
        try:
            text = self.find_element(self.empty_error_password_loc).text
            func.log(u'密码为空或格式错误时提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】密码为空或格式错误提示未找到')
            raise

    def confirm_password_error(self):
        try:
            text = self.find_element(self.confirm_password_error_loc).text
            func.log(u'确认密码错误时提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】确认密码错误提示未找到')
            raise

    def name_empty(self):
        try:
            text = self.find_element(self.name_empty_loc).text
            func.log(u'姓名为空时提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】姓名为空时错误提示未找到')
            raise

    def phone_empty(self):
        try:
            text = self.find_element(self.phone_empty_loc).text
            func.log(u'手机号为空时提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】手机号为空错误提示未找到')
            raise

    def company_empty(self):
        try:
            text = self.find_element(self.company_empty_loc).text
            func.log(u'企业名称为空时提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】企业名称为空错误提示未找到')
            raise

    def register_message(self):
        try:
            text = self.find_element(self.register_success_loc).text
            func.log(u'注册提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】注册提示信息未找到')
            raise

    def error_message(self):
        try:
            text = self.find_element(self.error_message_loc).text
            func.log(u'错误信息为：' + text)
            return text
        except Exception:
            func.log(u'【异常】错误信息未找到')
            raise

    def wait_element_register_visible(self):
        func.log(u'等待' + Register.check_page_register + u'元素可见')
        msg = self.wait_class_visible(self.check_page_register)
        if msg == 'Y':
            func.log(u'元素已可见')
        else:
            func.log(u'【异常】60秒后元素仍不可见')

    def wait_error_message_visible(self):
        func.log(u'等待' + Register.check_error_message + u'元素可见')
        msg = self.wait_class_visible(self.check_error_message)
        if msg == 'Y':
            func.log(u'元素已可见')
        else:
            func.log(u'【异常】60秒后元素仍不可见')

    def wait_register_message_visible(self):
        func.log(u'等待' + Register.check_register_message + u'元素可见')
        msg = self.wait_class_visible(self.check_register_message)
        if msg == 'Y':
            func.log(u'元素已可见')
        else:
            func.log(u'【异常】60秒后元素仍不可见')