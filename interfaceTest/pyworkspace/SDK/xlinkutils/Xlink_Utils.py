# -*- coding: utf-8 -*-
import json
import random
from struct import pack, unpack
import time
from datetime import datetime

import os
import xlrd

# from Interface.SerialPacket import Device
from xlinkutils.xlog import XLog


class UtilsException(Exception):
    def __init__(self, err='UtilsException'):
        Exception.__init__(self, err)


class UtilsDataLengthException(UtilsException):
    def __init__(self, err='len(data) is not equals datalen '):
        UtilsException.__init__(self, err)


def current_time():
    t = time.strftime('%Y-%m-%d %H:%M:%S.', time.localtime(time.time())) + str(datetime.now().microsecond)[0:3] + '\t'
    return t


def get_mac_address():
    import uuid
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
    x = hex(random.randint(0, 255))
    x = x[2:].upper()
    # print x
    return '%s%s%s%s%s%s%s' % (mac[0:2], mac[2:4], mac[4:6], mac[6:8], mac[8:10], mac[10:], x)


def readjson(jsontext):
    try:
        obj = json.loads(jsontext)
        return obj
    except Exception as e:
        print('readjson err!', Exception, ':', e)
        return None


def serial_send_packet_convert(data):
    index = 1
    # convert_list = data
    for i in range(1, len(data) - 2):
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


def derial_recv_packe_convert(data):
    index = 1
    # convert_list = data
    for i in range(1, len(data)):
        if data[index] == 0xFD:
            if data[index - 1] == 0x7F:
                data[index - 1] = 0xFF
                data.pop(index)
                index -= 1
            elif data[index - 1] == 0x7E:
                data[index - 1] = 0xFE
                data.pop(index)
                index -= 1
            elif data[index - 1] == 0x7D:
                data[index - 1] = 0xFD
                data.pop(index)
                index -= 1
        index += 1
    return data


def bytesToInt(value):
    return (value[0] << 24) + (value[1] << 16) + (value[2] << 8) + (value[3])


def ByteToHex(bins):
    return ''.join(["%02X " % x for x in bins]).strip()


def HexToByte(hexStr):
    return bytes.fromhex(hexStr)


def xor(data, datalen=0):
    ret = 0
    if datalen == 0:
        datalen = len(data)
    try:
        for i in range(datalen):
            ret ^= data[i]
        return ret
    except IndexError:
        XLog.GetLogger().info('Xor bytearray index out of range')
        return -1


def crc16(x, length=0):
    b = 0xA001
    a = 0xFFFF
    # data_type = type(x)
    # print isinstance(x,str)
    # byte in x:
    if length == 0:
        length = len(x)
    try:
        for index in range(length):
            # print (index)
            # if data_type == type('str') :
            if isinstance(x, str):
                a ^= ord(x[index])
                # print a
            # elif data_type == type(bytearray('1')):
            elif isinstance(x, bytearray):
                a ^= x[index]
                # print x[index]
            for i in range(8):
                last = a % 2
                a >>= 1
                if last == 1:
                    a ^= b
        print('crc16 is ' + hex(a))
    except IndexError:
        print('CRC16 bytearray index out of range')
    return a


class ValueType:
    BOOL = 0
    INT_16 = 1
    UNSIGNED_INT_16 = 2
    INT_32 = 3
    UNSIGNED_INT_32 = 4
    INT_64 = 5
    UNSIGNED_INT_64 = 6
    FLOAT = 7
    DOUBLE = 8
    STRING = 9
    BYTES = 10


