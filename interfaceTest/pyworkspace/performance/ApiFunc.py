# coding=utf-8
import requests
import openpyxl
import random
import json
import traceback
import Function as func
import operator
import time
import os

headers = {"Content-Type": "application/json", "Access-Token": "token_value"}
headers2 = {"Content-Type": "application/x-www-form-urlencoded", "Access-Token": "token_value"}
headers_user = {"Content-Type": "application/json", "Access-Token": "token_value"}
global false, true
false = False
true = True


def get_access_token(host, port, member, mem_password):
    func.log(u'开始获取token')
    login_body = {"account": member, "password": mem_password}
    url = host + port + '/v2/corp_auth'
    try:
        r = requests.post(url=url, json=login_body, headers=headers)
        res = eval(r.text)
        func.log('token:'+res['access_token'])
        modify_dict(headers, "Access-Token", res['access_token'])
        modify_dict(headers2, "Access-Token", res['access_token'])
        return res["corp_id"]
    except Exception:
        func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
        raise


def modify_dict(str_dict, key, value):
    str_dict[key] = value
    return str_dict


def create_product(host, port):
    u'''创建产品'''
    res = ''
    url = host + port + '/v2/product'
    body = {"name": "performance_product_"+time.strftime("%Y-%m-%d"), "link_type": 1, "description": "", "is_gateway_device": False}
    func.log(u'-----开始创建产品接口-----')
    func.log('url:' + url)
    func.log('body:' + json.dumps(body))
    try:
        r = requests.post(url=url, json=body, headers=headers)
        res = eval(r.text)
        func.log(u'创建产品接口响应:' + json.dumps(res))
        return res["id"], res["key"]
    except Exception:
        func.log('[error]:' + str(res))
        func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
        raise
    finally:
        pass


def import_devices(host, port, pid, count):
    u'''批量导入设备'''
    device_list = []
    res = ''
    device = {"mac":"mac","name":"name","sn":"sn"}
    seed = "1234567890ABCDEF"
    for i in range(count):
        sa = []
        for j in range(12):
            sa.append(random.choice(seed))
        mac = ''.join(sa)
        name = 'name'+str(mac)
        sn = 'sn'+str(mac)
        modify_dict(device, "mac", mac)
        modify_dict(device, "name", name)
        modify_dict(device, "sn", sn)
        device_list.append(eval(str(device)))
    url = host + port + '/v2/product/'+pid+'/device_import_batch'
    body = json.dumps(device_list)
    # func.log('url:' + url)
    # func.log('body:' + body)
    # func.log('header:' + json.dumps(headers2))
    try:
        r = requests.post(url=url, data=body, headers=headers2)
        res = eval(r.text)
        func.log(u'导入设备接成功')
    except Exception:
        func.log('[error]:' + str(res))
        func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
        raise
    finally:
        pass


def add_data_point_custom(host, port, pid):
    u'''添加数据端点int'''
    res = ''
    url = host + port + '/v2/product/'+str(pid)+'/datapoint'
    body = {
        "name":"porintid",
        "type":3,
        "index":0,
        "description":"descriptions",
        "symbol":"unit",
        "source":1,
        "is_read":true,
        "is_write":1,
        "min":0,
        "max":100
    }
    func.log(u'----开始创建自定义数据端点----')
    func.log('url:' + url)
    func.log('body:' + json.dumps(body))
    try:
        r = requests.post(url=url, json=body, headers=headers)
        res = eval(r.text)
        func.log(u'创建自定义数据端点响应:' + json.dumps(res))
        index_custom = res["index"]
        point_id_custom = res["id"]
        return index_custom, point_id_custom
    except Exception:
        func.log('[error]:' + str(res))
        func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
        raise
    finally:
        pass


