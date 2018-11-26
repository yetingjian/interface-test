#conding = utf-8

import sys,os,re
import unittest
import serial
import serial.tools.list_ports
import time
import xlrd
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os.path

def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # print path + ' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print path + ' 目录已存在'
        return False

def xor(data, datalen=0):
    ret = 0
    print(data[0])
    print(data[1])
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
    #convert_list = data
    for i in range(1, len(data) - 2):
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

def open_excel(file='file.exe'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print (str(e))

def excel_table_byindex(file='file.xls', colnameindex=0, by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    colnames = table.row_values(colnameindex)  # 某一行数据
    list = []
    for rownum in range(1, nrows):

        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)
    return list

def str_to_bytes(str):
    #字符串转换为16进制ascll字符列表
    list = []
    for i in range(0, len(str)):
        list.append(ord(str[i]))
    result = [hex(x) for x in bytes(list)]
    return result

def byteslist_to_asclllist(str):
    list = []
    for x in str:
        list.append(int(x, 16))
    return list

def parity_bit():
    #校验位计算
    # data = excel_table_byindex(path_equip, 0)
    # if (len(data) <= 0):
    #     assert 0, u"Excel数据异常"
    # PID = str_to_bytes(data[0][u"参数值"])
    # PKEY = str_to_bytes(data[1][u"参数值"])
    PID = str_to_bytes("160fa6af9c3e3a00160fa6af9c3e3a01")
    PKEY = str_to_bytes("f2a9ec41f3c41ab4c6108a05a92a06a9")
    #instruct = 数据长度（'0x00', '0x42'） + 指令（'0x03'）
    instruct = ['0x00', '0x42', '0x03']
    parity =  instruct + PID + PKEY
    k = []
    for i in range(0, len(parity)):
        #对ascii值小于10的数值左补0
        if (int(parity[i], 16) < 10):
            parity[i] = parity[i].zfill(4)
        else:
            parity[i] = parity[i]
        k.append(parity[i])
    # 转化为字符串
    k = "".join(k)
    #删除0x字符
    k = k.replace('0x', '')
    u = bytes_string_to_bytes_array(k)
    h = xor(u)
    parity = hex(h)
    #字符串转为字符串列表
    parity = parity.split()
    # print("parity :",parity)
    return parity


class Serial_test(unittest.TestCase):
    @staticmethod
    def find_serial():
        global serialFd
        # data = excel_table_byindex(path_equip, 0)
        # if (len(data) <= 0):
        #     assert 0, u"Excel数据异常"
        #获取所有的串口名称
        plist = list(serial.tools.list_ports.comports())
        if (len(plist) <= 0):
            print("没有发现端口!")
        else:
            plist_0 = list(plist[0])
            serialName = plist_0[0]
            serialFd = serial.Serial(serialName, 115200, timeout=1)
            # print("可用端口名>>>", serialFd.name)
            return serialFd

    @staticmethod
    def set_PID_PKEY():
        # data = excel_table_byindex(path_equip, 0)
        # if (len(data) <= 0):
        #     assert 0, u"Excel数据异常"
        # 转换格式
        PID1 = str_to_bytes("160fa6af9c3e3a00160fa6af9c3e3a01")
        PKEY1 = str_to_bytes("f2a9ec41f3c41ab4c6108a05a92a06a9")
        #修改PID1,PEKY1时要修改parity_bit()方法中的PID,PKEY
        print(PID1,PKEY1)
        # print("data :",data[0][u"参数值"],data[1][u"参数值"])
        #数据长度固定64位（PID,PKEY）数据长度 = 指令 +数据 + 校验（1+ x +1）
        #帧头HF，帧尾HT
        HF = ['0xFF']
        instruct = ['0x00', '0x42', '0x03']
        HT = ['0xFE']
        #校验位计算
        parity = parity_bit()
        send_command = HF + instruct + PID1 + PKEY1 + parity + HT
        # print("转换前 》》",send_command)
        send_ascll = byteslist_to_asclllist(send_command)
        # print(send_ascll)
        #发送数据转换
        b3 = serial_send_packet_convert(send_ascll)
        serialFd.write(b3)
        response = serialFd.readall()
        # print("转换前response :",response)
        #接收数据转换
        response = derial_recv_packe_convert(response)
        # print("接收转码：",response)
        # 将bytes类型转化为16进制
        response = [hex(x) for x in bytes(response)]
        print("转换后response :", response)
        # write_str(u"", filename, "0xfe", "set_PID_PKEY")
        # print("转换后response :", response)