def bytes_to_value(data, data_len, data_type, big_indian=True):
    ret = None
    raw = None
    a = []
    # print len(data)
    if len(data) is not data_len:
        raise UtilsDataLengthException()
        # return ret
    for v in data:
        a.append(hex(v))
    if big_indian is False:
        a.reverse()

    if data_type == ValueType.STRING:
        ret = bytes_to_strs(data)
    elif data_type == ValueType.BYTES:
        ret = data
    else:
        if data_len == 1:
            raw = pack('B', int(a[0], 16))
            if ValueType.BOOL == data_type:
                ret = unpack('B', raw)[0]
            # elif ValueType.CHAR == data_type:
            #     ret = unpack('b', raw)[0]
            # elif ValueType.CHAR == data_type:
            #     ret = unpack('B', raw)[0]
        elif data_len == 2:
            raw = pack('BB', int(a[1], 16), int(a[0], 16))
            if ValueType.INT_16 == data_type:
                ret = unpack('h', raw)[0]
            elif ValueType.UNSIGNED_INT_16 == data_type:
                ret = unpack('H', raw)[0]
        elif data_len == 4:
            raw = pack('BBBB', int(a[3], 16), int(a[2], 16), int(a[1], 16), int(a[0], 16))
            if ValueType.INT_32 == data_type:
                ret = unpack('i', raw)[0]
            elif ValueType.UNSIGNED_INT_32 == data_type:
                ret = unpack('I', raw)[0]
            elif ValueType.FLOAT == data_type:
                ret = unpack('f', raw)[0]
        elif data_len == 8:
            raw = pack('BBBBBBBB', int(a[7], 16), int(a[6], 16), int(a[5], 16), int(a[4], 16), int(a[3], 16),
                       int(a[2], 16), int(a[1], 16), int(a[0], 16))
            if ValueType.INT_64 == data_type:
                ret = unpack('q', raw)[0]
            elif ValueType.UNSIGNED_INT_64 == data_type:
                ret = unpack('Q', raw)[0]
            elif ValueType.DOUBLE == data_type:
                ret = unpack('d', raw)[0]
    return ret


def value_to_bytes(value, data_type, big_indian=True):
    byte = ''
    if data_type == ValueType.BOOL:
        byte = pack('B', value)
    # elif data_type == ValueType.CHAR:
    #     byte = pack('b', value)
    # elif data_type == ValueType.UNSIGNED_CHAR:
    #     byte = pack('B', value)
    elif data_type == ValueType.INT_16:
        byte = pack('h', value)
    elif data_type == ValueType.UNSIGNED_INT_16:
        byte = pack('H', value)
    elif data_type == ValueType.INT_32:
        byte = pack('i', value)
    elif data_type == ValueType.UNSIGNED_INT_32:
        byte = pack('I', value)
    elif data_type == ValueType.INT_64:
        byte = pack('q', value)
    elif data_type == ValueType.UNSIGNED_INT_64:
        byte = pack('Q', value)
    elif data_type == ValueType.FLOAT:
        byte = pack('f', value)
    elif data_type == ValueType.DOUBLE:
        byte = pack('d', value)
    elif data_type == ValueType.STRING:
        byte = strs_to_bytes(value)
    elif data_type == ValueType.BYTES:
        byte = value

    if big_indian and data_type != ValueType.BYTES:
        # print 'ddd'
        byte = bytearray(byte)
        byte.reverse()
        return bytearray(byte)
    return bytearray(byte)


def bytes_array_to_bytes_string(ByteArray, interval=''):
    str = ''
    for byte in ByteArray:
        str += ('%02X' % (byte))
        if interval != '':
            str += interval
    return str


def bytes_string_to_bytes_array(str):
    if str == '':
        return ''
    return ''.join(str.split()).decode('hex')


def strs_to_bytes(*args):
    """字符串转字节数据"""
    list = []
    for arg in args:
        for i in range(0, len(arg)):
            list.append(ord(arg[i]))
    return [int(hex(x), 16) for x in bytes(list)]


def bytes_to_strs(list):
    str_result = ''
    for i in list:
        str_result = str_result + chr(i)
    return str_result


def ints_to_bytes(*args):
    lists = []
    for i in args:
        lists.append(i)
    return lists


def excel_table_byindex(file, start, end):
    data = open_excel(file)
    table = data.sheets()[0]
    list = []
    colnames = table.row_values(0)
    for i in range(start - 1, end):
        row = table.row_values(i)
        app = {}
        for i in range(1, 5):
            app[colnames[i]] = row[i]
        list.append(app)
    return list


def get_device_list(file, sheet, start, end):
    data = open_excel(file)
    table = data.sheets()[sheet]
    ncols = table.ncols
    list = []
    colnames = table.row_values(0)
    for i in range(start - 1, end):
        row = table.row_values(i)
        app = {}
        for i in range(0, ncols):
            app[colnames[i]] = row[i]
        list.append(app)
    return list


