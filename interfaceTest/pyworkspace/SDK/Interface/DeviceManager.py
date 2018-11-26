# encoding: UTF-8
import json
import traceback
from pprint import pprint
from queue import Queue, Empty
import builtins
import threading
import serial
import serial.tools.list_ports
import os
from Interface.Commands import Commands
import threadpool

from Interface.DeviceDataConvert import Convert
from xlinkutils.EventManager import EventManager, Event
from xlinkutils import Xlink_Utils
from time import sleep

from xlinkutils.Xlink_Utils import get_device_list
from xlinkutils.xlog import XLog

global false, true
false = False
true = True


class Device:

    def __init__(self):
        """设备管理类属性"""
        self.baud_rate = 0
        self.time_out = 0
        self.comm = ''
        self.serialFd = None
        self.local_statue = 0
        self.server_statue = 0
        self.mac = None
        self.device_id = 0
        self.pid = ''
        self.p_key = ''
        self.sn = ''
        self.version = None
        self.local_time = None
        self.enable_couple_statue = None
        self.enable_testing_statue = None
        self.enable_subscript_statue = None
        self.ping_code = None

    def __str__(self):
        return 'pid:' + str(self.pid) + ' p_key:' + str(self.p_key) + ' mac:' + str(self.mac)

    def get_mac(self):
        DeviceManager.get_mac(self.mac)

    def get_connect_statue(self):
        DeviceManager.get_connect_statue(self.mac)

    def get_pid_pkey(self):
        DeviceManager.get_pid_pkey(self.mac)

    def set_pid_pkey(self, pid, pkey):
        DeviceManager.set_pid_pkey(self.mac, pid, pkey)

    def set_distribute_mode(self):
        DeviceManager.set_distribute_mode(self.mac)

    def restart_wifi_module(self):
        DeviceManager.restart_wifi_module(self.mac)

    def reset_wifi_module(self):
        DeviceManager.reset_wifi_module(self.mac)

    def get_muc_version(self):
        DeviceManager.get_muc_version(self.mac)

    def get_local_time(self):
        DeviceManager.get_local_time(self.mac)

    def set_seeable_statue(self, statue):
        DeviceManager.set_seeable_statue(self.mac, statue)

    def set_ap_distribute_statue(self, statue):
        DeviceManager.set_ap_distribute_statue(self.mac, statue)

    def get_sn(self):
        DeviceManager.get_sn(self.mac)

    def set_sn(self, sn):
        DeviceManager.set_sn(self.mac, sn)

    def get_current_statue_and_signal(self):
        DeviceManager.get_current_statue_and_signal(self.mac)

    def set_testing_statue(self, *args):
        DeviceManager.set_testing_statue(self.mac, *args)

    def update_testing_data(self, *args):
        DeviceManager.update_testing_data(self.mac, *args)

    def set_testing_enable(self, statue):
        DeviceManager.set_testing_enable(self.mac, statue)

    def set_couple_enable(self, *args):
        DeviceManager.set_couple_enable(self.mac, *args)

    def set_subscribe_enable(self, *args):
        DeviceManager.set_subscribe_enable(self.mac, *args)

    def get_ping_code(self):
        DeviceManager.get_ping_code(self.mac)

    def set_ping_code(self, code):
        DeviceManager.set_ping_code(self.mac, code)

    def get_new_mission(self, *args):
        DeviceManager.get_new_mission(self.mac, *args)

    def request_download_new_mcu(self, data):
        DeviceManager.request_download_new_mcu(self.mac, data)

    def send_mcu_data(self, *args):
        DeviceManager.send_mcu_data(self.mac, *args)

    def send_data_finish(self, *args):
        DeviceManager.send_data_finish(self.mac, *args)

    def upload_update_result(self, *args):
        DeviceManager.upload_update_result(self.mac, *args)

    def set_data_point_82(self):
        DeviceManager.get_data_point_82(self.mac)

    def set_data_point_83(self, *args):
        DeviceManager.set_data_point_83(self.mac, *args)

    def set_data_point_84(self, dataponits):
        DeviceManager.set_data_point_84(self.mac, dataponits)

    def set_data_point_85(self, dataponits):
        DeviceManager.set_data_point_85(self.mac, dataponits)


