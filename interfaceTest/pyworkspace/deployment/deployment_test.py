# coding=utf-8
import threading
import unittest

from datetime import datetime, date, timedelta

import api_operation as api
import json
import function as func
import traceback
import requests
import serial_method as ser
from urllib3 import encode_multipart_formdata
import operator
from HTMLTestRunnerDep import HTMLTestRunner, _TestResult
import time
import check_email as che


class ApiTest(unittest.TestCase):
    user_headers = {"Content-Type": "application/json", "Access-Token": "token_value"}
    global false, true
    false = False
    true = True
    host = 'http://api2.xlink.cn'
    port = ''
    avs_host = 'http://avs.xlink.cn'
    avs_port = ''
    google_home_host = 'http://avs-ge-test.xlink.cn'
    google_home_port = ':9999'
    tm_host = ''
    tm_port = ''
    member = "wangqi@xlink.cn"
    mem_password = 'Test1234'
    mem_id = ''
    corp_id = '100fa2b414b2f200'
    pid = '160fa6b2d86003e9160fa6b2d860f201'
    p_key = '7a76d32732cc0654ab08e5d5509457ae'
    device_id = '1658785277'
    index_sys = None
    index_custom = None
    point_id_sys = None
    point_id_custom = None
    MAC = 'F0FE6B792673'
    exception_id = None
    snapshot_id = None
    tag_id = None
    mcu1_url = None
    mcu1_md5 = None
    mcu1_size = None
    mcu2_url = None
    mcu2_md5 = None
    mcu2_size = None
    mcu3_url = None
    mcu3_md5 = None
    mcu3_size = None
    mcu_task_id_auto = None
    mcu_task_id_manu = None
    user_phone = '15018753353'
    user_email = 'wangqi@xlink.cn'
    user_password = 'Test1234'
    user_id = None
    qrcode = None
    app_id = None
    desc = None
    email_account = 'wangqi@xlink.cn'
    email_password = '120211Qq'
    devices_summary = []
    alarm_summary = []
    map_summary = []

    def start_email_listen(self):
        t = threading.Thread(target=ApiTest.check_new_email_and_operation)
        t.setDaemon(True)
        t.start()

    @staticmethod
    def check_new_email_and_operation():
        u'''检查是否收到测试邮件'''
        while True:
            num = func.get_email_unseen(ApiTest.email_account, ApiTest.email_password)
            if int(num) > 0:
                active_url, flag = che.get_active_url(ApiTest.email_account, ApiTest.email_password)
                if flag == 1:
                    che.check_user_register_email(active_url)
                    func.set_email_seen(ApiTest.email_account, ApiTest.email_password)
                elif flag == 2:
                    che.reset_password(active_url,ApiTest.user_password)
                    func.set_email_seen(ApiTest.email_account, ApiTest.email_password)
            else:
                time.sleep(1)

    def test_member_forgot_password(self):
        """企业成员找回密码"""
        url = self.host + self.port + '/v2/corp/password/forgot/email'
        body = {"email":self.member}
        func.log(u'-----开始企业成员找回密码-----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            requests.post(url=url, json=body, headers=api.headers)
            func.log(u'企业成员找回密码接口请求成功')
        except Exception:
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            time.sleep(5)
            pass

    @staticmethod
    def test_init_device():
        u'''重置设备'''
        try:
            func.log(u'-----------------------------------开始测试---------------------------------')
            func.log(u'----开始重置设备----')
            ser.find_serial('COM3')
            ser.reset_mcu()
            time.sleep(20)
        except Exception:
            func.log(u'【重置设备失败】')
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    @staticmethod
    def test_init_device2():
        u'''重置设备'''
        try:
            func.log(u'-----------------------------------开始测试---------------------------------')
            func.log(u'----开始重置设备----')
            # ser.find_serial('COM3')
            ser.reset_mcu()
            time.sleep(20)
        except Exception:
            func.log(u'【重置设备失败】')
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_member_login(self):
        u'''企业成员登录'''
        _TestResult.des = u'管理台基础功能服务'
        url = self.host + self.port + '/v2/corp_auth'
        body = {"account": self.member, "password": self.mem_password}
        ApiTest.corp_id = api.get_access_token(url, body)
        total, online, offline, exception = api.get_device_summary(self.host, self.port)
        ApiTest.devices_summary.append(total)
        ApiTest.devices_summary.append(online)
        ApiTest.devices_summary.append(offline)
        ApiTest.devices_summary.append(exception)
        alarms, exceptions, today_alarms, condition_alarams = api.get_alarm_summary(self.host, self.port)
        ApiTest.alarm_summary.append(alarms)
        ApiTest.alarm_summary.append(exceptions)
        ApiTest.alarm_summary.append(today_alarms)
        ApiTest.alarm_summary.append(condition_alarams)
        total, online, exception = api.get_map_summary(self.host, self.port)
        ApiTest.map_summary.append(total)
        ApiTest.map_summary.append(online)
        ApiTest.map_summary.append(exception)

    def test_create_product(self):
        u'''创建产品'''
        _TestResult.des = u'管理台基础功能服务'
        # func.set_email_seen(self.user_email, self.user_password)  # 设置所有邮件已读
        res = ''
        url = self.host + self.port + '/v2/product'
        body = {"name": "product_" + time.strftime("%Y-%m-%d"), "link_type": 1, "description": "",
                "is_gateway_device": False}
        func.log(u'-----开始创建产品接口-----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("id", res)
            ApiTest.pid = res["id"]
            ApiTest.p_key = res["key"]
            func.log(u'创建产品接口响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_add_member(self):
        u'''添加企业成员'''
        _TestResult.des = u'管理台基础功能服务'
        res = ''
        url = self.host + self.port + '/v2/corp/member_add'
        body = {"email": self.user_email, "phone": self.user_phone, "name": "test", "password": self.mem_password,
                "type": 99}
        func.log(u'-----开始添加企业成员----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("id", res)
            ApiTest.mem_id = res["id"]
            func.log(u'创建添加企业成员响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_add_data_point_sys(self):
        u'''添加数据端点$1002'''
        _TestResult.des = u'管理台基础功能服务'
        res = ''
        url = self.host + self.port + '/v2/product/' + str(self.pid) + '/datapoint'
        body = {
            "name": "$1002",
            "field_name": "name",
            "type": 1,
            "index": 0,
            "description": u"开关开启时可进行二维码订阅",
            "symbol": "",
            "source": 1,
            "is_read": True,
            "is_write": 1
        }
        func.log(u'----开始创建$1002数据端点----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("id", res)
            ApiTest.index_sys = res["index"]
            ApiTest.point_id_sys = res["id"]
            func.log(u'创建$1002数据端点响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_add_data_point_custom(self):
        u'''添加数据端点byte'''
        _TestResult.des = u'管理台基础功能服务'
        res = ''
        url = self.host + self.port + '/v2/product/' + str(self.pid) + '/datapoint'
        body = {
            "name": "para_name",
            "field_name": "point_name",
            "type": 2,
            "index": 1,
            "description": "",
            "symbol": "",
            "source": 1,
            "is_read": True,
            "is_write": 1,
            "min": 0,
            "max": 255
        }
        func.log(u'----开始创建自定义数据端点----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("id", res)
            ApiTest.index_custom_ = res["index"]
            ApiTest.point_id_custom = res["id"]
            func.log(u'创建自定义数据端点响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_register_device(self):
        u'''注册设备'''
        _TestResult.des = u'管理台基础功能服务'
        res = ''
        url = self.host + self.port + '/v2/product/' + str(self.pid) + '/device'
        body = {
            "mac": self.MAC,
            "sn": func.random_num(),
            "name": "TEST_1"
        }
        func.log(u'----开始添加设备----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("id", res)
            ApiTest.device_id = res["id"]
            ApiTest.MAC = res["mac"]
            func.log(u'添加设备响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_alter_rule(self):
        u'''设置异常规则'''
        _TestResult.des = u'告警服务'
        res = ''
        url = self.host + self.port + '/v2/alert/rule'
        url_get_list = self.host + self.port + '/v2/exception/tags'
        r1 = requests.get(url=url_get_list, json={}, headers=api.headers)
        res1 = eval(r1.text)
        ApiTest.tag_id = res1["list"][2]["id"]
        body = {
            "name": "test_exception",
            "deviceOnline": "online",
            "content": "value>100",
            "product_id": self.pid,
            "tag": "",
            "scope": 4,
            "source": 1,
            "is_enable": true,
            "notify_type": 2,
            "notify_target": [

            ],
            "notify_apps": [

            ],
            "exception": {
                "tag_id": self.tag_id,
                "suggestions": ""
            },
            "notification": {
                "is_enable": false,
                "conditions": {
                    "times": 1
                },
                "scope": {
                    "member": {
                        "is_all": true,
                        "department_ids": [

                        ],
                        "position_ids": [

                        ],
                        "member_ids": [

                        ]
                    }
                }
            },
            "param": self.point_id_custom,
            "type": 1,
            "compare": 2,
            "value": "100"
        }
        func.log(u'----开始设置异常规则----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("id", res)
            ApiTest.exception_id = res["id"]
            func.log(u'设置异常规则响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_alarm_setting(self):
        u'''添加报警设置'''
        _TestResult.des = u'告警服务'
        res = ''
        url = self.host + self.port + '/v2/alert/rule/' + str(self.exception_id)
        body = {
            "exception": {
                "tag_id": self.tag_id,
                "suggestions": ""
            },
            "compare": 2,
            "is_enable": true,
            "source": 0,
            "type": 1,
            "version": 1,
            "content": "value>100",
            "notify_type": 2,
            "notify_apps": [

            ],
            "notification": {
                "is_enable": true,
                "scope": {
                    "member": {
                        "is_all": true,
                        "member_ids": [

                        ],
                        "department_ids": [

                        ],
                        "position_ids": [

                        ]
                    }
                },
                "conditions": {
                    "times": 1
                }
            },
            "notify_target": [
                2
            ],
            "param": self.point_id_custom,
            "product_id": self.pid,
            "scope": 1,
            "name": "test_exception",
            "interval": 0,
            "id": self.exception_id,
            "tag": "",
            "value": "100"
        }
        func.log(u'----开始报警设置----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.put(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("id", res)
            func.log(u'报警设置响应：' + json.dumps(res))
            # time.sleep(120)
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_snapshot(self):
        u'''添加快照'''
        _TestResult.des = u'快照服务'
        res = ''
        url = self.host + self.port + '/v2/product/' + self.pid + '/snapshot'
        body = {"rule": 1,
                "storage": {"expire": 0},
                "datapoint": [1],
                "name": "sanp_name"
                }
        func.log(u'----开始设置快照----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            ApiTest.snapshot_id = res["id"]
            self.assertIn("id", res)
            func.log(u'设置快照响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_statistic_rule(self):
        u'''添加统计规则'''
        _TestResult.des = u'快照服务'
        res = ''
        url = self.host + self.port + '/v2/product/' + self.pid + '/snapshot/' + str(
            self.snapshot_id) + '/statistic_rule'
        body = {
            "dp_mode": [
                {
                    "index": 1,
                    "mode": 1
                },
                {
                    "index": 1,
                    "mode": 2
                },
                {
                    "index": 1,
                    "mode": 3
                },
                {
                    "index": 1,
                    "mode": 4
                }
            ],
            "fineness": [
                6
            ],
            "name": "rule_name",
            "describe": "rule_description",
            "type": 2,
            "status": 1
        }
        func.log(u'----开始设置统计规则----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("id", res)
            func.log(u'统计规则响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_set_task(self):
        """添加定时任务"""
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.999Z")
        end = (date.today() + timedelta(days=+1)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        res = ''
        url = self.host + self.port + '/v2/timer/task'
        body = {
            "name": "task",
            "desc": "task",
            "actions": [{
                "type": "1",
                "name": "start",
                "moment": "00:00:00",
                "config": {
                    "device_id": self.device_id,
                    "datapoint": [{
                        "index": "1",
                        "value": 11
                    }]
                }
            }
            ],
            "timer": {
                "type": "1",
                "first_execute_time": now,
                "last_execute_time": end,
                "schedule": {

                    "exclude_day": [

                    ]
                }
            }
        }
        func.log(u'----开始添加定时任务----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("id", res)
            func.log(u'添加定时任务响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_active_device(self):
        u'''串口激活设备'''
        _TestResult.des = u'MQTT连接服务'
        try:
            func.log(u'----开始调串口激活设备----')
            # ser.find_serial('COM3')
            result = ser.set_PID_PKEY(self.pid, self.p_key)
            self.assertEqual(result, True)
            time.sleep(120)
        except Exception:
            func.log(u'【串口激活设备失败】')
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_active_device2(self):
        u'''串口激活设备'''
        _TestResult.des = u'MQTT连接服务'
        try:
            func.log(u'----开始调串口激活设备----')
            # ser.find_serial('COM3')
            result = ser.set_PID_PKEY(self.pid, self.p_key)
            self.assertEqual(result, True)
            time.sleep(120)
        except Exception:
            func.log(u'【串口激活设备失败】')
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_wide_devices(self):
        u'''查询宽表设备列表'''
        _TestResult.des = u'虚拟设备服务'
        res = ''
        url = self.host + self.port + '/v2/wide-devices'
        body = {
            "offset": 0,
            "limit": 100,
            "filter": [
                "product_id",
                "id",
                "is_active",
                "is_online"
            ],
            "query": {
                "product_id": {
                    "$like": self.pid
                }
            }
        }
        func.log(u'----开始查询宽表设备列表----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn(str(self.device_id), str(res))
            func.log(u'查询宽表设备列表响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_device_control(self):
        u'''设备控制'''
        _TestResult.des = u'MQTT连接服务'
        res = ''
        url = self.host + self.port + '/v2/diagnosis/device/set/' + str(self.device_id)
        body = {
            "datapoint": [
                {
                    "index": 0,
                    "value": true
                },
                {
                    "index": 1,
                    "value": 150
                }
            ]
        }
        func.log(u'----开始设备控制----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("200", str(res))
            func.log(u'设备控制响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_get_v_device(self):
        u'''获取虚拟设备'''
        _TestResult.des = u'MQTT连接服务'
        res = ''
        url = self.host + self.port + '/v2/product/' + self.pid + '/v_device/' + str(self.device_id)
        body = {}
        func.log(u'----开始获取虚拟设备----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.get(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn(str(self.device_id), str(res))
            func.log(u'获取虚拟设备响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_get_device_geography(self):
        u'''获取设备地理位置'''
        _TestResult.des = u'地理位置服务'
        res = ''
        url = self.host + self.port + '/v2/product/' + self.pid + '/device/' + str(self.device_id) + '/geography'
        body = {}
        func.log(u'----开始获取设备地理位置----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.get(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn(str(self.device_id), str(res))
            func.log(u'获取设备地理位置响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_upload_MCU(self):
        u'''上传固件版本'''
        _TestResult.des = u'固件升级服务'
        res1 = ''
        res2 = ''
        res3 = ''
        res4 = ''
        res5 = ''
        res6 = ''
        url_upload = self.host + self.port + '/v2/upload/product/' + self.pid + '/firmware'
        url = self.host + self.port + '/v2/product/' + self.pid + '/firmware'
        base_path = func.find_path()
        func.log(u'----开始上传固件版本1----')
        try:
            filename = base_path + '/V10051/1.png'
            fil1 = open(filename, 'rb').read()
            r1 = requests.post(url=url_upload, data=fil1, headers=api.headers)
            res1 = eval(r1.text)
            self.assertIn("url", res1)
            ApiTest.mcu1_url = res1["url"]
            ApiTest.mcu1_md5 = res1["md5"]
            ApiTest.mcu1_size = res1["size"]
            func.log(u'上传固件1响应：' + json.dumps(res1))
            body = {
                "mod": "1",
                "version": "1",
                "description": "mcu1",
                "type": 1,
                "identify": "",
                "file_url": self.mcu1_url,
                "file_md5": self.mcu1_md5,
                "file_size": self.mcu1_size,
                "is_release": true,
                "release_date": time.strftime("%Y-%m-%d") + "T01:36:06.173Z"
            }
            func.log('url：' + url)
            func.log('body：' + json.dumps(body))
            r2 = requests.post(url=url, json=body, headers=api.headers)
            res2 = eval(r2.text)
            self.assertIn("id", res2)
            func.log(u'上传固件版本1响应：' + json.dumps(res2))
        except Exception:
            func.log('[error_upload]:' + str(res1))
            func.log('[error_mcu]:' + str(res2))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass
        func.log(u'----开始上传固件版本2----')
        try:
            filename1 = base_path + '/V10052/1.png'
            fil2 = open(filename1, 'rb').read()
            r3 = requests.post(url=url_upload, data=fil2, headers=api.headers)
            res3 = eval(r3.text)
            self.assertIn("url", res3)
            ApiTest.mcu2_url = res3["url"]
            ApiTest.mcu2_md5 = res3["md5"]
            ApiTest.mcu2_size = res3["size"]
            func.log(u'上传固件2响应：' + json.dumps(res3))
            body = {
                "mod": "2",
                "version": "2",
                "description": "mcu2",
                "type": 1,
                "identify": "",
                "file_url": self.mcu2_url,
                "file_md5": self.mcu2_md5,
                "file_size": self.mcu2_size,
                "is_release": true,
                "release_date": time.strftime("%Y-%m-%d") + "T01:36:06.173Z"
            }
            func.log('url：' + url)
            func.log('body：' + json.dumps(body))
            r4 = requests.post(url=url, json=body, headers=api.headers)
            res4 = eval(r4.text)
            self.assertIn("id", res4)
            func.log(u'上传固件版本2响应：' + json.dumps(res4))
        except Exception:
            func.log('[error_upload]:' + str(res3))
            func.log('[error_mcu]:' + str(res4))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass
        func.log(u'----开始上传固件版本3----')
        try:
            filename1 = base_path + '/V10051/1.png'
            fil3 = open(filename1, 'rb').read()
            r5 = requests.post(url=url_upload, data=fil3, headers=api.headers)
            res5 = eval(r5.text)
            self.assertIn("url", res5)
            ApiTest.mcu3_url = res5["url"]
            ApiTest.mcu3_md5 = res5["md5"]
            ApiTest.mcu3_size = res5["size"]
            func.log(u'上传固件2响应：' + json.dumps(res5))
            body = {
                "mod": "3",
                "version": "3",
                "description": "mcu3",
                "type": 1,
                "identify": "",
                "file_url": self.mcu3_url,
                "file_md5": self.mcu3_md5,
                "file_size": self.mcu3_size,
                "is_release": true,
                "release_date": time.strftime("%Y-%m-%d") + "T01:36:06.173Z"
            }
            func.log('url：' + url)
            func.log('body：' + json.dumps(body))
            r6 = requests.post(url=url, json=body, headers=api.headers)
            res6 = eval(r6.text)
            self.assertIn("id", res6)
            func.log(u'上传固件版本3响应：' + json.dumps(res6))
        except Exception:
            func.log('[error_upload]:' + str(res5))
            func.log('[error_mcu]:' + str(res6))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_create_mcu_task(self):
        u'''创建升级任务'''
        _TestResult.des = u'固件升级服务'
        res = ''
        url = self.host + self.port + '/v2/upgrade/firmware/task'
        body = {
            "name": "task_auto",
            "description": "task_description",
            "type": 1,
            "identify": "",
            "product_id": self.pid,
            "from_version": 1,
            "from_version_url": self.mcu1_url,
            "from_version_md5": self.mcu1_md5,
            "from_version_size": self.mcu1_size,
            "target_version": 2,
            "target_version_url": self.mcu2_url,
            "target_version_md5": self.mcu2_md5,
            "target_version_size": self.mcu2_size,
            "task_type": 0,
            "scope": {
                "category": 0,
                "device_list": [

                ]
            }
        }
        func.log(u'----开始创建自动升级任务----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("id", str(res))
            ApiTest.mcu_task_id_auto = res["id"]
            func.log(u'创建自动升级任务响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass
        body1 = {
            "name": "task_manu",
            "description": "task_description",
            "type": 1,
            "identify": "",
            "product_id": self.pid,
            "from_version": 2,
            "from_version_url": self.mcu2_url,
            "from_version_md5": self.mcu2_md5,
            "from_version_size": self.mcu2_size,
            "target_version": 3,
            "target_version_url": self.mcu3_url,
            "target_version_md5": self.mcu3_md5,
            "target_version_size": self.mcu3_size,
            "task_type": 1,
            "scope": {
                "category": 0,
                "device_list": [

                ]
            }
        }
        func.log(u'----开始创建手动升级任务----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body1, headers=api.headers)
            res = eval(r.text)
            self.assertIn("id", str(res))
            ApiTest.mcu_task_id_manu = res["id"]
            func.log(u'创建手动升级任务响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_start_task(self):
        u'''启动任务'''
        _TestResult.des = u'固件升级服务'
        r = ''
        url = self.host + self.port + '/v2/upgrade/firmware/task/status'
        body = {
            "product_id": self.pid,
            "upgrade_task_id": self.mcu_task_id_auto,
            "status": 1
        }
        func.log(u'----开始启动自动升级任务----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            self.assertIn("200", str(r))
            func.log(u'启动自动升级任务成功')
        except Exception:
            res = eval(r.text)
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass
        body = {
            "product_id": self.pid,
            "upgrade_task_id": self.mcu_task_id_manu,
            "status": 1
        }
        func.log(u'----开始启动手动升级任务----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            self.assertIn("200", str(r))
            func.log(u'启动手动升级任务成功')
        except Exception:
            res = eval(r.text)
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_get_geographies(self):
        u'''获取地理位置信息列表'''
        _TestResult.des = u'地理位置服务'
        res = ''
        url = self.host + self.port + '/v2/service/position/geographies'
        body = {
            "param": "F001S006"
        }
        func.log(u'----开始获取地理位置信息列表----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("'count': 9", str(res))
            func.log(u'获取地理位置信息列表响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_check_user_active(self):
        """检查启动激活验证用户登录是否需要激活"""
        func.log(u'----开始检查启动激活验证用户登录是否需要激活----')
        res = ''
        api.set_corp_setting(self.host, self.port, true)
        url = self.host + self.port + '/v2/user_register'
        random_email = func.random_string()
        body = {
            "email": random_email+"@qq.com",
            "nickname": "nickname",
            "corp_id": self.corp_id,
            "password": self.user_password,
            "source": "2",
            "local_lang": "zh-cn"
        }
        func.log(u'用户通过邮箱注册')
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("email", str(res))
            func.log(u'用户通过邮箱注册响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass
        url = self.host + self.port + '/v2/user_auth'
        body = {
            "email": random_email+"@qq.com",
            "corp_id": self.corp_id,
            "password": self.user_password
        }
        func.log(u'用户通过邮箱登录')
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("account is not valid", str(res))
            func.log(u'用户通过邮箱登录响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_user_register_email(self):
        u'''用户通过邮箱注册'''
        api.set_corp_setting(self.host, self.port, false)
        _TestResult.des = u'API服务'
        res = ''
        url = self.host + self.port + '/v2/user_register'
        body = {
            "email": self.user_email,
            "nickname": "nickname",
            "corp_id": self.corp_id,
            "password": self.user_password,
            "source": "2",
            "local_lang": "zh-cn"
        }
        func.log(u'----开始用户通过邮箱注册----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("email", str(res))
            func.log(u'用户通过邮箱注册响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_user_register_phone_verifycode(self):
        u'''用户获取注册验证码'''
        _TestResult.des = u'API服务'
        r = ''
        url = self.host + self.port + '/v2/user_register/verifycode'
        body = {
            "corp_id": self.corp_id,
            "phone": self.user_phone,
            "captcha": ""
        }
        func.log(u'----开始获取注册验证码----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            self.assertIn("200", str(r))
            func.log(u'已发送验证码')
        except Exception:
            res = eval(r.text)
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_user_login(self):
        u'''用户通过邮箱登录'''
        _TestResult.des = u'API服务'
        res = ''
        url = self.host + self.port + '/v2/user_auth'
        body = {
            "email": self.user_email,
            "corp_id": self.corp_id,
            "password": self.user_password
        }
        func.log(u'----开始用户通过邮箱登录----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("user_id", str(res))
            ApiTest.user_headers["Access-Token"] = res["access_token"]
            ApiTest.user_id = res["user_id"]
            func.log(u'用户通过邮箱登录响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_echo_server(self):
        u'''检查echo第三方服务'''
        _TestResult.des = u'echo第三方服务'
        res = ''
        res1 = ''
        login_url = self.avs_host + self.avs_port + '/avs/v1/user/auth'
        token_url = self.avs_host + self.avs_port + '/avs/v1/alexa/token'
        login_body = {
            "email": self.user_email,
            "corp_id": self.corp_id,
            "password": self.user_password,
            "state": "",
            "redirect_uri": ""
        }
        func.log(u'----检查echo第三方服务----')
        func.log('login_url：' + login_url)
        func.log('login_body：' + json.dumps(login_body))
        try:
            r = requests.post(url=login_url, json=login_body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("redirect_uri", str(res))
            code = func.get_code(str(res))
            func.log(u'用户通过邮箱登录响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass
        token_body = "grant_type=authorization_code&code=" + code + "&client_id=1&client_secret=1&redirect_uri=https%3A%2F%2Flocalhost"
        func.log('token_url：' + token_url)
        func.log('token_body：' + token_body)
        try:
            r1 = requests.post(url=token_url, data=token_body, headers=api.headers)
            res1 = eval(r1.text)
            self.assertIn("access_token", str(res1))
            func.log(u'获取token响应：' + json.dumps(res1))
        except Exception:
            func.log('[error]:' + str(res1))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_google_home_server(self):
        u'''检查google_home第三方服务'''
        _TestResult.des = u'google_home第三方服务'
        res = ''
        res1 = ''
        code_url = self.google_home_host + self.google_home_port + '/gh/v1/auth'
        token_url = self.google_home_host + self.google_home_port + '/gh/v1/token'
        code_body = {
            "account": self.user_email,
            "corp_id": self.corp_id,
            "password": self.user_password,
            "client_id": "1",
            "redirect_uri": "",
            "state": "",
            "scope": "",
            "response_type": "code"
        }
        func.log(u'----检查google_home第三方服务----')
        func.log('code_url：' + code_url)
        func.log('login_body：' + json.dumps(code_body))
        try:
            r = requests.post(url=code_url, json=code_body, headers=api.headers)
            res = r.text
            self.assertIn("code", str(res))
            code = func.get_code_google_home(str(res))
            func.log(u'用户通过邮箱登录响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass
        token_body = "client_id=1&client_secret=1&grant_type=authorization_code&code=" + code
        func.log('token_url：' + token_url)
        func.log('token_body：' + token_body)
        try:
            r1 = requests.post(url=token_url, data=token_body, headers=api.headers)
            res1 = eval(r1.text)
            self.assertIn("access_token", str(res1))
            func.log(u'获取token响应：' + json.dumps(res1))
        except Exception:
            func.log('[error]:' + str(res1))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_aligenie_server(self):
        u'''检查天猫精灵第三方服务'''
        _TestResult.des = u'google_home第三方服务'
        res = ''
        res1 = ''
        client_id = '1'
        client_secret = '2'
        func.log(u'----检查天猫精灵第三方服务----')
        get_app_id_url = self.host + self.port + '/v2/plugin/apps'
        aligenie_id = api.get_apps_aligenie_id(get_app_id_url)
        config_aligenie_url = self.host + self.port + '/v2/plugin/app/' + aligenie_id
        api.set_aligenie_config(config_aligenie_url, client_id, client_secret)
        time.sleep(10)
        code_url = self.host + self.port + '/v2/aligenie/auth'
        token_url = self.host + self.port + '/v2/aligenie/token'
        code_body = {
            "corp_id": self.corp_id,
            "email": self.user_email,
            "password": self.user_password,
            "redirect_uri": "",
            "state": "",
            "client_id": client_id
        }
        func.log(u'开始用户通过邮箱登录获取code')
        func.log('code_url：' + code_url)
        func.log('login_body：' + json.dumps(code_body))
        try:
            r = requests.post(url=code_url, json=code_body, headers=api.headers)
            res = r.text
            self.assertIn("code", str(res))
            code = func.get_code(str(res))
            func.log(u'用户通过邮箱登录响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass
        token_body = "grant_type=authorization_code&client_id=" + client_id + "&client_secret=" + client_secret + "&code=" + code + "&redirect_uri=https%3A%2F%2Fopen.bot.tmall.com%2Foauth%2Fcallback"
        func.log(u'开始获取token')
        func.log('token_url：' + token_url)
        func.log('token_body：' + token_body)
        try:
            r1 = requests.post(url=token_url, data=token_body, headers=api.headers)
            res1 = eval(r1.text)
            self.assertIn("access_token", str(res1))
            func.log(u'获取token响应：' + json.dumps(res1))
        except Exception:
            func.log('[error]:' + str(res1))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_get_projects(self):
        """获取项目列表"""
        res = ''
        url = self.host + self.port + '/v2/realty-master-data/authorizations/projects?project_type=0'
        body = {
            "limit":10,
            "offset":0
        }
        func.log(u'----开始获取项目列表----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            self.assertIn('"status":200', r.text)
            func.log(u'获取项目列表响应：' + json.dumps(r.text))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_visitor_log_list(self):
        """获取开锁记录"""
        res = ''
        url = self.host + self.port + '/v2/smart-door/device-visitor-log/list'
        body = {

        }
        func.log(u'----开始获取开锁记录----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            self.assertIn('"status":200', r.text)
            func.log(u'获取项目列表响应：' + json.dumps(r.text))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_get_schedule_list(self):
        """获取排程列表"""
        res = ''
        url = self.host + self.port + '/v2/linkages/schedule-list'
        body = {
            "limit": 10,
            "offset": 0
        }
        func.log(u'----开始获取排程列表----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            self.assertIn('"status":200', r.text)
            func.log(u'获取排程列表响应：' + json.dumps(r.text))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_certificate(self):
        """网关授权添加证书"""
        res = ''
        url = self.host + self.port + '/v2/mqtt/certificate'
        body = {
            "name": "test_certificate",
            "expire_in": 0,
            "grant_type": 1,
            "product_ids": [
                self.pid
            ]
        }
        func.log(u'----开始网关授权添加证书----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("id", str(res))
            func.log(u'网关授权添加证书响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_data_platform(self):
        """数据平台添加仪表盘"""
        res = ''
        url = self.host + self.port + '/v2/data_platform/page'
        body = {
            "name": "data_platform",
            "page_type": 2,
            "auth_department": [

            ],
            "auth_position": [

            ],
            "auth_user": [

            ]
        }
        func.log(u'----开始数据平台添加仪表盘----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("id", str(res))
            func.log(u'数据平台添加仪表盘响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_work_order(self):
        """智能维保添加工单"""
        res = ''
        url = self.host + self.port + '/v2/work_order'
        body = {
            "type": "2",
            "title": "work_order",
            "link_man": "link_man",
            "link_phone": "13555555555",
            "link_address": "link_address",
            "is_notice": false,
            "extends": {
                "isDealer": false
            },
            "event_logs": [
                {
                    "type": 1,
                    "description": "description"
                }
            ],
            "link_country": "F001",
            "link_province": "F001S001",
            "link_city": "F001S001T0001"
        }
        func.log(u'----开始智能维保添加工单----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("_id", str(res))
            func.log(u'智能维保添加工单响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_maintenance_task(self):
        """智能维保添加巡检任务"""
        res = ''
        url = self.host + self.port + '/v2/service/maintenance/strategy_task'
        body = {
            "checkUser": u"系统",
            "circleMode": 1,
            "name": "name",
            "neverFail": 1,
            "runTime": "00:00:00",
            "status": 2,
            "type": 4,
            "productList": [
                self.pid
            ]
        }
        func.log(u'----开始智能维保添加巡检任务----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("OK", str(res))
            func.log(u'智能维保添加巡检任务响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_check_device_summary(self):
        """检查设备管理的设备数统计"""
        func.log(u'----开始检查设备管理的设备数统计----')
        new_devices_summary = []
        total, online, offline, exception = api.get_device_summary(self.host, self.port)
        new_devices_summary.append(total - 1)
        new_devices_summary.append(online - 1)
        new_devices_summary.append(offline)
        new_devices_summary.append(exception - 1)
        try:
            self.assertEqual(ApiTest.devices_summary, new_devices_summary)
        except Exception:
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_check_alarm_summary(self):
        """检查报警数据统计"""
        func.log(u'----开始检查报警数据统计----')
        new_alarm_summary = []
        alarms, exceptions, today_alarms, condition_alarms = api.get_alarm_summary(self.host, self.port)
        new_alarm_summary.append(alarms - 1)
        new_alarm_summary.append(exceptions - 1)
        new_alarm_summary.append(today_alarms - 1)
        new_alarm_summary.append(condition_alarms - 1)
        try:
            self.assertEqual(ApiTest.alarm_summary, new_alarm_summary)
        except Exception:
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_check_map_summary(self):
        """检查地图设备数据统计"""
        func.log(u'----开始检查地图设备数据统计----')
        new_map_summary = []
        total, online, exception = api.get_map_summary(self.host, self.port)
        new_map_summary.append(total - 1)
        new_map_summary.append(online - 1)
        new_map_summary.append(exception - 1)
        try:
            self.assertEqual(ApiTest.map_summary, new_map_summary)
        except Exception:
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_user_forgot_password(self):
        """用户通过邮件找回密码"""
        url = self.host + self.port + '/v2/user/password/forgot'
        body = {
             "corp_id":self.corp_id,
             "email":self.user_email
        }
        func.log(u'----开始用户通过邮件找回密码----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            requests.post(url=url, json=body, headers=api.headers)
            func.log(u'用户通过邮件找回密码响应成功')
        except Exception:
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            time.sleep(5)
            pass

    def test_get_qrcode(self):
        u'''生成设备二维码'''
        _TestResult.des = u'管理台基础功能服务'
        res = ''
        url = self.host + self.port + '/v2/product/' + self.pid + '/device/' + str(self.device_id) + '/qrcode'
        body = {
            "authority": "RW",
            "custom_field": [
                "id",
                "mac",
                "pid",
                "sn"
            ],
            "format": {
                "prefix": "",
                "suffix": "",
                "encode": "source"
            }
        }
        func.log(u'----开始生成设备二维码----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("qrcode", str(res))
            ApiTest.qrcode = res["qrcode"]
            func.log(u'生成设备二维码响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_set_data_point_value(self):
        u'''串口上报数据端点'''
        _TestResult.des = u'MQTT连接服务'
        try:
            func.log(u'----开始调串口上报数据----')
            # ser.find_serial2('COM3')
            ser.mcu_wifi()
            time.sleep(120)
        except Exception:
            func.log(u'【串口上报数据失败】')
            raise
        finally:
            pass

    def test_get_alarm_list(self):
        u'''获取告警记录'''
        _TestResult.des = u'告警服务'
        res = ''
        url = self.host + self.port + '/v2/corp/alarm/states'
        body = {
            "filter": [
                "id",
                "device_id",
                "rule_id",
                "status",
                "content",
                "count"
            ],
            "order": {
                "start_time": "desc"
            },
            "query": {
                "scope": {
                    "$in": [
                        1,
                        3,
                        4
                    ]
                },
                "product_id": {
                    "$in": [
                        self.pid
                    ]
                },
                "device_id": {
                    "$eq": self.device_id
                }
            },
            "limit": 10,
            "offset": 0
        }
        func.log(u'----开始获取告警记录----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn(str(self.device_id), str(res))
            func.log(u'获取告警记录响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_get_qrcode_subscribe(self):
        u'''用户通过二维码订阅设备'''
        _TestResult.des = u'API服务'
        res = ''
        url = self.host + self.port + '/v2/user/' + str(self.user_id) + '/qrcode_subscribe'
        body = {
            "qrcode": self.qrcode
        }
        func.log(u'----开始订阅设备----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=self.user_headers)
            res = eval(r.text)
            self.assertIn(str(self.device_id), str(res))
            func.log(u'订阅设备响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_user_get_device_list(self):
        u'''用户获取设备列表'''
        _TestResult.des = u'虚拟设备服务'
        res = ''
        url = self.host + self.port + '/v2/user/' + str(self.user_id) + '/subscribe/devices'
        body = {
        }
        func.log(u'----开始获取设备列表----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.get(url=url, json=body, headers=self.user_headers)
            res = eval(r.text)
            self.assertIn(str(self.device_id), str(res))
            func.log(u'获取设备列表响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_create_app(self):
        u'''配置app'''
        _TestResult.des = u'管理台基础功能服务'
        res = ''
        url = self.host + self.port + '/v2/plugin/app'
        api.get_help_app(self.host, self.port)
        body = {
            "name": "feedback",
            "type": 10,
            "plugin": "helpdesk",
            "enable": true
        }
        func.log(u'----开始配置app----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            self.assertIn("id", str(res))
            ApiTest.app_id = res["id"]
            func.log(u'配置app响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_feedback(self):
        u'''新增用户反馈'''
        _TestResult.des = u'用户反馈服务'
        res = ''
        url = self.host + self.port + '/v2/module/feedback/' + str(self.app_id) + '/api/feedback/save'
        body = {
            "user_id": self.user_id,
            "user_name": "小明",
            "phone": "1689624223",
            "email": "xiaoming@qq.com",
            "content": u"电饭煲无法启用"
        }
        func.log(u'----开始新增用户反馈----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=self.user_headers)
            res = eval(r.text)
            self.assertIn("id", str(res))
            func.log(u'新增用户反馈响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def check_receive_new_email(self):
        u'''检查是否收到测试邮件'''
        _TestResult.des = u'邮件服务'
        func.log(u'----开始是否收到测试邮件----')
        num = func.get_email_unseen(self.user_email, self.user_password)
        try:
            if int(num) > 0:
                self.assertTrue(True)
                func.log(u'已收到测试邮件')
            else:
                self.assertTrue(False)
        except Exception:
            func.log(u'未收到测试邮件')
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))

    def check_auto_update_firmware_version(self):
        u'''检查自动升级是否成功'''
        _TestResult.des = u'固件升级服务'
        res = ''
        url = self.host + self.port + '/v2/product/' + self.pid + '/device/' + str(self.device_id)
        body = {
        }
        func.log(u'----开始检查自动升级是否成功----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.get(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            version = str(res["firmware_version"])
            self.assertEqual(version, '2')
            func.log(u'设备信息响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_upgrade_by_manual(self):
        u'''设备手动升级'''
        _TestResult.des = u'固件升级服务'
        r = ''
        r1 = ''
        url = self.host + self.port + '/v2/upgrade/device'
        url1 = self.host + self.port + '/v2/upgrade/firmware/task/status'
        body = {
            "product_id": self.pid,
            "device_id": self.device_id
        }
        body1 = {
            "product_id": self.pid,
            "upgrade_task_id": self.mcu_task_id_auto,
            "status": 0
        }
        func.log(u'----开始关闭自动升级任务----')
        func.log('url：' + url1)
        func.log('body：' + json.dumps(body1))
        try:
            r1 = requests.post(url=url1, json=body1, headers=api.headers)
            self.assertIn("200", str(r1))
            func.log(u'自动升级任务已关闭')
        except Exception:
            res = eval(r1.text)
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass
        func.log(u'----开始设备手动升级----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.post(url=url, json=body, headers=self.user_headers)
            self.assertIn("200", str(r))
            func.log(u'已设备手动升级')
            time.sleep(120)
        except Exception:
            res = eval(r.text)
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def check_manual_update_firmware_version(self):
        u'''检查手动升级是否成功'''
        _TestResult.des = u'固件升级服务'
        res = ''
        url = self.host + self.port + '/v2/product/' + self.pid + '/device/' + str(self.device_id)
        body = {
        }
        func.log(u'----开始检查手动升级是否成功----')
        func.log('url：' + url)
        func.log('body：' + json.dumps(body))
        try:
            r = requests.get(url=url, json=body, headers=api.headers)
            res = eval(r.text)
            version = str(res["firmware_version"])
            self.assertEqual(version, '1')
            func.log(u'设备信息响应：' + json.dumps(res))
        except Exception:
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass

    def test_clear_data(self):
        u'''清理测试数据'''
        _TestResult.des = u'清除数据'
        r = ''
        url1 = self.host + self.port + '/v2/user/' + str(self.user_id)
        url2 = self.host + self.port + '/v2/product/' + str(self.pid)
        url3 = self.host + self.port + '/v2/plugin/app/' + str(self.app_id)
        url4 = self.host + self.port + '/v2/corp/member/' + str(self.mem_id)
        body = {
        }
        # func.log(u'----开始删除用户----')
        # func.log('url：' + url1)
        # try:
        #     r = requests.delete(url=url1, json=body, headers=api.headers)
        #     func.log(u'已删除用户')
        # except Exception:
        #     res = eval(r.text)
        #     func.log('[error]:' + str(res))
        #     func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
        #     raise
        # finally:
        #     pass
        # func.log(u'----开始删除产品----')
        # func.log('url：' + url2)
        # try:
        #     r = requests.delete(url=url2, json=body, headers=api.headers)
        #     func.log(u'已删除产品')
        # except Exception:
        #     res = eval(r.text)
        #     func.log('[error]:' + str(res))
        #     func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
        #     raise
        # finally:
        #     pass
        func.log(u'----开始删除app配置----')
        func.log('url：' + url3)
        try:
            r = requests.delete(url=url3, json=body, headers=api.headers)
            func.log(u'已删app配置')
        except Exception:
            res = eval(r.text)
            func.log('[error]:' + str(res))
            func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            raise
        finally:
            pass
            # func.log(u'----开始删除成员----')
            # func.log('url：' + url4)
            # try:
            #     r = requests.delete(url=url4, json=body, headers=api.headers)
            #     func.log(u'已删除成员')
            # except Exception:
            #     res = eval(r.text)
            #     func.log('[error]:' + str(res))
            #     func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
            #     raise
            # finally:
            pass


if __name__ == '__main__':
    base_path = func.find_path()
    now = time.strftime("%Y-%m-%d.%H.%M.%S")
    filename = base_path + '/report/' + now + 'result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp, title='deployment_api_test', description='base_api_test_of_services')
    suite = unittest.TestSuite()
    # runner = unittest.TextTestRunner()
    # suite.addTest(ApiTest('test_init_device'))  # 重置设备
    # suite.addTest(ApiTest('start_email_listen'))  # 启动邮件监听线程，接收激活和密码修改邮件，并打开连接操作
    # suite.addTest(ApiTest('test_member_forgot_password'))  # 企业成员找回密码
    suite.addTest(ApiTest('test_member_login'))  # 成员登录
    # suite.addTest(ApiTest('test_add_member'))  # 添加成员
    # suite.addTest(ApiTest('test_create_product'))  # 创建产品
    # suite.addTest(ApiTest('test_add_data_point_sys'))  # 添加$1002数据端点
    # suite.addTest(ApiTest('test_add_data_point_custom'))  # 添加自定义数据端点
    # suite.addTest(ApiTest('test_register_device'))  # 注册设备
    # suite.addTest(ApiTest('test_alter_rule'))  # 添加异常设置
    # suite.addTest(ApiTest('test_alarm_setting'))  # 添加报警设置
    # suite.addTest(ApiTest('test_snapshot'))  # 添加快照规则
    # suite.addTest(ApiTest('test_statistic_rule'))  # 添加快照
    # suite.addTest(ApiTest('test_set_task'))  # 添加定时任务
    # suite.addTest(ApiTest('test_upload_MCU'))  # 创建固件版本
    # suite.addTest(ApiTest('test_create_mcu_task'))  # 创建升级任务
    # suite.addTest(ApiTest('test_start_task'))  # 启动升级任务
    # suite.addTest(ApiTest('test_active_device'))  # 串口激活设备
    # suite.addTest(ApiTest('test_wide_devices'))  # 获取宽表设备列表
    # suite.addTest(ApiTest('test_device_control'))  # 设备控制
    # suite.addTest(ApiTest('test_get_v_device'))  # 获取虚拟设备列表
    # suite.addTest(ApiTest('test_get_device_geography'))  # 获取设备地理位置
    # suite.addTest(ApiTest('test_get_geographies'))  # 获取位置列表
    # suite.addTest(ApiTest('test_check_user_active'))  # 检查启动激活验证后新注册用户是否需要激活
    # suite.addTest(ApiTest('test_user_register_email'))  # 用户通过邮箱注册账号
    # suite.addTest(ApiTest('test_set_data_point_value'))  # 串口上报数据端点
    # suite.addTest(ApiTest('test_get_alarm_list'))  # 获取告警记录
    # suite.addTest(ApiTest('test_user_register_phone_verifycode'))  # 用户获取注册短信验证码
    # suite.addTest(ApiTest('test_user_login'))  # 用户登录
    # suite.addTest(ApiTest('test_echo_server'))  # avs获取用户token
    # suite.addTest(ApiTest('test_google_home_server'))  # google_home获取用户token
    # suite.addTest(ApiTest('test_aligenie_server'))  # google_home获取用户token
    suite.addTest(ApiTest('test_get_projects'))  # 获取项目列表
    # suite.addTest(ApiTest('test_visitor_log_list'))  # 获取开锁记录
    # suite.addTest(ApiTest('test_get_schedule_list'))  # 获取排程列表
    # suite.addTest(ApiTest('test_certificate'))  # 网关授权添加证书
    # suite.addTest(ApiTest('test_data_platform'))  # 数据平台添加仪表盘
    # suite.addTest(ApiTest('test_work_order'))  # 智能维保添加工单
    # suite.addTest(ApiTest('test_maintenance_task'))  # 智能维保添加巡检任务
    # suite.addTest(ApiTest('test_check_device_summary'))  # 检查设备数量统计
    # suite.addTest(ApiTest('test_check_alarm_summary'))  # 检查报警数量统计是
    # suite.addTest(ApiTest('test_check_map_summary'))  # 检查地图设备数量统计
    # suite.addTest(ApiTest('test_user_forgot_password'))  # 用户找回密码
    # suite.addTest(ApiTest('test_create_app'))  # 配置app
    # suite.addTest(ApiTest('test_feedback'))  # 添加用户反馈
    # suite.addTest(ApiTest('test_get_qrcode'))  # 生成设备二维码
    # suite.addTest(ApiTest('test_get_qrcode_subscribe'))  # 通过二维码订阅设备
    # suite.addTest(ApiTest('test_user_get_device_list'))  # 用户获取设备列表
    # suite.addTest(ApiTest('check_auto_upda te_firmware_version'))  # 检查自动升级是否成功
    # suite.addTest(ApiTest('test_upgrade_by_manual'))  # 用户手动升级设备
    # suite.addTest(ApiTest('test_clear_data'))  # 清理测试数据
    # suite.addTest(ApiTest('test_init_device2'))  # 重置设备
    # suite.addTest(ApiTest('test_active_device2'))  # 串口激活设备
    # suite.addTest(ApiTest('check_manual_update_firmware_version'))  # 检查手动升级是否成功
    runner.run(suite)
    # fp.close()
    # file_path = func.new_report(base_path + '/report/')
    # try:
    #     func.send_mail(file_path)
    # except Exception, msg:
    #     func.log(u'结果邮件发送失败')
    #     raise
