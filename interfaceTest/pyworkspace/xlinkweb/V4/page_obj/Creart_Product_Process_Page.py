# coding=utf-8
import time
from selenium.webdriver.common.by import By
from test_case.page_obj import base
from test_case.page_obj.base import Page
from common import exceluitl as EX, function as func


class Login(Page):

    def login_username(self, username):
        try:
            obj = self.find_element((By.NAME,'model.account'))
            # self.clear(obj)
            obj.send_keys(username)
            func.log(u'输入用户名：' + username)
        except Exception:
            func.log(u'【异常】用户名输入框未找到')
            raise

    # 输入密码
    def login_password(self, password):
        try:
            obj = self.find_element((By.NAME,'model.password'))
            # self.clear(obj)
            obj.send_keys(password)
            func.log(u'输入密码：' + password)
        except Exception:
            func.log(u'【异常】密码输入框未找到')
            raise

    # 记住密码checkbox
    def login_checkbox(self):
        try:
            self.find_element((By.CLASS_NAME,'checkbox')).click()
            func.log(u'点击记住密码')
        except Exception:
            func.log(u'【异常】记住密码checkbox未找到')
            raise

    # 统一登录入口
    def user_login(self, username=None, password=None):
        self.open_url_with_host('https://admin.xlink.cn/#!/login')
        self.login_username(username)
        self.login_password(password)
        # self.login_checkbox()
        self.click_button(u'登录')

    def wait_Login_success(self):
        func.log(u'等待footer元素可见')
        msg = self.wait_class_visible('footer')
        if msg == 'Y':
            func.log(u'元素已可见')
        else:
            func.log(u'【异常】60秒后元素仍不可见')

    def click_dev_platform(self):
        self.find_element_by_xpath('.//*[@id="app"]/div/div[1]/div[1]/div/div[4]/button').click()
        time.sleep(1)

    def new_product(self):
        self.open_V4_home_page()
        time.sleep(1)
        self.click_dev_platform()
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