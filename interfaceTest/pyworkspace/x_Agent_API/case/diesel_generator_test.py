# coding=utf-8

import unittest
from common import api_operation as api
import json
from common import function as func
import traceback
import operator
from HTMLTestRunner import HTMLTestRunner
import time

class ApiTest(unittest.TestCase):
    dicts = {}
    dicts1 = {"service_name": "diesel_generator", "object_name": "generator"}
    dicts2 = {"service_name": "diesel_generator", "object_name": "generator_fault"}
    api_path = func.find_path() + u"\\data\\API_list\\BA对接说明-柴电发电机.xlsx"
    body_data = {}
    @classmethod
    def setUpClass(cls):
        api.get_access_token()

    def base_operation(self):
        api.get_start_end_rows(self.dicts, self.api_path)
        api.modify_body_base(self.dicts)
        api.get_objects_values(api.start_row, api.end_row, self.api_path)
        self.count_id, self.verify_data = api.get_query_json(self.dicts)

    def test_a1_diesel_generator_generator_south(self):
        func.log('----------------------test_a1_diesel_generator_generator_south---------------------')
        self.dicts = self.dicts1
        api.body_json = {}
        self.base_operation()
        ApiTest.body_data = api.create_data_normal()
        api.body_json['data'] = ApiTest.body_data
        func.log(u'请求的json为：' + json.dumps(api.body_json))
        self.res = api.post_south_api(api.south_api_url, api.body_json, api.headers)
        api.assert_status(self.res["msg"])

    def test_a2_diesel_generator_generator_north_by_id(self):
        func.log('----------------------test_a2_diesel_generator_generator_north_by_id---------------------')
        self.dicts = self.dicts1
        self.dicts["id_num"] = str(api.id_str)
        res2 = api.get_data_api(self.dicts)
        api.assert_body_data(ApiTest.body_data, res2)

    def test_a3_diesel_generator_generator_north_total(self):
        func.log('----------------------test_a3_diesel_generator_generator_north_total---------------------')
        self.dicts = self.dicts1
        self.count_id, self.verify_data = api.get_query_json(self.dicts)
        api.assert_body_data(ApiTest.body_data, self.verify_data)

    def test_a4_diesel_generator_generator_invalid_value(self):
        func.log('----------------------test_a4_diesel_generator_generator_invalid_value---------------------')
        self.dicts = self.dicts1
        api.body_json = {}
        api.modify_body_base(self.dicts)
        ApiTest.body_data, invalid_value = api.create_data_invalid_value()
        api.body_json['data'] = ApiTest.body_data
        func.log(u'请求的json为：' + json.dumps(api.body_json))
        self.res = api.post_south_api(api.south_api_url, api.body_json, api.headers)
        api.assert_invalid_value(invalid_value, self.res)

    def test_a5_diesel_generator_generator_not_empty(self):
        func.log('----------------------test_a5_diesel_generator_generator_not_empty---------------------')
        self.dicts = self.dicts1
        api.body_json = {}
        api.modify_body_base(self.dicts)
        ApiTest.body_data, invalid_value = api.create_data_non_empty()
        api.body_json['data'] = ApiTest.body_data
        func.log(u'请求的json为：' + json.dumps(api.body_json))
        self.res = api.post_south_api(api.south_api_url, api.body_json, api.headers)
        api.assert_invalid_value(invalid_value, self.res)

    def test_a6_diesel_generator_generator_invalid_range(self):
        func.log('----------------------test_a6_diesel_generator_generator_invalid_range---------------------')
        self.dicts = self.dicts1
        api.body_json = {}
        api.modify_body_base(self.dicts)
        ApiTest.body_data, invalid_value = api.create_data_invalid_range()
        api.body_json['data'] = ApiTest.body_data
        func.log(u'请求的json为：' + json.dumps(api.body_json))
        self.res = api.post_south_api(api.south_api_url, api.body_json, api.headers)
        api.assert_invalid_value(invalid_value, self.res)

    def test_b1_diesel_generator_generator_fault_south(self):
        func.log('----------------------test_b1_diesel_generator_generator_fault_south---------------------')
        self.dicts = self.dicts2
        api.body_json = {}
        self.base_operation()
        ApiTest.body_data = api.create_data_normal()
        api.body_json['data'] = ApiTest.body_data
        func.log(u'请求的json为：' + json.dumps(api.body_json))
        self.res = api.post_south_api(api.south_api_url, api.body_json, api.headers)
        api.assert_status(self.res["msg"])

    def test_b2_diesel_generator_generator_fault_north_by_id(self):
        func.log('----------------------test_b2_diesel_generator_generator_fault_north_by_id---------------------')
        self.dicts = self.dicts2
        self.dicts["id_num"] = str(api.id_str)
        res2 = api.get_data_api(self.dicts)
        api.assert_body_data(ApiTest.body_data, res2)

    def test_b3_diesel_generator_generator_fault_north_total(self):
        func.log('----------------------test_b3_diesel_generator_generator_fault_north_total---------------------')
        self.dicts = self.dicts2
        self.count_id, self.verify_data = api.get_query_json(self.dicts)
        api.assert_body_data(ApiTest.body_data, self.verify_data)

    def test_b4_diesel_generator_generator_fault_invalid_value(self):
        func.log('----------------------test_b4_diesel_generator_generator_fault_invalid_value---------------------')
        self.dicts = self.dicts2
        api.body_json = {}
        api.modify_body_base(self.dicts)
        ApiTest.body_data, invalid_value = api.create_data_invalid_value()
        api.body_json['data'] = ApiTest.body_data
        func.log(u'请求的json为：' + json.dumps(api.body_json))
        self.res = api.post_south_api(api.south_api_url, api.body_json, api.headers)
        api.assert_invalid_value(invalid_value, self.res)

    def test_b5_diesel_generator_generator_fault_not_empty(self):
        func.log('----------------------test_b5_diesel_generator_generator_fault_not_empty---------------------')
        self.dicts = self.dicts2
        api.body_json = {}
        api.modify_body_base(self.dicts)
        ApiTest.body_data, invalid_value = api.create_data_non_empty()
        api.body_json['data'] = ApiTest.body_data
        func.log(u'请求的json为：' + json.dumps(api.body_json))
        self.res = api.post_south_api(api.south_api_url, api.body_json, api.headers)
        api.assert_invalid_value(invalid_value, self.res)

    def test_b6_diesel_generator_generator_fault_invalid_range(self):
        func.log('----------------------test_b6_diesel_generator_generator_fault_invalid_range---------------------')
        self.dicts = self.dicts2
        api.body_json = {}
        api.modify_body_base(self.dicts)
        ApiTest.body_data, invalid_value = api.create_data_invalid_range()
        api.body_json['data'] = ApiTest.body_data
        func.log(u'请求的json为：' + json.dumps(api.body_json))
        self.res = api.post_south_api(api.south_api_url, api.body_json, api.headers)
        api.assert_invalid_value(invalid_value, self.res)


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    suite = unittest.TestSuite()
    # suite.addTest(ApiTest('test_a1_diesel_generator_generator_south'))
    # suite.addTest(ApiTest('test_a2_diesel_generator_generator_north_by_id'))
    # suite.addTest(ApiTest('test_a3_diesel_generator_generator_north_total'))
    # suite.addTest(ApiTest('test_a4_diesel_generator_generator_invalid_value'))
    # suite.addTest(ApiTest('test_a5_diesel_generator_generator_not_empty'))
    # suite.addTest(ApiTest('test_a6_diesel_generator_generator_invalid_range'))
    suite.addTest(ApiTest('test_b1_diesel_generator_generator_fault_south'))
    suite.addTest(ApiTest('test_b2_diesel_generator_generator_fault_north_by_id'))
    suite.addTest(ApiTest('test_b3_diesel_generator_generator_fault_north_total'))
    suite.addTest(ApiTest('test_b4_diesel_generator_generator_fault_invalid_value'))
    suite.addTest(ApiTest('test_b5_diesel_generator_generator_fault_not_empty'))
    suite.addTest(ApiTest('test_b6_diesel_generator_generator_fault_invalid_range'))
    runner.run(suite)



