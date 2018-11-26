# encoding: utf-8
from selenium import webdriver
import unittest


class OpenBroswer(unittest.TestCase):

    @classmethod
    def setUp(cls):
        global driver
        driver = webdriver.Firefox()
        base_url = "http://www.baidu.com"
        driver.get(base_url)


if __name__ == "__main__":
    unittest.main()