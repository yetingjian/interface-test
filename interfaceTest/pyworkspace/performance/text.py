# coding=utf-8
import openpyxl
import os

from datetime import datetime, date, timedelta
import time

import ExcelFunc
import PerformanceFunc as pf
import ApiFunc as af
import requests
import openpyxl
import random
import json

def get_access_token(host, port, member, mem_password):
    login_body = {"account": member, "password": mem_password}
    url = host + port + '/v2/corp_auth'
    try:
        r = requests.post(url=url, json=login_body, headers=headers)
        res = eval(r.text)
        modify_dict(headers, "Access-Token", res['access_token'])
        return res["corp_id"]
    except Exception:
        raise

def test_xj(host, port):
    login_body = {
        "objectType":2,
        "projectList":[
            {
                "prjId":"9547a08630b1e0b9f003194b38743df0",
                "productList":[
                    "1607d2b54bd700011607d2b54bd7be0d",
                    "1607d2b5564800011607d2b556482801"
                ]
            }
        ]
    }
    url = host + port + '/v2/service/maintenance/inspection'
    try:
        r = requests.post(url=url, json=login_body, headers=headers)
        res = eval(r.text)
        print res["status"]
    except Exception:
        raise

def modify_dict(str_dict, key, value):
    str_dict[key] = value
    return str_dict

if __name__ == '__main__':
    print int(time.time())