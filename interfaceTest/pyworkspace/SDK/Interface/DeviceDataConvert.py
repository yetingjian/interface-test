from time import sleep

from Interface.DataPoint import DataPoint
from xlinkutils import Xlink_Utils

global false, true
false = False
true = True

class Convert:
    def __init__(self, cmd=None, data=None):
        if data is None:
            data = []
        self.head = 0xff
        self.length = len(data) + 2
        self.commandId = cmd
        self.data = data
        self.valid = self.getvalid()
        self.teal = 0xfe

    def getvalid(self):
        """生成检验位"""
        valid_list = []
        valid_list.append(self.length)
        valid_list.append(self.commandId)
        for i in self.data:
            valid_list.append(i)
        return Xlink_Utils.xor(valid_list)

    @staticmethod
    def checkVaiid(obj):
        """计算返回数据的校验位"""
        valid_list = []
        valid_list.append(obj.length)
        valid_list.append(obj.commandId)
        if obj.data is not None:
            for i in obj.data:
                valid_list.append(i)
        return Xlink_Utils.xor(valid_list)

    @staticmethod
    def getDataPoints(data):
        """数据端点指令的数据部分封装解析，返回指令"""
        pass

    @staticmethod
    def data_to_bytes(*args):
        """解析发送的数据端点，返回字节数组"""
        data = []
        for datapoint in args:
            data.append(datapoint.index)
            d1 = (datapoint.type << 4 & 0xf0) + (datapoint.length >> 8 & 0x0f)
            d2 = datapoint.length & 0xff
            data.append(d1)  # 类型+长度
            data.append(d2)
            data += Xlink_Utils.value_to_bytes(datapoint.value, datapoint.type)
        return data

    @staticmethod
    def bytes_data(datas):
        """解析接收的数据端点，返回DataPoint对象"""
        data_list = []
        while len(datas) >= 4:
            index = datas[0]
            type = datas[1] >> 4 & 0x0f
            length = (datas[1] & 0x0f)*256 + datas[2]
            data = datas[3:length + 3]
            data_list.append(DataPoint(index, type, Xlink_Utils.bytes_to_value(data, length, type)))
            del datas[0:length + 3]
            sleep(0.001)
        return data_list

    @staticmethod
    def getCommand(comm):
        """根据接收的指令，返回可读数据"""
        if comm.commandId == 0x00:
            return comm.commandId, Convert.get_str_result(comm.data)
        if comm.commandId == 0x01:
            return comm.commandId, comm.data
        if comm.commandId == 0x02:
            return comm.commandId, [Convert.get_ascii_str_result(comm.data)[0:32],
                                    Convert.get_ascii_str_result(comm.data)[32:64]]
        if comm.commandId == 0x03:
            return comm.commandId, None
        if comm.commandId == 0x04:
            return comm.commandId, None
        if comm.commandId == 0x05:
            return comm.commandId, None
        if comm.commandId == 0x06:
            return comm.commandId, None
        if comm.commandId == 0x07:
            return comm.commandId, comm.data
        if comm.commandId == 0x08:
            return comm.commandId, comm.data
        if comm.commandId == 0x09:
            return comm.commandId, None
        if comm.commandId == 0x0A:
            return comm.commandId, None
        if comm.commandId == 0x0B:
            return comm.commandId, Convert.get_ascii_str_result(comm.data)
        if comm.commandId == 0x0C:
            return comm.commandId, None
        if comm.commandId == 0x0D:
            return comm.commandId, comm.data
        if comm.commandId == 0x0E:
            return comm.commandId, comm.data
        if comm.commandId == 0x0F:
            return comm.commandId, comm.data
        if comm.commandId == 0x10:
            return comm.commandId, comm.data
        if comm.commandId == 0x11:
            return comm.commandId, comm.data
        if comm.commandId == 0x12:
            return comm.commandId, comm.data
        if comm.commandId == 0x13:
            return comm.commandId, Convert.get_ascii_str_result(comm.data)
        if comm.commandId == 0x14:
            return comm.commandId, None
        if comm.commandId == 0x30:
            return comm.commandId, comm.data
        if comm.commandId == 0x31:
            return comm.commandId, comm.data
        if comm.commandId == 0x32:
            return comm.commandId, comm.data
        if comm.commandId == 0x33:
            return comm.commandId, None
        if comm.commandId == 0x34:
            return comm.commandId, comm.data
        if comm.commandId == 0x82:
            return comm.commandId, Convert.bytes_data(comm.data)
        if comm.commandId == 0x83:
            return comm.commandId, comm.data
        if comm.commandId == 0x84:
            return comm.commandId, comm.data
        if comm.commandId == 0x85:
            return comm.commandId, comm.data

    @staticmethod
    def get_str_result(data):
        """字节串直接转字符串"""
        hex_list = [hex(x) for x in bytes(data)]
        str_result = ''
        for i in hex_list:
            str_result = str_result + i.replace('0x', '').upper()
        return str_result

    @staticmethod
    def get_ascii_str_result(data):
        """字节串ascii码转字符串"""
        str_result = ''
        for i in data:
            str_result = str_result + chr(i)
        return str_result

    @staticmethod
    def get_int_result(data):
        pass

    @staticmethod
    def get_result_data(data_list):
        """从串口结果中获取指令id和data部分信息放到数据commandID,data中"""
        objects = Convert
        objects.head = data_list[0]
        objects.length = int.from_bytes(data_list[1:3], byteorder='big')
        objects.commandId = data_list[3]
        if objects.length == 2:
            objects.data = None
        else:
            objects.data = data_list[4:objects.length + 2]
        objects.valid = data_list[objects.length + 2]
        if objects.valid == Convert.checkVaiid(objects):
            objects.teal = data_list[objects.length + 3]
            return objects
        else:
            return False

    @staticmethod
    def strs_to_bytes(*args):
        """字符串转字节数据"""
        list = []
        for arg in args:
            for i in range(0, len(arg)):
                list.append(ord(arg[i]))
        return [int(hex(x), 16) for x in bytes(list)]

    @staticmethod
    def data_points_convert_from_search_result(data):
        """解析查询数据端点结果，返回DataPoint对象"""
        point_list = []
        for point in data['result']['list']:
            if point['value'] == 'true':
                point['value'] = 1
            elif point['value'] == 'false':
                point['value'] = 0
            dp = DataPoint(int(point['index']), int(point['type']), point['value'])
            point_list.append(dp)
        return point_list

    @staticmethod
    def data_points_convert_from_notification(data):
        """解析数据端点通知结果，返回DataPoint对象"""
        point_list = []
        mac = data['XDevice']['mac']
        for point in data['datapoints']:
            if point['value'] == 'true':
                point['value'] = 1
            elif point['value'] == 'false':
                point['value'] = 0
            dp = DataPoint(int(point['index']), int(point['type']), point['value'])
            point_list.append(dp)
        return mac, point_list