class DeviceManager:
    buff = []
    device_list = []
    active_list = []
    __active = false
    __instance = None

    def __init__(self):
        """初始化事件管理器"""
        self.task_pool = None
        self.requests = None
        DeviceManager.__active = True
        # self.thread1 = Thread(target=self.receive)
        # self.thread2 = Thread(target=self.handel_packet)

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = DeviceManager()
        return cls.__instance

    def load_device_config(self, devices):
        """读取设备配置表"""
        for d in devices:
            DeviceManager.device_list.append(d)
        DeviceManager.buff = [[]] * len(self.device_list)

    def start(self, device_list):
        """获取所有串口并与配置表mac对应，赋值给serial_list"""
        self.load_device_config(device_list)
        plist = list(serial.tools.list_ports.comports())
        for i in range(len(plist)):
            com = list(plist[i])[0]
            for device in self.device_list:
                if "USB-to-Serial" in list(plist[i])[1] and device.comm == com:
                    serialFd = serial.Serial(com, device.baud_rate, timeout=device.time_out)
                    device.serialFd = serialFd
                    DeviceManager.active_list.append(device)
        self.task_pool = threadpool.ThreadPool(len(DeviceManager.device_list))
        self.requests = threadpool.makeRequests(DeviceManager.deviceHandler, DeviceManager.active_list)
        for req in self.requests:
            self.task_pool.putRequest(req)

    @staticmethod
    def getDevice(mac):
        for device in DeviceManager.device_list:
            if device.mac == mac:
                return device
        return None

    @staticmethod
    def getDevices():
        return DeviceManager.device_list

    @staticmethod
    def get_mac(mac):
        """查询MAC地址"""
        conver = Convert(0x00)
        DeviceManager.send(mac, conver)

    @staticmethod
    def get_connect_statue(mac):
        """查询连接状态"""
        conver = Convert(0x01)
        DeviceManager.send(mac, conver)

    @staticmethod
    def get_pid_pkey(mac):
        """查询pid，pkey??该指令会返回pid，pkey，同时也会返回[255, 0, 4, 1, 1, 1, 5, 254]"""
        conver = Convert(0x02)
        DeviceManager.send(mac, conver)

    @staticmethod
    def set_pid_pkey(mac, pid, pkey):
        """设置pid，pkey"""
        data = Xlink_Utils.strs_to_bytes(pid, pkey)
        conver = Convert(0x03, data)
        DeviceManager.send(mac, conver)

    @staticmethod
    def set_distribute_mode(mac):
        """设置进入配网模式"""
        conver = Convert(0x04)
        DeviceManager.send(mac, conver)

    @staticmethod
    def restart_wifi_module(mac):
        """重启wifi模组"""
        conver = Convert(0x05)
        DeviceManager.send(mac, conver)

    @staticmethod
    def reset_wifi_module(mac):
        """重设wifi模组"""
        conver = Convert(0x06)
        DeviceManager.send(mac, conver)

    @staticmethod
    def get_muc_version(mac):
        """查询固件版本"""
        conver = Convert(0x07)
        DeviceManager.send(mac, conver)

    @staticmethod
    def get_local_time(mac):
        """查询本地模糊时间"""
        conver = Convert(0x08)
        DeviceManager.send(mac, conver)

    @staticmethod
    def set_seeable_statue(mac, statue):
        """设置被发现状态"""
        data = statue
        conver = Convert(0x09, data)
        DeviceManager.send(mac, conver)

    @staticmethod
    def set_ap_distribute_statue(mac, statue):
        """设置AP配网状态"""
        data = Xlink_Utils.ints_to_bytes(statue)
        conver = Convert(0x0A, data)
        DeviceManager.send(mac, conver)

    @staticmethod
    def get_sn(mac):
        """查询SN字段"""
        conver = Convert(0x0B)
        DeviceManager.send(mac, conver)

    @staticmethod
    def set_sn(mac, sn):
        """设置sn"""
        data = Xlink_Utils.strs_to_bytes(sn)
        conver = Convert(0x0C, data)
        DeviceManager.send(mac, conver)

    @staticmethod
    def get_current_statue_and_signal(mac):
        """查询S当前状态和信号质量"""
        conver = Convert(0x0D)
        DeviceManager.send(mac, conver)

    @staticmethod
    def set_testing_statue(mac, *args):
        """设置产测模式状态??data添什么"""
        data = Xlink_Utils.ints_to_bytes(*args)
        conver = Convert(0x0E, data)
        DeviceManager.send(mac, conver)

    @staticmethod
    def update_testing_data(mac, *args):
        """更新WIFI模组自定义产测数据??data添什么"""
        data = Xlink_Utils.ints_to_bytes(*args)
        conver = Convert(0x0F, data)
        DeviceManager.send(mac, conver)

    @staticmethod
    def set_testing_enable(mac, statue):
        """产测使能设置"""
        data = Xlink_Utils.ints_to_bytes(statue)
        conver = Convert(0x10, data)
        DeviceManager.send(mac, conver)

    @staticmethod
    def set_couple_enable(mac, *args):
        """配对使能设置???data添什么"""
        data = Xlink_Utils.ints_to_bytes(*args)
        conver = Convert(0x11, data)
        DeviceManager.send(mac, conver)

    @staticmethod
    def set_subscribe_enable(mac, *args):
        """配对使能设置???data添什么"""
        data = Xlink_Utils.ints_to_bytes(*args)
        conver = Convert(0x12, data)
        DeviceManager.send(mac, conver)

    @staticmethod
    def get_ping_code(mac):
        """查询WIFI模组PINGCODE字段"""
        conver = Convert(0x13)
        DeviceManager.send(mac, conver)

    @staticmethod
    def set_ping_code(mac, code):
        """设置PINGCODE字段"""
        data = Xlink_Utils.strs_to_bytes(code)
        conver = Convert(0x14, data)
        DeviceManager.send(mac, conver)

    @staticmethod
    def get_new_mission(mac, *args):
        """MCU向WIFI模组查询是否有新任务??data是否包含int和str"""
        data = Xlink_Utils.ints_to_bytes(*args)
        conver = Convert(0x30, data)
        DeviceManager.send(mac, conver)

    @staticmethod
    def request_download_new_mcu(mac, data):
        """MCU向WIFI模组发请求下载新固件"""
        datas = Xlink_Utils.ints_to_bytes(data)
        conver = Convert(0x31, datas)
        DeviceManager.send(mac, conver)

    @staticmethod
    def send_mcu_data(mac, *args):
        """WIFI模组向MCU发送新固件数据??data是否包含int和str"""
        datas = Xlink_Utils.ints_to_bytes(*args)
        conver = Convert(0x32, datas)
        DeviceManager.send(mac, conver)

    @staticmethod
    def send_data_finish(mac, *args):
        """WIFI模组向MCU发送数据传输完成指令??data是否包含int和str"""
        datas = Xlink_Utils.ints_to_bytes(*args)
        conver = Convert(0x33, datas)
        DeviceManager.send(mac, conver)

    @staticmethod
    def upload_update_result(mac, *args):
        """MCU向WIFI模组上报更新结果??data是否包含int和str"""
        datas = Xlink_Utils.ints_to_bytes(*args)
        conver = Convert(0x34, datas)
        DeviceManager.send(mac, conver)

    @staticmethod
    def get_data_point_82(mac):
        """WIFI模组向MCU转发接收到的数据端点数据"""
        conver = Convert(0x82)
        DeviceManager.send(mac, conver)

    @staticmethod
    def set_data_point_83(mac, *args):
        """MCU向WIF模组发送数据端点数据"""
        datas = Convert.data_to_bytes(*args)
        conver = Convert(0x83, datas)
        DeviceManager.send(mac, conver)

    @staticmethod
    def set_data_point_84(mac, *args):
        """MCU向WIFI模组发送所有数据端点数据"""
        datas = Convert.data_to_bytes(*args)
        conver = Convert(0x84, datas)
        DeviceManager.send(mac, conver)

    @staticmethod
    def set_data_point_85(mac, *args):
        """MCU向WIFI发送数据端点数据"""
        datas = Convert.data_to_bytes(*args)
        conver = Convert(0x85, datas)
        DeviceManager.send(mac, conver)

    @staticmethod
    def send(mac, commands):
        """发送指令方法，通过mac遍历当前已打开的所有端口，发送指令"""
        data = []
        data.append(commands.head)
        if commands.length > 255:
            data.append(commands.length)
        else:
            data.append(0)
            data.append(commands.length)
        data.append(commands.commandId)
        data = data + commands.data
        data.append(commands.valid)
        data.append(commands.teal)
        send_command = Xlink_Utils.serial_send_packet_convert(data)

        if type(mac) == str:
            serialID = DeviceManager.getDevice(mac).serialFd
            serialID.write(send_command)
        elif type(mac) == list:
            for i in mac:
                serialID = DeviceManager.getDevice(i).serialFd
                serialID.write(send_command)
        try:
            XLog.GetLogger().info('MCU->WIFI:[%s] %s', mac, Xlink_Utils.ByteToHex(send_command))
        except Exception as e:
            XLog.GetLogger().info(e)
            raise

    # def get_com(self, mac):
    #     """通过mac查找到对应串口"""
    #     for i in self.serial_list:
    #         if mac == i['mac']:
    #             return i['object']
    #     else:
    #         print('mac not in serial_list')
    @staticmethod
    def deviceHandler(device):
        """串口接收指令线程"""
        buff = []
        try:
            while DeviceManager.__active:
                n = device.serialFd.inWaiting()
                if n or len(buff) > 0:
                    # 接收
                    recv_data = device.serialFd.read(n)
                    # if recv_data[-1] != 0x7e and recv_data[-1] != 0x7d and recv_data[-1] != 0x7f:
                    #     recv_data = Xlink_Utils.derial_recv_packe_convert(bytearray(recv_data))
                    buff += recv_data
                    XLog.GetLogger().info('WIFI->MCU :[%s] %s', device.mac, Xlink_Utils.ByteToHex(recv_data))
                    # 解析
                    if buff != [] and (buff[-1] != 0x7e) and (buff[-1] != 0x7d) and (buff[-1] != 0x7f):
                        # 转义
                        buff = Xlink_Utils.derial_recv_packe_convert(buff)
                        if len(buff) >= 5:
                            if buff[0] == 0xff:
                                length = int.from_bytes(buff[1:3], byteorder='big')
                                if len(buff) >= length + 4:
                                    data = buff[0:length + 4]
                                    if buff[length + 3] != 0xfe:
                                        XLog.GetLogger().warning('解析错误2' + Xlink_Utils.ByteToHex(buff))
                                    del buff[0:length + 4]
                                    comm = Convert.get_result_data(data)
                                    if comm:
                                        commandId, data = Convert.getCommand(comm)
                                        DeviceManager.set_device_attributes(device, data, commandId)
                                        XLog.GetLogger().debug('mac:%s commandId:%s data:%s', device.mac, commandId, data)
                                        # 发送事件
                                        try:
                                            event = Event(type_=device.mac + ':' + str(commandId))
                                            event.data['device'] = device
                                            event.data['commandId'] = commandId
                                            event.data['data'] = data
                                            EventManager.get_instance().SendEvent(event)
                                        except Exception as e:
                                            XLog.GetLogger().warning(traceback.format_exc())

                            else:
                                del buff[0]
                sleep(0.001)
            XLog.GetLogger().warning('线程退出')
        except Exception as error:
            XLog.GetLogger().warning(traceback.format_exc())

    @staticmethod
    def set_device_attributes(dev, data, commid):
        """更新Deveice类相关属性"""
        if commid == Commands.GET_MAC:
            dev.mac = data
        if commid == Commands.GET_CONNECT_STATUE:
            dev.local_statue = data[0]
            dev.server_statue = data[1]
        if commid == Commands.GET_PID_PKEY:
            dev.pid = data[0]
            dev.p_key = data[1]
        # if commid== Commands.SET_DISTRIBUTE_MODE :
        # if commid== Commands.RESTART_WIFI_MODULE :
        # if commid== Commands.RESET_WIFI_MODULE :
        if commid == Commands.GET_MUC_VERSION:
            dev.version = data
        if commid == Commands.GET_LOCAL_TIME:
            dev.local_time = data
        # if commid== Commands.SET_SEEABLE_STATUE :
        # if commid== Commands.SET_AP_DISTRIBUTE_STATUE :
        if commid == Commands.GET_SN:
            dev.sn = data
        # if commid== Commands.SET_SN :
        if commid == Commands.GET_CURRENT_STATUE_AND_SIGNAL:
            pass
        # if commid== Commands.SET_TESTING_STATUE :
        # if commid== Commands.UPDATE_TESTING_DATA :
        if commid == Commands.SET_TESTING_ENABLE:
            dev.enable_testing_statue = data
        if commid == Commands.SET_COUPLE_ENABLE:
            dev.enable_couple_statue = data
        if commid == Commands.SET_SUBSCRIBE_ENABLE:
            dev.enable_subscript_statue = data
        if commid == Commands.GET_PING_CODE:
            dev.ping_code = data
        # if commid== Commands.SET_PING_CODE :
        # if commid== Commands.GET_NEW_MISSION :
        # if commid== Commands.REQUEST_DOWNLOAD_NEW_MCU :
        # if commid== Commands.SEND_MCU_DATA :
        # if commid== Commands.SEND_DATA_FINISH :
        # if commid== Commands.UPLOAD_UPDATE_RESULT :
        # if commid== Commands.SET_DATA_POINT_82 :
        # if commid== Commands.SET_DATA_POINT_83 :
        # if commid == Commands.SET_DATA_POINT_84 :
        # if commid == Commands.SET_DATA_POINT_85 :
