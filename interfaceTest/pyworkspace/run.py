# encoding: utf-8
import unittest
import init


class Case1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver1 = init.driver

    def test_search(self):
        self.driver1.find_element_by_id("kw").send_keys('search')
        self.driver1.find_element_by_id("su").click()
        self.driver1.find_element_by_class_name('toindex').click()




