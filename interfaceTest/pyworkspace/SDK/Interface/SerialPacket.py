# # encoding: UTF-8
# import json
# import traceback
# from pprint import pprint
# from queue import Queue, Empty
# import builtins
# import threading
# import serial
# import serial.tools.list_ports
# import os
#
# import threadpool
# from xlinkutils.EventManager import EventManager, Event
# from xlinkutils import Xlink_Utils
# from time import sleep
#
# from xlinkutils.Xlink_Utils import get_device_list
# from xlinkutils.xlog import XLog
#
# global false, true
# false = False
# true = True
#
#
# class Device:
#
#     def __init__(self):
#         """设备管理类属性"""
#         self.baud_rate = 0
#         self.time_out = 0
#         self.comm = ''
#         self.serialFd = None
#         self.local_statue = 0
#         self.server_statue = 0
#         self.mac = None
#         self.device_id = 0
#         self.pid = ''
#         self.p_key = ''
#         self.sn = ''
#         self.version = None
#         self.local_time = None
#         self.enable_couple_statue = None
#         self.enable_testing_statue = None
#         self.enable_subscript_statue = None
#         self.ping_code = None
#
#     def __str__(self):
#         return 'pid:' + str(self.pid) + ' p_key:' + str(self.p_key) + ' mac:' + str(self.mac)
#
#     def get_mac(self):
#         DeviceManager.get_mac(self.mac)
#
#     def get_connect_statue(self):
#         DeviceManager.get_connect_statue(self.mac)
#
#     def get_pid_pkey(self):
#         DeviceManager.get_pid_pkey(self.mac)
#
#     def set_pid_pkey(self, pid, pkey):
#         DeviceManager.set_pid_pkey(self.mac, pid, pkey)
#
#     def set_distribute_mode(self):
#         DeviceManager.set_distribute_mode(self.mac)
#
#     def restart_wifi_module(self):
#         DeviceManager.restart_wifi_module(self.mac)
#
#     def reset_wifi_module(self):
#         DeviceManager.reset_wifi_module(self.mac)
#
#     def get_muc_version(self):
#         DeviceManager.get_muc_version(self.mac)
#
#     def get_local_time(self):
#         DeviceManager.get_local_time(self.mac)
#
#     def set_seeable_statue(self, statue):
#         DeviceManager.set_seeable_statue(self.mac, statue)
#
#     def set_ap_distribute_statue(self, statue):
#         DeviceManager.set_ap_distribute_statue(self.mac, statue)
#
#     def get_sn(self):
#         DeviceManager.get_sn(self.mac)
#
#     def set_sn(self, sn):
#         DeviceManager.set_sn(self.mac, sn)
#
#     def get_current_statue_and_signal(self):
#         DeviceManager.get_current_statue_and_signal(self.mac)
#
#     def set_testing_statue(self, *args):
#         DeviceManager.set_testing_statue(self.mac, *args)
#
#     def update_testing_data(self, *args):
#         DeviceManager.update_testing_data(self.mac, *args)
#
#     def set_testing_enable(self, statue):
#         DeviceManager.set_testing_enable(self.mac, statue)
#
#     def set_couple_enable(self, *args):
#         DeviceManager.set_couple_enable(self.mac, *args)
#
#     def set_subscribe_enable(self, *args):
#         DeviceManager.set_subscribe_enable(self.mac, *args)
#
#     def get_ping_code(self):
#         DeviceManager.get_ping_code(self.mac)
#
#     def set_ping_code(self, code):
#         DeviceManager.set_ping_code(self.mac, code)
#
#     def get_new_mission(self, *args):
#         DeviceManager.get_new_mission(self.mac, *args)
#
#     def request_download_new_mcu(self, data):
#         DeviceManager.request_download_new_mcu(self.mac, data)
#
#     def send_mcu_data(self, *args):
#         DeviceManager.send_mcu_data(self.mac, *args)
#
#     def send_data_finish(self, *args):
#         DeviceManager.send_data_finish(self.mac, *args)
#
#     def upload_update_result(self, *args):
#         DeviceManager.upload_update_result(self.mac, *args)
#
#     def set_data_point_82(self):
#         DeviceManager.get_data_point_82(self.mac)
#
#     def set_data_point_83(self, *args):
#         DeviceManager.set_data_point_83(self.mac, *args)
#
#     def set_data_point_84(self, dataponits):
#         DeviceManager.set_data_point_84(self.mac, dataponits)
#
#     def set_data_point_85(self, dataponits):
#         DeviceManager.set_data_point_85(self.mac, dataponits)
#
#
# class DeviceManager:
#     buff = []
#     device_list = []
#     active_list = []
#     __active = false
#     __instance = None
#
#     def __init__(self):
#         """初始化事件管理器"""
#         self.task_pool = None
#         self.requests = None
#         DeviceManager.__active = True
#         # self.thread1 = Thread(target=self.receive)
#         # self.thread2 = Thread(target=self.handel_packet)
#
#     @classmethod
#     def get_instance(cls):
#         if cls.__instance is None:
#             cls.__instance = DeviceManager()
#         return cls.__instance
#
#     def load_device_config(self, devices):
#         """读取设备配置表"""
#         for d in devices:
#             DeviceManager.device_list.append(d)
#         DeviceManager.buff = [[]] * len(self.device_list)
#
#     def start(self, device_list):
#         """获取所有串口并与配置表mac对应，赋值给serial_list"""
#         self.load_device_config(device_list)
#         plist = list(serial.tools.list_ports.comports())
#         for i in range(len(plist)):
#             com = list(plist[i])[0]
#             for device in self.device_list:
#                 if "USB-to-Serial" in list(plist[i])[1] and device.comm == com:
#                     serialFd = serial.Serial(com, device.baud_rate, timeout=device.time_out)
#                     device.serialFd = serialFd
#                     DeviceManager.active_list.append(device)
#         self.task_pool = threadpool.ThreadPool(len(DeviceManager.device_list))
#         self.requests = threadpool.makeRequests(DeviceManager.deviceHandler, DeviceManager.active_list)
#         for req in self.requests:
#             self.task_pool.putRequest(req)
#
#     @staticmethod
#     def getDevice(mac):
#         for device in DeviceManager.device_list:
#             if device.mac == mac:
#                 return device
#         return None
#
#     @staticmethod
#     def getDevices():
#         return DeviceManager.device_list
#
#     @staticmethod
#     def get_mac(mac):
#         """查询MAC地址"""
#         conver = Convert(0x00)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def get_connect_statue(mac):
#         """查询连接状态"""
#         conver = Convert(0x01)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def get_pid_pkey(mac):
#         """查询pid，pkey??该指令会返回pid，pkey，同时也会返回[255, 0, 4, 1, 1, 1, 5, 254]"""
#         conver = Convert(0x02)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def set_pid_pkey(mac, pid, pkey):
#         """设置pid，pkey"""
#         data = Xlink_Utils.strs_to_bytes(pid, pkey)
#         conver = Convert(0x03, data)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def set_distribute_mode(mac):
#         """设置进入配网模式"""
#         conver = Convert(0x04)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def restart_wifi_module(mac):
#         """重启wifi模组"""
#         conver = Convert(0x05)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def reset_wifi_module(mac):
#         """重设wifi模组"""
#         conver = Convert(0x06)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def get_muc_version(mac):
#         """查询固件版本"""
#         conver = Convert(0x07)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def get_local_time(mac):
#         """查询本地模糊时间"""
#         conver = Convert(0x08)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def set_seeable_statue(mac, statue):
#         """设置被发现状态"""
#         data = statue
#         conver = Convert(0x09, data)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def set_ap_distribute_statue(mac, statue):
#         """设置AP配网状态"""
#         data = Xlink_Utils.ints_to_bytes(statue)
#         conver = Convert(0x0A, data)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def get_sn(mac):
#         """查询SN字段"""
#         conver = Convert(0x0B)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def set_sn(mac, sn):
#         """设置sn"""
#         data = Xlink_Utils.strs_to_bytes(sn)
#         conver = Convert(0x0C, data)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def get_current_statue_and_signal(mac):
#         """查询S当前状态和信号质量"""
#         conver = Convert(0x0D)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def set_testing_statue(mac, *args):
#         """设置产测模式状态??data添什么"""
#         data = Xlink_Utils.ints_to_bytes(*args)
#         conver = Convert(0x0E, data)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def update_testing_data(mac, *args):
#         """更新WIFI模组自定义产测数据??data添什么"""
#         data = Xlink_Utils.ints_to_bytes(*args)
#         conver = Convert(0x0F, data)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def set_testing_enable(mac, statue):
#         """产测使能设置"""
#         data = Xlink_Utils.ints_to_bytes(statue)
#         conver = Convert(0x10, data)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def set_couple_enable(mac, *args):
#         """配对使能设置???data添什么"""
#         data = Xlink_Utils.ints_to_bytes(*args)
#         conver = Convert(0x11, data)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def set_subscribe_enable(mac, *args):
#         """配对使能设置???data添什么"""
#         data = Xlink_Utils.ints_to_bytes(*args)
#         conver = Convert(0x12, data)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def get_ping_code(mac):
#         """查询WIFI模组PINGCODE字段"""
#         conver = Convert(0x13)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def set_ping_code(mac, code):
#         """设置PINGCODE字段"""
#         data = Xlink_Utils.strs_to_bytes(code)
#         conver = Convert(0x14, data)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def get_new_mission(mac, *args):
#         """MCU向WIFI模组查询是否有新任务??data是否包含int和str"""
#         data = Xlink_Utils.ints_to_bytes(*args)
#         conver = Convert(0x30, data)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def request_download_new_mcu(mac, data):
#         """MCU向WIFI模组发请求下载新固件"""
#         datas = Xlink_Utils.ints_to_bytes(data)
#         conver = Convert(0x31, datas)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def send_mcu_data(mac, *args):
#         """WIFI模组向MCU发送新固件数据??data是否包含int和str"""
#         datas = Xlink_Utils.ints_to_bytes(*args)
#         conver = Convert(0x32, datas)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def send_data_finish(mac, *args):
#         """WIFI模组向MCU发送数据传输完成指令??data是否包含int和str"""
#         datas = Xlink_Utils.ints_to_bytes(*args)
#         conver = Convert(0x33, datas)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def upload_update_result(mac, *args):
#         """MCU向WIFI模组上报更新结果??data是否包含int和str"""
#         datas = Xlink_Utils.ints_to_bytes(*args)
#         conver = Convert(0x34, datas)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def get_data_point_82(mac):
#         """WIFI模组向MCU转发接收到的数据端点数据"""
#         conver = Convert(0x82)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def set_data_point_83(mac, *args):
#         """MCU向WIF模组发送数据端点数据"""
#         datas = Convert.data_to_bytes(*args)
#         conver = Convert(0x83, datas)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def set_data_point_84(mac, *args):
#         """MCU向WIFI模组发送所有数据端点数据"""
#         datas = Convert.data_to_bytes(*args)
#         conver = Convert(0x84, datas)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def set_data_point_85(mac, *args):
#         """MCU向WIFI发送数据端点数据"""
#         datas = Convert.data_to_bytes(*args)
#         conver = Convert(0x85, datas)
#         DeviceManager.send(mac, conver)
#
#     @staticmethod
#     def send(mac, commands):
#         """发送指令方法，通过mac遍历当前已打开的所有端口，发送指令"""
#         data = []
#         data.append(commands.head)
#         if commands.length > 255:
#             data.append(commands.length)
#         else:
#             data.append(0)
#             data.append(commands.length)
#         data.append(commands.commandId)
#         data = data + commands.data
#         data.append(commands.valid)
#         data.append(commands.teal)
#         send_command = Xlink_Utils.serial_send_packet_convert(data)
#
#         if type(mac) == str:
#             serialID = DeviceManager.getDevice(mac).serialFd
#             serialID.write(send_command)
#         elif type(mac) == list:
#             for i in mac:
#                 serialID = DeviceManager.getDevice(i).serialFd
#                 serialID.write(send_command)
#         try:
#             XLog.GetLogger().info('MCU->WIFI:[%s] %s', mac, Xlink_Utils.ByteToHex(send_command))
#         except Exception as e:
#             XLog.GetLogger().info(e)
#             raise
#
#     # def get_com(self, mac):
#     #     """通过mac查找到对应串口"""
#     #     for i in self.serial_list:
#     #         if mac == i['mac']:
#     #             return i['object']
#     #     else:
#     #         print('mac not in serial_list')
#     @staticmethod
#     def deviceHandler(device):
#         """串口接收指令线程"""
#         buff = []
#         try:
#             while DeviceManager.__active:
#                 n = device.serialFd.inWaiting()
#                 if n or len(buff) > 0:
#                     # 接收
#                     recv_data = device.serialFd.read(n)
#                     # if recv_data[-1] != 0x7e and recv_data[-1] != 0x7d and recv_data[-1] != 0x7f:
#                     #     recv_data = Xlink_Utils.derial_recv_packe_convert(bytearray(recv_data))
#                     buff += recv_data
#                     XLog.GetLogger().info('WIFI->MCU :[%s] %s', device.mac, Xlink_Utils.ByteToHex(recv_data))
#                     # 解析
#                     if buff != [] and (buff[-1] != 0x7e) and (buff[-1] != 0x7d) and (buff[-1] != 0x7f):
#                         # 转义
#                         buff = Xlink_Utils.derial_recv_packe_convert(buff)
#                         if len(buff) >= 5:
#                             if buff[0] == 0xff:
#                                 length = int.from_bytes(buff[1:3], byteorder='big')
#                                 if len(buff) >= length + 4:
#                                     data = buff[0:length + 4]
#                                     if buff[length + 3] != 0xfe:
#                                         XLog.GetLogger().warning('解析错误2' + Xlink_Utils.ByteToHex(buff))
#                                     del buff[0:length + 4]
#                                     comm = Convert.get_result_data(data)
#                                     if comm:
#                                         commandId, data = Convert.getCommand(comm)
#                                         DeviceManager.set_device_attributes(device, data, commandId)
#                                         XLog.GetLogger().debug('mac:%s commandId:%s data:%s', device.mac, commandId, data)
#                                         # 发送事件
#                                         try:
#                                             event = Event(type_=device.mac + ':' + str(commandId))
#                                             event.data['device'] = device
#                                             event.data['commandId'] = commandId
#                                             event.data['data'] = data
#                                             EventManager.get_instance().SendEvent(event)
#                                         except Exception as e:
#                                             XLog.GetLogger().warning(traceback.format_exc())
#
#                             else:
#                                 del buff[0]
#                 sleep(0.001)
#             XLog.GetLogger().warning('线程退出')
#         except Exception as error:
#             XLog.GetLogger().warning(traceback.format_exc())
#
#     @staticmethod
#     def set_device_attributes(dev, data, commid):
#         """更新Deveice类相关属性"""
#         if commid == Commands.GET_MAC:
#             dev.mac = data
#         if commid == Commands.GET_CONNECT_STATUE:
#             dev.local_statue = data[0]
#             dev.server_statue = data[1]
#         if commid == Commands.GET_PID_PKEY:
#             dev.pid = data[0]
#             dev.p_key = data[1]
#         # if commid== Commands.SET_DISTRIBUTE_MODE :
#         # if commid== Commands.RESTART_WIFI_MODULE :
#         # if commid== Commands.RESET_WIFI_MODULE :
#         if commid == Commands.GET_MUC_VERSION:
#             dev.version = data
#         if commid == Commands.GET_LOCAL_TIME:
#             dev.local_time = data
#         # if commid== Commands.SET_SEEABLE_STATUE :
#         # if commid== Commands.SET_AP_DISTRIBUTE_STATUE :
#         if commid == Commands.GET_SN:
#             dev.sn = data
#         # if commid== Commands.SET_SN :
#         if commid == Commands.GET_CURRENT_STATUE_AND_SIGNAL:
#             pass
#         # if commid== Commands.SET_TESTING_STATUE :
#         # if commid== Commands.UPDATE_TESTING_DATA :
#         if commid == Commands.SET_TESTING_ENABLE:
#             dev.enable_testing_statue = data
#         if commid == Commands.SET_COUPLE_ENABLE:
#             dev.enable_couple_statue = data
#         if commid == Commands.SET_SUBSCRIBE_ENABLE:
#             dev.enable_subscript_statue = data
#         if commid == Commands.GET_PING_CODE:
#             dev.ping_code = data
#         # if commid== Commands.SET_PING_CODE :
#         # if commid== Commands.GET_NEW_MISSION :
#         # if commid== Commands.REQUEST_DOWNLOAD_NEW_MCU :
#         # if commid== Commands.SEND_MCU_DATA :
#         # if commid== Commands.SEND_DATA_FINISH :
#         # if commid== Commands.UPLOAD_UPDATE_RESULT :
#         # if commid== Commands.SET_DATA_POINT_82 :
#         # if commid== Commands.SET_DATA_POINT_83 :
#         # if commid == Commands.SET_DATA_POINT_84 :
#         # if commid == Commands.SET_DATA_POINT_85 :
#
#
# class Convert:
#     def __init__(self, cmd=None, data=None):
#         if data is None:
#             data = []
#         self.head = 0xff
#         self.length = len(data) + 2
#         self.commandId = cmd
#         self.data = data
#         self.valid = self.getvalid()
#         self.teal = 0xfe
#
#     def getvalid(self):
#         """生成检验位"""
#         valid_list = []
#         valid_list.append(self.length)
#         valid_list.append(self.commandId)
#         for i in self.data:
#             valid_list.append(i)
#         return Xlink_Utils.xor(valid_list)
#
#     @staticmethod
#     def checkVaiid(obj):
#         """计算返回数据的校验位"""
#         valid_list = []
#         valid_list.append(obj.length)
#         valid_list.append(obj.commandId)
#         if obj.data is not None:
#             for i in obj.data:
#                 valid_list.append(i)
#         return Xlink_Utils.xor(valid_list)
#
#     @staticmethod
#     def getDataPoints(data):
#         """数据端点指令的数据部分封装解析，返回指令"""
#         pass
#
#     @staticmethod
#     def data_to_bytes(*args):
#         """解析发送的数据端点，返回字节数组"""
#         data = []
#         for datapoint in args:
#             data.append(datapoint.index)
#             d1 = (datapoint.type << 4 & 0xf0) + (datapoint.length >> 8 & 0x0f)
#             d2 = datapoint.length & 0xff
#             data.append(d1)  # 类型+长度
#             data.append(d2)
#             data += Xlink_Utils.value_to_bytes(datapoint.value, datapoint.type)
#         return data
#
#     @staticmethod
#     def bytes_data(datas):
#         """解析接收的数据端点，返回DataPoint对象"""
#         data_list = []
#         while len(datas) >= 4:
#             index = datas[0]
#             type = datas[1] >> 4 & 0x0f
#             length = (datas[1] & 0x0f)*256 + datas[2]
#             data = datas[3:length + 3]
#             data_list.append(DataPoint(index, type, Xlink_Utils.bytes_to_value(data, length, type)))
#             del datas[0:length + 3]
#             sleep(0.001)
#         return data_list
#
#     @staticmethod
#     def getCommand(comm):
#         """根据接收的指令，返回可读数据"""
#         if comm.commandId == 0x00:
#             return comm.commandId, Convert.get_str_result(comm.data)
#         if comm.commandId == 0x01:
#             return comm.commandId, comm.data
#         if comm.commandId == 0x02:
#             return comm.commandId, [Convert.get_ascii_str_result(comm.data)[0:32],
#                                     Convert.get_ascii_str_result(comm.data)[32:64]]
#         if comm.commandId == 0x03:
#             return comm.commandId, None
#         if comm.commandId == 0x04:
#             return comm.commandId, None
#         if comm.commandId == 0x05:
#             return comm.commandId, None
#         if comm.commandId == 0x06:
#             return comm.commandId, None
#         if comm.commandId == 0x07:
#             return comm.commandId, comm.data
#         if comm.commandId == 0x08:
#             return comm.commandId, comm.data
#         if comm.commandId == 0x09:
#             return comm.commandId, None
#         if comm.commandId == 0x0A:
#             return comm.commandId, None
#         if comm.commandId == 0x0B:
#             return comm.commandId, Convert.get_ascii_str_result(comm.data)
#         if comm.commandId == 0x0C:
#             return comm.commandId, None
#         if comm.commandId == 0x0D:
#             return comm.commandId, comm.data
#         if comm.commandId == 0x0E:
#             return comm.commandId, comm.data
#         if comm.commandId == 0x0F:
#             return comm.commandId, comm.data
#         if comm.commandId == 0x10:
#             return comm.commandId, comm.data
#         if comm.commandId == 0x11:
#             return comm.commandId, comm.data
#         if comm.commandId == 0x12:
#             return comm.commandId, comm.data
#         if comm.commandId == 0x13:
#             return comm.commandId, Convert.get_ascii_str_result(comm.data)
#         if comm.commandId == 0x14:
#             return comm.commandId, None
#         if comm.commandId == 0x30:
#             return comm.commandId, comm.data
#         if comm.commandId == 0x31:
#             return comm.commandId, comm.data
#         if comm.commandId == 0x32:
#             return comm.commandId, comm.data
#         if comm.commandId == 0x33:
#             return comm.commandId, None
#         if comm.commandId == 0x34:
#             return comm.commandId, comm.data
#         if comm.commandId == 0x82:
#             return comm.commandId, Convert.bytes_data(comm.data)
#         if comm.commandId == 0x83:
#             return comm.commandId, comm.data
#         if comm.commandId == 0x84:
#             return comm.commandId, comm.data
#         if comm.commandId == 0x85:
#             return comm.commandId, comm.data
#
#     @staticmethod
#     def get_str_result(data):
#         """字节串直接转字符串"""
#         hex_list = [hex(x) for x in bytes(data)]
#         str_result = ''
#         for i in hex_list:
#             str_result = str_result + i.replace('0x', '').upper()
#         return str_result
#
#     @staticmethod
#     def get_ascii_str_result(data):
#         """字节串ascii码转字符串"""
#         str_result = ''
#         for i in data:
#             str_result = str_result + chr(i)
#         return str_result
#
#     @staticmethod
#     def get_int_result(data):
#         pass
#
#     @staticmethod
#     def get_result_data(data_list):
#         """从串口结果中获取指令id和data部分信息放到数据commandID,data中"""
#         objects = Convert
#         objects.head = data_list[0]
#         objects.length = int.from_bytes(data_list[1:3], byteorder='big')
#         objects.commandId = data_list[3]
#         if objects.length == 2:
#             objects.data = None
#         else:
#             objects.data = data_list[4:objects.length + 2]
#         objects.valid = data_list[objects.length + 2]
#         if objects.valid == Convert.checkVaiid(objects):
#             objects.teal = data_list[objects.length + 3]
#             return objects
#         else:
#             return False
#
#     @staticmethod
#     def strs_to_bytes(*args):
#         """字符串转字节数据"""
#         list = []
#         for arg in args:
#             for i in range(0, len(arg)):
#                 list.append(ord(arg[i]))
#         return [int(hex(x), 16) for x in bytes(list)]
#
#     @staticmethod
#     def data_points_convert_from_search_result(data):
#         """解析查询数据端点结果，返回DataPoint对象"""
#         point_list = []
#         for point in data['result']['list']:
#             if point['value'] == 'true':
#                 point['value'] = 1
#             elif point['value'] == 'false':
#                 point['value'] = 0
#             dp = DataPoint(int(point['index']), int(point['type']), point['value'])
#             point_list.append(dp)
#         return point_list
#
#     @staticmethod
#     def data_points_convert_from_notification(data):
#         """解析数据端点通知结果，返回DataPoint对象"""
#         point_list = []
#         mac = data['XDevice']['mac']
#         for point in data['datapoints']:
#             if point['value'] == 'true':
#                 point['value'] = 1
#             elif point['value'] == 'false':
#                 point['value'] = 0
#             dp = DataPoint(int(point['index']), int(point['type']), point['value'])
#             point_list.append(dp)
#         return mac, point_list
#
#
# class DataPoint:
#     def __init__(self, index, types, value):
#         self.index = index
#         self.type = types
#         self.value = value
#         self.length = {
#             Xlink_Utils.ValueType.BOOL: 1,
#             Xlink_Utils.ValueType.INT_16: 2,
#             Xlink_Utils.ValueType.UNSIGNED_INT_16: 2,
#             Xlink_Utils.ValueType.INT_32: 4,
#             Xlink_Utils.ValueType.UNSIGNED_INT_32: 4,
#             Xlink_Utils.ValueType.INT_64: 8,
#             Xlink_Utils.ValueType.UNSIGNED_INT_64: 8,
#             Xlink_Utils.ValueType.FLOAT: 4,
#             Xlink_Utils.ValueType.DOUBLE: 8,
#             Xlink_Utils.ValueType.STRING: len(self.value) if type(self.value) == str else 0,
#             Xlink_Utils.ValueType.BYTES: len(self.value) if type(self.value) == list else 0,
#         }.get(self.type, 0)
#
#     def __setitem__(self, key, value):
#         pass
#
#     def __eq__(self, other):
#         """比较两个DataPoint是否相等，只比较index，value的值"""
#         return self.index == other.index and self.value == other.value
#
#     def __str__(self):
#         """字符串类型输出DataPoint对象"""
#         return '{"index":' + str(self.index) + ',"type":' + str(self.type) + ',"value":' + str(self.value) + '}'
#
#     def __repr__(self):
#         """自定义输出格式，字典类型输出DataPoint对象"""
#         return '{"index":' + str(self.index) + ',"type":' + str(self.type) + ',"value":' + str(self.value) + '}'
#
#
# class Commands:
#     GET_MAC = 0X00
#     GET_CONNECT_STATUE = 0X01
#     GET_PID_PKEY = 0X02
#     SET_PID_PKEY = 0X03
#     SET_DISTRIBUTE_MODE = 0X04
#     RESTART_WIFI_MODULE = 0X05
#     RESET_WIFI_MODULE = 0X06
#     GET_MUC_VERSION = 0X07
#     GET_LOCAL_TIME = 0X08
#     SET_SEEABLE_STATUE = 0X09
#     SET_AP_DISTRIBUTE_STATUE = 0X0A
#     GET_SN = 0X0B
#     SET_SN = 0X0C
#     GET_CURRENT_STATUE_AND_SIGNAL = 0X0D
#     SET_TESTING_STATUE = 0X0E
#     UPDATE_TESTING_DATA = 0X0F
#     SET_TESTING_ENABLE = 0X10
#     SET_COUPLE_ENABLE = 0X11
#     SET_SUBSCRIBE_ENABLE = 0X12
#     GET_PING_CODE = 0X13
#     SET_PING_CODE = 0X14
#     GET_NEW_MISSION = 0X30
#     REQUEST_DOWNLOAD_NEW_MCU = 0X31
#     SEND_MCU_DATA = 0X32
#     SEND_DATA_FINISH = 0X33
#     UPLOAD_UPDATE_RESULT = 0X34
#     SET_DATA_POINT_82 = 0X82
#     SET_DATA_POINT_83 = 0X83
#     SET_DATA_POINT_84 = 0X84
#     SET_DATA_POINT_85 = 0X85
#
#
#
#
# if __name__ == '__main__':
#     d = [{"index":0,"type":0,"value":1}]
#     b = [{"index":0,"type":0,"value":1}]
#
#     print(d == b)
#     # buff = []
#     # a = b'\xff\x00\x07\x82\x02\x10\x02\x05\xdcL\xfe\xff\x00\x07\x82\x02\x10\x02\x05\xdcL\xfe'
#     # buff += a
#     # buff = Xlink_Utils.derial_recv_packe_convert(buff)
#     # comm = Convert.get_result_data(buff)
#     # commandId, data = Convert.getCommand(comm)
#     #
#     # print(commandId)
#     # print(data)
#     # for j in data:
#     #     print(vars(j))
#     #     print(j.index)
#
#     # power = DataPoint(0, 0, 1)
#     # # fan = DataPoint(1, 1, 35)
#     # devMgr = DeviceManager(start_line=2, end_line=2)
#     #
#     # EventManager.get_instance().Start()
#     # # EventManager.get_instance().AddEvent(devMgr.getDevices()[0].mac, 0x83, upDataDp)
#     # for i in devMgr.getDevices():
#     #     EventManager.get_instance().AddEvent(i.mac, Commands.SET_DATA_POINT_82, upDataDp)
#     #     EventManager.get_instance().AddEvent(i.mac, Commands.GET_CONNECT_STATUE, getConnectStatue)
#     # #
#     # while true:
#     #     sleep(0.5)
#     #     for dev in devMgr.getDevices():
#     #         # dev.get_data_point_82()
#     #         dev.get_mac()
#     # #       dev.set_pid_pkey('160fa6af9c3e3a00160fa6af9c3e3a01', 'f2a9ec41f3c41ab4c6108a05a92a06a9')
#
#     # power = DataPoint(0, 0, 1)
#     # fan =  DataPoint(1, 0, 35)
#     #
#     # device1 = DeviceManager(start_line=2, end_line=2)
#     # device1.get_serial()
#     # device1.start()
#     # sleep(5)
#     # device1.get_mac()
#     # device1.get_connect_statue(device1.active_mac)
#     # device.set_data_point_83(device.active_mac,power,fan)
#     # # device.set_pid_pkey(device.active_mac, '160fa6af9c3e3a00160fa6af9c3e3a01','f2a9ec41f3c41ab4c6108a05a92a06a9')
#     # # device.set_testing_enable(device.active_mac, 1)
#     sleep(5000)
#
#     #
#     # data = Convert.data_to_bytes(power , fan)
#     # print(data)
#     # ss = Xlink_Utils.serial_send_packet_convert(data)
#     # print(ss)
#     # print(Xlink_Utils.ByteToHex(ss))
