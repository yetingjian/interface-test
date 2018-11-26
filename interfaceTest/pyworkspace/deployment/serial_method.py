# coding=utf-8

import sys,os,re
import unittest
import serial
import serial.tools.list_ports
import function as func
import time
import traceback
import xlrd
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os.path


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

def xor(data, datalen=0):
    ret = 0
    if datalen == 0:
        datalen = len(data)
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
    return ''.join(str.split()).decode('hex')
    #return bytes.fromhex(''.join(str.split()))

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
    nrows = table.nrows
    ncols = table.ncols
    colnames = table.row_values(colnameindex)
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
    list = []
    result = []
    for i in range(0, len(str)):
        list.append(ord(str[i]))
    for i in range(0, len(list)):
        result.append(hex(list[i]))
    return result

def byteslist_to_asclllist(str):
    list = []
    for x in str:
        list.append(int(x, 16))
    return list

def parity_bit(pid, pkey):
    # data = excel_table_byindex(path_equip, 0)
    # if (len(data) <= 0):
    PID = str_to_bytes(pid)
    PKEY = str_to_bytes(pkey)
    instruct = ['0x00', '0x42', '0x03']
    parity = instruct + PID + PKEY
    k = []
    for i in range(0, len(parity)):
        if (int(parity[i], 16) < 10):
            parity[i] = parity[i].zfill(4)
        else:
            parity[i] = parity[i]
        k.append(parity[i])
    k = "".join(k)
    k = k.replace('0x', '')
    u = bytes_string_to_bytes_array(k)
    h = xor(bytearray(u))
    parity = hex(h)
    parity = parity.split()
    # print("parity :",parity)
    return parity

def find_serial(com):
    global serialFd
    # data = excel_table_byindex(path_equip, 0)
    # if (len(data) <= 0):
    plist = list(serial.tools.list_ports.comports())
    func.log('len(plist): ' + str(len(plist)))
    if len(plist) <= 0:
        print(u"没有发现端口!")
    else:
        plist_0 = list(plist[0])
        # serialName = plist_0[0]
        serialName = com
        serialFd = serial.Serial(serialName, 115200, timeout=1)
        func.log('serialFd: '+ str(serialFd))
        return serialFd

def find_serial2(com):
    global serialFd1
    # data = excel_table_byindex(path_equip, 0)
    # if (len(data) <= 0):
    plist = list(serial.tools.list_ports.comports())
    func.log('len(plist): ' + str(len(plist)))
    if len(plist) <= 0:
        print(u"没有发现端口!")
    else:
        plist_0 = list(plist[0])
        # serialName = plist_0[0]
        serialName = com
        serialFd1 = serial.Serial(serialName, 115200, timeout=1)
        func.log('serialFd: '+ str(serialFd1))
        return serialFd1

def set_PID_PKEY(pid, pkey):
    # data = excel_table_byindex(path_equip, 0)
    # if (len(data) <= 0):
    response = None
    try:
        PID = str_to_bytes(pid)
        PKEY = str_to_bytes(pkey)
        HF = ['0xFF']
        instruct = ['0x00', '0x42', '0x03']
        HT = ['0xFE']
        parity = parity_bit(pid, pkey)
        send_command = HF + instruct + PID + PKEY + parity + HT
        send_ascll = byteslist_to_asclllist(send_command)
        # print(send_ascll)
        b3 = serial_send_packet_convert(send_ascll)
        serialFd.write(b3)
        response = serialFd.readall()
        response = derial_recv_packe_convert(response)
        func.log(('response:', list(response)))
        if list(response) != '':
            return True
    except Exception:
        func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
        raise


def mcu_wifi():
    result = []
    HF = [0xFF]
    HT = [0xFE]
    ZL = [0x83]
    DL1 = [0x00,0x06]
    DL2 = [0x00,0x06]
    DT1 = [0x00, 0x00, 0x01, 0x01]
    DT2 = [0x01, 0x00, 0x01, 0x96]
    JY1 = [0x85]
    JY2 = [0x13]
    send1 = HF + DL1 + ZL + DT1 + JY1 + HT
    send2 = HF + DL2 + ZL + DT2 + JY2 + HT
    # 发送转换
    try:
        for send in (send1,send2):
            send = serial_send_packet_convert(send)
            serialFd.write(send)
            response = serialFd.readall()
            # 将bytes类型转化为16进制
            list_response = list(response)
            #response = [hex(x) for x in bytes(response)]
            # 返回结果转换
            response = derial_recv_packe_convert(list_response)
            func.log(response)
            for i in range(0,len(response)):
                if(response[i] == "0xfe"):
                    try:
                        assert response[i-2] =='0x0', u"转发失败"
                        break
                    except:
                        continue
    except Exception:
        func.log(('traceback.format_exc():\n%s' % traceback.format_exc()))
        raise


def reset_mcu():
    send = [0xFF, 0x00, 0x02, 0x06, 0x04, 0xFE]
    send = serial_send_packet_convert(send)
    serialFd.write(send)
    response = serialFd.readall()
    assert response != None, u"重置失败"
    list_response = list(response)
    # response = [hex(x) for x in bytes(response)]
    # 返回结果转换
    response = derial_recv_packe_convert(list_response)
    func.log(response)
