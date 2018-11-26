import json

import xlrd,os
import unittest
from ddt import data, ddt
from time import sleep


from xlinkutils import Xlink_Utils
from xlinkutils.Xlink_Utils import get_datapoints_list, load_data_points, get_user_list
import time
global false, true
false = False
true = True

def excel_table_byindex(file, start, end):
    data = open_excel(file)
    table = data.sheets()[0]
    list = []
    colnames = table.row_values(0)
    for i in range(start-1, end):
        row = table.row_values(i)
        app = {}
        for i in range(1,5):
            app[colnames[i]] = row[i]
        list.append(app)
    return list

def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print (str(e))



@ddt
class test_suite(unittest.TestCase):
    global test_info

    # 这里可以修改和添加test_info变量的内容和属性

    test_info = []

    for i in range(5):
        test_info.append(i)

    @data(*test_info)  # 这里很多教程会用 @unpack 其实不需要的打包好数据再重新放入test_info中
    def test_case(self, test_info):
        print('111')

def find_path():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    base_dir = str(base_dir)
    base_dir = base_dir.replace('\\', '/')
    base = base_dir.split('/SDK')[0]
    return base + '/SDK'


def xor(data, datalen=0):
    ret = 0
    if datalen == 0:
        datalen = len(data)
        print("datalen:  " + str(datalen))
    try:
        for i in range(datalen):
            ret ^= data[i]
        return ret
    except IndexError:
        print('Xor bytearray index out of range')
        return -1

def bytes_string_to_bytes_array(str):
    if str == '':
        return ''
    # return ''.join(str.split()).decode('hex')
    return bytes.fromhex(''.join(str.split()))


def str_to_bytes(str):
    # 字符串转换为16进制ascll字符列表
    list = []
    for i in range(0, len(str)):
        list.append(ord(str[i]))
    result = [int(hex(x),16) for x in bytes(list)]
    result1 = [hex(x) for x in bytes(list)]
    return result,result1

class ddd:

    def __init__(self):
        pass

    def get_mac(self, mac):
        conver = Convert(0x00)

        self.send(mac, conver)

    def send(self,a ,b):
        print(b.head)
        pass

class Convert:
    head = 0xFF
    length = 0x00
    commandID = 0x00
    data = []
    valid = 0x00
    teal = 0xFE

    def __init__(self, cmd, data=None):
        if data is None:
            data = []
        self.head=0xff
        self.length=len(data)+2
        self.commandId = cmd
        self.data = data
        self.valid=self.getValid()
        self.teal=0xfe


    def getValid(self):
        return 1


def intToBytes(value):
    src = []
    src.append(value >> 24 & 0xff)
    src.append(value >> 16 & 0xff)
    src.append(value >> 8 & 0xff)
    src.append(value & 0xff)
    return src

def bytesToInt(value):
    return (value[0]<<24)+(value[1]<<16)+(value[2]<<8)+(value[3])



def ByteToHex(bins):
    return ''.join(["%02X " % x for x in bins]).strip()


def HexToByte(hexStr):
    return bytes.fromhex(hexStr)


def data_to_bytes(DataPoints):
    """解析数据端点，返回可读数据"""
    data = []
    for datapoint in DataPoints:
        data.append(datapoint.index)

        d1 = (datapoint.type << 4 & 0xf0) + (datapoint.length >> 8 & 0x0f)
        d2 = datapoint.length & 0xff

        data.append(d1)  # 类型+长度
        data.append(d2)

        data += Xlink_Utils.value_to_bytes(datapoint.value,datapoint.type)

    return data

def serial_send_packet_convert(data):
    index = 1
    # convert_list = data
    for i in range(1, len(data)):
        if data[index] == 0xFF:
            data[index] = 0x7F
            index += 1
            data.insert(index, 0xFD)
        elif data[index] == 0xFE:
            data[index] = 0x7E
            index += 1
            data.insert(index, 0xFD)
        elif data[index] == 0xFD:
            data[index] = 0x7D
            index += 1
            data.insert(index, 0xFD)
        index += 1
    return data

class DataPoint:

    def __init__(self, index, types, value):
        self.index = index
        self.type = types
        self.value = value
        self.length = {
            0: 1,
            1: 2,
            2: 2,
            3: 4,
            4: 4,
            5: 8,
            6: 8,
            7: 4,
            8: 8,
            9:  len(self.value) if type(self.value) == str else 0,
            10: len(self.value) if type(self.value) == list else 0,
        }.get(self.type, 0)


class JsonCustomEncoder(json.JSONEncoder):

    def encode(self, field):
        if field is None:
            return 'aa'
        else:
            super().encode(field)

def convert_to_builtin_type(obj):
    # print 'default(', repr(obj), ')'
    # Convert objects to a dictionary of their representation
    d = { '__class__':obj.__class__.__name__,
          '__module__':obj.__module__,
        }
    d.update(obj.__dict__)
    return d

if __name__ == "__main__":
    # print(int(time.time()))
    # timeArray = time.localtime(1541642437)
    # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    # print(otherStyleTime)
    a = "{'status': 200, 'msg': 'OK', 'data': {'_id': '5be4ecb1d93f036a4132171f'}}"
    print('OK' in a)
    # for i in a.keys():
    #     print(i)
    # b = json.dumps(a,cls=encoder_my.JSONEncoder)
    # print(b)

    # dps_list = []
    # for i in a:
    #     dp = []
    #     dp.append(i['index'])
    #     dp.append(i['type'])
    #     if i['value'] == true:
    #         dp.append(1)
    #     elif i['value'] == false:
    #         dp.append(0)
    #     else:
    #         dp.append(i['value'])
    #     dps_list.append(dp)
    # print(dps_list)

    # b = [hex(x) for x in bytes(a)]
    # print(b)
    # strs = ''
    # for i in a:
    #     print(chr(i))
    #     strs = strs + chr(i)
    # print(type(strs))



    # args = '160fa6af9c3e3a00160fa6af9c3e3a01'
    # list = []
    #
    # for i in range(0, len(args)):
    #     print(args[i])
    #     print(ord(args[i]))
    #     list.append(ord(args[i]))
    # print([hex(x)for x in bytes(list)])


    # curPath = os.path.abspath(os.path.dirname(__file__))
    # rootPath = curPath[:curPath.find("SDK\\") + len("SDK\\")]
    # print(curPath)
    # print(find_path())