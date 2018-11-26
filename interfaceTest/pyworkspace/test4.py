# coding=utf-8
import requests
import random
import xlrd

def get_access_token():
    login_url = 'http://iotapitest.bgycc.com/v2/corp_auth'
    headers = {"Content-Type": "application/json"}
    login_body = {"account": "wq@xlink.cn", "password": "Test1234"}

    r = requests.post(url=login_url, json=login_body, headers=headers)
    print(r.text)
    res = vars(r.text)
    print(res['access_token'])
    return res['access_token']

def test_qualification_add1():
    # data2 = excel_table_byindex("C:\\Users\\Demon\\Desktop\\test.xlsx", 0)
    # if (len(data2) <= 0):
    #     assert 0, u"Excel数据异常"
    # time.sleep(5)
    # print data2.sheets()
    # url = data2.sheet_by_index(0)  # 测试的接口url
    url = "http://iotapitest.bgycc.com/v2/service/iot/get_data?service=air_and_exhaust&object=exhaust_fan&id=5"  # 测试的接口url
    #headers3 = str(data2[0][u'headers1'])       #转字符串
    headers = eval('{"Content-Type": "application/json","Access-Token": "MjRBQTRCMEEyMEJFQ0RFNTY5QTM0RTVDRDlDQURCMUY4RjQ4RTM3QTVDRDkzNzAxQzI0MjM0OTQ0NjMzOEUwMQ=="}') #转为dict类型
    # headers = json.dumps(data2[0][u'headers1'])
    # headers = json.loads(headers)
    # data = # 接口传送的参数
    #data3 = str(data2[0][u'data1'])
    data = eval('{"product_id":"1607d2b3c03400011607d2b3c0345601","offset":0,"limit":10}')
    print (type(url))
    print (type(headers))
    print (type(data))
    print (url)
    print (headers)
    print (data)
    # print "url is : " + str(url)
    # print "headers is : " + str(headers)
    # print "data is :" + str(data)
    r = requests.get(url=url, json=data, headers=headers)  # 发送请求
    # result = r.json
    print (r.text)  # 获取响应报文
    res = eval(r.text)
    print (res["mode"])
    print (res["mode"] == '1')
    print (r.status_code)
    a = random.uniform(1,2)
    b = random.randint(1,100)
    print(b)
    print(a)
    print (type(a))
    print (round(a,2))


if __name__ == '__main__':
    get_access_token()