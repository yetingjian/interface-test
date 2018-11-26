from selenium import webdriver
from .driver import *
from test_case.page_obj.base import Page
from test_case.page_obj.loginPage import Login
from common import exceluitl as EX, function as func
import unittest
import os


class MyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = broswer_no_remote()
        cls.driver.implicitly_wait(20)
        cls.driver.maximize_window()

    # @classmethod
    # def tearDownClass(cls):
    #      cls.driver.quit()


class MyTestSigned(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        login_data_path = func.find_path() + '/test_data/login/login.xlsx'
        login_data_sheet = 'case'
        cls.driver = broswer_no_remote()
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        value_list = EX.get_case_list(login_data_path, login_data_sheet, 'test_login_success')
        obj1 = Login(cls.driver)
        obj1.user_login(username=value_list[0], password=value_list[1])
        obj1.wait_element_visible()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

