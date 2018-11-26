# coding=utf-8

import unittest
from V4.page_obj.Creart_Product_Process_Page import Login
from common import exceluitl as EX,  function as func
# import sys, time
from common.driver import broswer_no_remote
import sys, time
import gc
reload(sys)

class CreateProductProcessTest(unittest.TestCase):
    u'''新增产品'''
    data_path = func.find_path() + '/test_data/V4/V4.xlsx'
    data_sheet = 'login'
    data_sheet1 = 'creat_product_process'
    data_sheet2 = 'case2'
    min_value = None
    max_value = None
    url = ''


    # @classmethod
    # def setUpClass(cls):
    #     func.log(u'----------------------------------CreateProductProcessTest 开始-----------------------------------')
    #     cls.driver = Broswer.get_instance()

    @classmethod
    def setUpClass(cls):
        func.log(u'----------------------------------CreateProductProcessTest 开始-----------------------------------')
        cls.driver = broswer_no_remote()
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        value_list = EX.get_case_list(cls.data_path, cls.data_sheet, 'test_login_success')
        obj = Login(cls.driver)
        obj.user_login(username=value_list[0], password=value_list[1])
        time.sleep(2)
        obj.wait_Login_success()
        time.sleep(2)

    @unittest.skipIf(EX.get_case_status(data_path, data_sheet, 'test_create_product') == u'否', u'跳过执行')
    def test_a_create_product_success(self):
        u'''创建产品成功'''
        func.log(u'--------------test_a_create_product_success 开始-------------')
        # obj1 = CreateProduct(self.driver)
        value_list = EX.get_case_list(self.data_path, self.data_sheet1, 'test_create_product')
        try:
            self.new_product(value_list)
            time.sleep(1)
            self.obj1.wait_button_enabled_css(u'添加数据端点')
            CreateProductProcessTest.url = self.obj1.get_current_url()
            self.obj1.click_button(u'匹配完成，下一步')
            time.sleep(1)
            self.obj1.wait_success_tips_visible()
            self.assertEqual(self.obj1.create_success_message(), value_list[5])
        except Exception:
            func.log(u'【断言失败】创建产品成功后预期提示信息为：' + value_list[5])
            func.scream_shot(self.driver, 'devplatform/' + sys._getframe().f_code.co_name + '.jpg')
            raise
        finally:
            func.log(u'--------------test_a_create_product_success 结束-------------')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    #suite.addTest(CreateProductTest('test_a_create_product_success'))
    suite.addTest(CreateProductProcessTest('test_create_product'))
    #suite.addTest(CreateProductTest('test_g1_mod_library_add_empty_point_name'))
    runner = unittest.TextTestRunner()
    runner.run(suite)