def alter_rule_new(host, port, pid, point_id_custom):
    u'''设置异常规则'''
    res = ''
    url = host + port + '/v2/alert/rule'
    url_get_list = host + port + '/v2/exception/tags'
    r1 = requests.get(url=url_get_list, json={}, headers=headers)
    res1 = eval(r1.text)
    tag_id = res1["list"][2]["id"]
    body = {
        "name":"test_exception",
        "deviceOnline":"online",
        "content":"value>100",
        "product_id":pid,
        "tag":"",
        "scope":4,
        "source":1,
        "is_enable":true,
        "notify_type":2,
        "notify_target":[

        ],
        "notify_apps":[

        ],
        "exception": {
            "tag_id": tag_id,
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
        "param":point_id_custom,
        "type":1,
        "compare":5,
        "value":"100"
    }
    func.log(u'----开始设置异常规则----')
    func.log('url:' + url)
    func.log('body:' + json.dumps(body))
    try:
        r = requests.post(url=url, json=body, headers=headers)
        res = eval(r.text)
        exception_id = res["id"]
        func.log(u'设置异常规则响应:' + json.dumps(res))
        return exception_id, tag_id
    except Exception:
        func.log('[error]:' + str(res))
        func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
        raise
    finally:
        pass


def alarm_setting_new(host, port, pid, point_id_custom, exception_id, tag_id):
    u'''添加报警设置'''
    res = ''
    url = host + port + '/v2/alert/rule/' + str(exception_id)
    body = {
        "exception":{
            "tag_id":tag_id,
            "suggestions":""
        },
        "compare":5,
        "is_enable":true,
        "source":1,
        "type":1,
        "version":1,
        "content":"",
        "notify_type":2,
        "notify_apps":[

        ],
        "notification":{
            "is_enable":true,
            "scope":{
                "member":{
                    "is_all":true,
                    "member_ids":[

                    ],
                    "department_ids":[

                    ],
                    "position_ids":[

                    ]
                }
            },
            "conditions":{
                "times":1
            }
        },
        "notify_target":[
            2
        ],
        "param":point_id_custom,
        "product_id":pid,
        "scope":1,
        "name":"test_exception",
        "interval":0,
        "id":exception_id,
        "tag":"",
        "value":"100"
    }
    func.log(u'----开始报警设置----')
    func.log('url:' + url)
    func.log('body:' + json.dumps(body))
    try:
        r = requests.put(url=url, json=body, headers=headers)
        res = eval(r.text)
        func.log(u'报警设置响应:' + json.dumps(res))
    except Exception:
        func.log('[error]:' + str(res))
        func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
        raise
    finally:
        pass


def alarm_setting_old(host, port, pid, point_id_custom):
    u'''添加告警设置'''
    res = ''
    url = host + port + '/v2/alert/rule'
    url_get_list = host + port + '/v2/alert_tag'
    r1 = requests.get(url=url_get_list, json={}, headers=headers)
    res1 = eval(r1.text)
    tag_id = res1["tags"][0]
    body = {
        "product_id":str(pid),
        "name":"name",
        "content":"neirong",
        "type":1,
        "notify_type":1,
        "notify_apps":[

        ],
        "notify_target":[
            3
        ],
        "is_enable":1,
        "param":str(point_id_custom),
        "compare":5,
        "value":"100",
        "scope":1,
        "tag":str(tag_id),
        "xlink_wechat_template":""
    }
    func.log(u'----开始告警设置----')
    func.log('url:' + url)
    func.log('body:' + json.dumps(body))
    try:
        r = requests.post(url=url, json=body, headers=headers)
        res = eval(r.text)
        func.log(u'设置异常规则响应:' + json.dumps(res))
    except Exception:
        func.log('[error]:' + str(res))
        func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
        raise
    finally:
        pass


def user_subscribe_device(host, port, pid, corp_id, user_email, user_password):
    u'''用户订阅设备'''
    res = ''
    user_id = ''
    url_p_set = host + port + '/v2/product/'+pid
    url_user_register = host + port + '/v2/user_register'
    url_user_login = host + port + '/v2/user_auth'
    body_p_set = {
            "create_time": "2018-09-04T17:41:30.888Z",
            "visibility": 1,
            "is_active_register": false,
            "description": "",
            "is_registerable": true,
            "type": 0,
            "link_type": 1,
            "mode": "A",
            "extend": {
            },
            "is_allow_multi_admin": false,
            "is_gateway_device": false,
            "scan_mode": 1,
            "quota": 100000000,
            "name": u"性能测试自动化",
            "id": pid,
            "categories": [
            ],
            "is_release": false,
            "pics": [
                ""
            ]
        }
    func.log(u'----开始设置产品允许用户自行授权----')
    func.log('url:' + url_p_set)
    func.log('body:' + json.dumps(body_p_set))
    try:
        requests.put(url=url_p_set, json=body_p_set, headers=headers)
        func.log(u'已设置产品允许用户自行授权')
    except Exception:
        func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
        raise
    finally:
        pass
    body_user_register = {
        "email":user_email,
        "nickname":"nickname",
        "corp_id":corp_id,
        "password":user_password,
        "source":"2",
        "local_lang":"zh-cn"
    }
    func.log(u'----开始注册用户----')
    func.log('url:' + url_user_register)
    func.log('body:' + json.dumps(body_user_register))
    try:
        r = requests.post(url=url_user_register, json=body_user_register, headers=headers)
        res = eval(r.text)
        func.log(u'设置异常规则响应:' + json.dumps(res))
    except Exception:
        func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
        raise
    finally:
        pass
    body_user_login = {
        "email": user_email,
        "corp_id": corp_id,
        "password": user_password
    }
    func.log(u'----获取用户id----')
    func.log('url:' + url_user_login)
    func.log('body:' + json.dumps(body_user_login))
    try:
        r = requests.post(url=url_user_login, json=body_user_login, headers=headers)
        res = eval(r.text)
        func.log(u'设置异常规则响应:' + json.dumps(res))
        user_id = res["user_id"]
        user_token = res['access_token']
        modify_dict(headers_user, "Access-Token", res['access_token'])
    except Exception:
        func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
        raise
    finally:
        pass
    url_user_register_device = host + port + '/v2/user/' + str(user_id) + '/register_device'
    body_user_register_device = {
        "product_id":pid,
        "mac":func.random_mac()
    }
    func.log(u'----开始用户注册设备----')
    func.log('url:' + url_user_register_device)
    func.log('body:' + json.dumps(body_user_register_device))
    try:
        r = requests.post(url=url_user_register_device, json=body_user_register_device, headers=headers_user)
        res = eval(r.text)
        func.log(u'用户注册设备响应:' + json.dumps(res))
        return res["device_id"], user_id, user_token
    except Exception:
        func.log('[error]:' + str(res))
        func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
        raise
    finally:
        pass

def get_access_key(host, port):
    u'''添加accesskey'''
    res = ''
    url = host + port + '/v2/accesskey'
    body = {
        "name": "access_key"
    }
    func.log(u'----开始添加accesskey----')
    func.log('url:' + url)
    func.log('body:' + json.dumps(body))
    try:
        r = requests.post(url=url, json=body, headers=headers)
        res = eval(r.text)
        func.log(u'添加accesskey响应:' + json.dumps(res))
        return res["id"], res["secret"]
    except Exception:
        func.log('[error]:' + str(res))
        func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
        raise
    finally:
        pass

def set_device_property(host, port, pid, device_id):
    u'''设置设备扩展属性'''
    res = ''
    url = host + port + '/v2/product/'+str(pid)+'/device/'+str(device_id)+'/property'
    body = {
        "name": "value"
    }
    func.log(u'----开始设置设备扩展属性----')
    func.log('url:' + url)
    func.log('body:' + json.dumps(body))
    try:
        r = requests.post(url=url, json=body, headers=headers_user)
        res = eval(r.text)
        func.log(u'设置设备扩展属性响应:' + json.dumps(res))
    except Exception:
        func.log('[error]:' + str(res))
        func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
        raise
    finally:
        pass

def write_login_body_to_txt(corp_id, email, password, path):
    u'''用户登录请求体写入文件'''
    body = {
        "corp_id": corp_id,
        "email": email,
        "password": password,
        "resource": "1"
    }
    if not os.path.exists('C:/mqtt-client/'):
        os.mkdir('C:/mqtt-client/')
    if not os.path.exists(path):
        fobj = open(path, 'w')
        fobj.close()
    f = open(path, 'w')
    f.write(json.dumps(body))
    f.close()
    func.log(u'登录body写入本地postdata.txt成功')

def get_msg_by_ab_result(filename, result):
    u'''ab命令结果写入本地log'''
    msg = []
    path = 'C:/mqtt-client/'+filename+'.txt'
    if not os.path.exists(path):
        fobj = open(path, 'w')
        fobj.close()
    f = open(path, 'w')
    f.write(result)
    f.close()
    f1 = open(path, 'r')
    for line in f1.readlines():
        if line.find('Time taken for tests') >= 0:
            s = line.find(':')
            e = len(line)
            r = line[s+1:e]
            ''.join(r.split())
            msg.append(r)
        elif line.find('Requests per second') >= 0:
            s = line.find(':')
            e = len(line)
            r = line[s + 1:e]
            ''.join(r.split())
            msg.append(r)
        elif line.find('Time per request') >= 0:
            s = line.find(':')
            e = len(line)
            r = line[s + 1:e]
            ''.join(r.split())
            msg.append(r)
        elif line.find('Transfer rate') >= 0:
            s = line.find(':')
            e = len(line)
            r = line[s + 1:e]
            ''.join(r.split())
            msg.append(r)
    f1.close()
    if len(msg) == 0:
        msg = [u'无数据', u'无数据', u'无数据', u'无数据']
    return msg

def get_msg_by_cm_result(filename, result, num):
    u'''ab命令结果写入本地log'''
    msg = ['','','','','']
    a = 0
    path = 'C:/mqtt-client/'+filename+'_'+num+'.txt'
    if not os.path.exists(path):
        fobj = open(path, 'w')
        fobj.close()
    f = open(path, 'w')
    f.write(result)
    f.close()
    f1 = open(path, 'r')
    for line in f1.readlines():
        if line.find('CONNECT') >= 0:
            s = line.find('CONNECT')
            e = len(line)
            r = line[s + 7:e]
            ''.join(r.split())
            msg[0] = r
            a = 1
        elif line.find('PING') >= 0:
            s = line.find('PING')
            e = len(line)
            r = line[s + 4:e]
            ''.join(r.split())
            msg[1] = r
            a = 1
        elif line.find('DEVICE_ONLINE') >= 0:
            s = line.find('DEVICE_ONLINE')
            e = len(line)
            r = line[s + 13:e]
            ''.join(r.split())
            msg[2] = r
            a = 1
        elif line.find('DEVICE_SYNC') >= 0:
            s = line.find('DEVICE_SYNC')
            e = len(line)
            r = line[s + 11:e]
            ''.join(r.split())
            msg[3] = r
            a = 1
        elif line.find('FAILURE') >= 0:
            msg[4] = 'failure'
            a = 1
    if a == 0:
        msg[4] = u'发生异常，请查看C:\mqtt-client下的输入日志'
    f1.close()
    return msg