def get_server_config(file, sheet, start, end):
    data = open_excel(file)
    table = data.sheets()[sheet]
    ncols = table.ncols
    colnames = table.row_values(0)
    app = {}
    for i in range(start, end +1 ):
        row = table.row_values(i)
        for i in range(0, ncols):
            app[colnames[i]] = row[i]
    return app

def get_user_list(file, sheet, start, end):
    data = open_excel(file)
    table = data.sheets()[sheet]

    list = []
    colnames = table.row_values(0)
    for i in range(start - 1, end):
        row = table.row_values(i)
        app = {}
        for i in range(0, 5):
            app[colnames[i]] = row[i]
        list.append(app)
    return list

def load_test_excel(file):
    data = {}
    excle = open_excel(file)
    for i in range(len(excle.sheets())):
        table = excle.sheets()[i]
        nrows = table.nrows
        ncols = table.ncols
        head_row = table.row_values(0)
        data_sheet = {}
        for j in range(1, nrows):
            row_data = {}
            row_value = table.row_values(j)
            for k in range(1, ncols):
                row_data[head_row[k]] = row_value[k]
            if str(row_value[0]) in data_sheet.keys():
                if type(data_sheet[str(row_value[0])]) == list:
                    data_sheet[str(row_value[0])].append(row_data)
                else:
                    data_list = []
                    data_list.append(data_sheet[str(row_value[0])])
                    data_list.append(row_data)
                    data_sheet[str(row_value[0])] = data_list
            else:
                data_sheet[str(row_value[0])] = row_data
        data[excle.sheets()[i].name] = data_sheet
    return data


def get_datapoints_list(file, sheet, start, end):
    data = open_excel(file)
    table = data.sheets()[sheet]
    list = []
    colnames = table.row_values(0)
    for i in range(start - 1, end):
        row = table.row_values(i)
        app = {}
        for i in range(1, 4):
            app[colnames[i]] = row[i]
        list.append(app)
    return list


def load_data_points(path_device, sheet, start, end):
    sdk_dps = []
    serial_valid_dps = []
    dp_list = get_datapoints_list(path_device, sheet, start, end)
    for dp in dp_list:
        a = {}
        b = []
        a['type'] = int(dp['枚举值（int）'])
        a['index'] = int(dp['索引index（int）'])
        # if int(dp['枚举值（int）']) in (1,2,3,4,8,9):
        #     a['value'] = int(dp['value（string）'])
        # elif int(dp['枚举值（int）']) == 5:
        #     a['value'] = float(dp['value（string）'])
        # elif int(dp['枚举值（int）']) == 6:
        #     a['value'] = dp['value（string）']
        # elif int(dp['枚举值（int）']) == 7:
        #     a['value'] = bytearray(dp['value（string）'])
        a['value'] = str(dp['value（string）'])
        sdk_dps.append(a)
        b.append(int(dp['索引index（int）']))
        b.append(int(dp['枚举值（int）']))
        b.append(dp['value（string）'])
        serial_valid_dps.append(b)
    return sdk_dps,serial_valid_dps

#
# def load_device_config(path_device, start_line, end_line):
#     """读取设备配置表"""
#     device_list = []
#     lists = get_device_list(path_device, 1, start_line, end_line)
#     for d in lists:
#         device = Device()
#         device.mac = d['mac']
#         device.time_out = int(d[u'超时'])
#         device.comm = d[u'串口']
#         device.baud_rate = int(d[u'码率'])
#         device_list.append(device)
#     return device_list


def find_path():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    base_dir = str(base_dir)
    base_dir = base_dir.replace('\\', '/')
    base = base_dir.split('/SDK')[0]
    return base + '/SDK'





def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    a = '22AA'
    print(HexToByte(a))
    # crc = CRCGenerator()
    # crc.create('aaaa')

    # crc16("1234567890")
    # a = bytearray.fromhex("12 34 56 78 90")
    # crc16(a)
    # # test = [0x41, 0x8d, 0x00, 0x00]
    # # test = [0x00, 0x00,0x00, 0x00,0xff, 0xff, 0xff, 0xff]
    # # print BytesToValue(test,8,ValueType.INT_64)
    # #print a
    # print(list(value_to_bytes(65535, ValueType.DOUBLE)))
