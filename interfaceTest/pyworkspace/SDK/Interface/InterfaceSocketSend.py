# -*- coding: utf-8 -*-
import json
import os
from Interface import InterfaceSocketPacket
from time import sleep
# import InterfaceSocketPacket
# from TestCase.Start_device import excel_table_byindex
import socketserver

from xlinkutils.xlog import XLog
global false, true
false = False
true = True

path_send = os.path.abspath(".\\date\\sdk_SocketSend.xlsx")


# data1 = excel_table_byindex(path_send,0)

class InterfaceSocketSend(object):

    def __init__(self, msg_type):
        self.packet = InterfaceSocketPacket.InterfaceSocketPacket(msg_type)

    @staticmethod
    def start_sdk(conn, msg_id, api_server='https://api2.xlink.cn:443', cloud_server='mqtt.xlink.cn',
                  cloud_server_port=1884, keepalive_interval=60, ssl=1,
                  support_version_flag=3):
        data_dict = {}
        data_dict['class'] = 'XLinkSDK'
        data_dict['method'] = 'start'
        params = {}
        xlink_config = {}
        xlink_config['api_server'] = api_server
        xlink_config['cloud_server'] = cloud_server
        xlink_config['cloud_server_port'] = cloud_server_port
        xlink_config['keepalive_interval'] = keepalive_interval
        xlink_config['support_version_flag'] = support_version_flag

        xlink_config['debug'] = True
        xlink_config['ssl'] = ssl
        params['XLinkConfig'] = xlink_config
        data_dict['params'] = params

        return InterfaceSocketSend.send_data_to_comm(conn, InterfaceSocketPacket.SDK_TEST_MESSAGE_TYPE, msg_id,
                                                     data_dict)

    @staticmethod
    def stop_sdk(conn, msg_id):
        data_dict = {}
        data_dict['class'] = 'XLinkSDK'
        data_dict['method'] = 'stop'
        params = {}
        data_dict['params'] = params

        return InterfaceSocketSend.send_data_to_comm(conn, InterfaceSocketPacket.SDK_TEST_MESSAGE_TYPE, msg_id,
                                                     data_dict)

    @staticmethod
    def logout_and_stop_sdk(conn, msg_id):
        data_dict = {}
        data_dict['class'] = 'XLinkSDK'
        data_dict['method'] = 'logout_and_stop'
        params = {}
        data_dict['params'] = params

        return InterfaceSocketSend.send_data_to_comm(conn, InterfaceSocketPacket.SDK_TEST_MESSAGE_TYPE, msg_id,
                                                     data_dict)

    @staticmethod
    def user_auth(conn, msg_id, corp_id, account, password, timeout=30):
        packet = InterfaceSocketSend(InterfaceSocketPacket.SDK_TEST_MESSAGE_TYPE)
        data_dict = {}
        data_dict['class'] = 'XLinkUserAuthorizeTask'
        data_dict['method'] = 'start'
        params = {}
        params['corp_id'] = corp_id
        params['account'] = account
        params['password'] = password
        params['timeout'] = timeout
        data_dict['params'] = params

        return InterfaceSocketSend.send_data_to_comm(conn, InterfaceSocketPacket.SDK_TEST_MESSAGE_TYPE, msg_id,
                                                     data_dict)

    @staticmethod
    def third_party_user_auth(conn, msg_id, corp_id, open_id, access_token, source, nick_name, timeout=10):
        data_dict = {}
        data_dict['class'] = 'XLinkThirdPartyAuthorizeTask'
        data_dict['method'] = 'start'
        params = {}
        params['corp_id'] = corp_id
        params['open_id'] = open_id
        params['access_token'] = access_token
        params['source'] = source
        params['nick_name'] = nick_name
        params['timeout'] = timeout
        data_dict['params'] = params

        return InterfaceSocketSend.send_data_to_comm(conn, InterfaceSocketPacket.SDK_TEST_MESSAGE_TYPE, msg_id,
                                                     data_dict)

    @staticmethod
    def scan_devices(conn, msg_id, product_ids, timeout=10):
        data_dict = {}
        data_dict['class'] = 'XLinkScanDeviceTask'
        data_dict['method'] = 'start'
        params = {}
        params['product_ids'] = product_ids
        params['timeout'] = timeout
        data_dict['params'] = params

        return InterfaceSocketSend.send_data_to_comm(conn, InterfaceSocketPacket.SDK_TEST_MESSAGE_TYPE, msg_id,
                                                     data_dict)

    @staticmethod
    def add_device(conn, msg_id, mac='', product_id='', timeout=10):
        data_dict = {}
        data_dict['class'] = 'XLinkAddDeviceTask'
        data_dict['method'] = 'start'
        params = {}
        XDevice = {}
        XDevice['mac'] = mac
        XDevice['product_id'] = product_id
        params['XDevice'] = XDevice
        params['timeout'] = timeout
        data_dict['params'] = params

        return InterfaceSocketSend.send_data_to_comm(conn, InterfaceSocketPacket.SDK_TEST_MESSAGE_TYPE, msg_id,
                                                     data_dict)

    @staticmethod
    def delete_device(conn, msg_id, device_id, timeout=10):
        data_dict = {}
        data_dict['class'] = 'XLinkRemoveDeviceTask'
        data_dict['method'] = 'start'
        params = {}
        XDevice = {}
        XDevice['id'] = device_id
        params['XDevice'] = XDevice
        params['timeout'] = timeout
        data_dict['params'] = params

        return InterfaceSocketSend.send_data_to_comm(conn, InterfaceSocketPacket.SDK_TEST_MESSAGE_TYPE, msg_id,
                                                     data_dict)

    @staticmethod
    def sync_devices_list(conn, msg_id, timeout=10):
        data_dict = {}
        data_dict['class'] = 'XLinkSyncDeviceListTask'
        data_dict['method'] = 'start'
        params = {}
        params['timeout'] = timeout
        data_dict['params'] = params

        return InterfaceSocketSend.send_data_to_comm(conn, InterfaceSocketPacket.SDK_TEST_MESSAGE_TYPE, msg_id,
                                                     data_dict)

    @staticmethod
    def get_device_datapoint(conn, msg_id, mac='', product_id='', timeout=10):
        data_dict = {}
        data_dict['class'] = 'XLinkGetDataPointTask'
        data_dict['method'] = 'start'
        params = {}
        XDevice = {}
        XDevice['mac'] = mac
        XDevice['product_id'] = product_id
        params['XDevice'] = XDevice
        params['timeout'] = timeout
        data_dict['params'] = params

        return InterfaceSocketSend.send_data_to_comm(conn, InterfaceSocketPacket.SDK_TEST_MESSAGE_TYPE, msg_id,
                                                     data_dict)

    @staticmethod
    def set_device_datapoint(conn, msg_id, datapoints, mac='', product_id='', timeout=10):
        data_dict = {}
        data_dict['class'] = 'XLinkSetDataPointTask'
        data_dict['method'] = 'start'
        params = {}
        XDevice = {}
        XDevice['mac'] = mac
        XDevice['product_id'] = product_id
        params['XDevice'] = XDevice
        if type(datapoints) != list:
            params['datapoints'] = [datapoints.__dict__]
        else:
            datapoints_list = []
            for i in datapoints:
                datapoints_list.append(i.__dict__)
            params['datapoints'] = datapoints_list
        params['timeout'] = timeout
        data_dict['params'] = params

        return InterfaceSocketSend.send_data_to_comm(conn, InterfaceSocketPacket.SDK_TEST_MESSAGE_TYPE, msg_id,
                                                     data_dict)

    @staticmethod
    def probe_device_datapoint(conn, msg_id, indexes, mac='', product_id='', timeout=10):
        data_dict = {}
        data_dict['class'] = 'XLinkProbeDataPointTask'
        data_dict['method'] = 'start'
        params = {}
        XDevice = {}
        XDevice['mac'] = mac
        XDevice['product_id'] = product_id

        params['XDevice'] = XDevice
        params['index'] = indexes
        params['timeout'] = timeout
        data_dict['params'] = params

        return InterfaceSocketSend.send_data_to_comm(conn, InterfaceSocketPacket.SDK_TEST_MESSAGE_TYPE, msg_id,
                                                     data_dict)

    @staticmethod
    def share_device(conn, msg_id, mac, product_id, device_id, account, mode, authority='RW', expire=7200, source='',
                     timeout=10):
        data_dict = {}
        data_dict['class'] = 'XLinkShareDeviceTask'
        data_dict['method'] = 'start'
        params = {}
        XDevice = {}
        XDevice['mac'] = mac
        XDevice['product_id'] = product_id
        XDevice['id'] = device_id
        params['XDevice'] = XDevice
        params['account'] = account
        if source != '':
            params['source'] = source
        params['expire'] = expire
        params['mode'] = mode
        params['authority'] = authority
        params['timeout'] = timeout

        data_dict['params'] = params

        return InterfaceSocketSend.send_data_to_comm(conn, InterfaceSocketPacket.SDK_TEST_MESSAGE_TYPE, msg_id,
                                                     data_dict)

    @staticmethod
    def handle_share_device(conn, msg_id, invite_code, handle_share_type, timeout=10):
        data_dict = {}
        data_dict['class'] = 'XLinkHandleShareDeviceTask'
        data_dict['method'] = 'start'
        params = {}
        params['invite_code'] = invite_code
        params['handle_share_type'] = handle_share_type
        params['timeout'] = timeout

        data_dict['params'] = params

        return InterfaceSocketSend.send_data_to_comm(conn, InterfaceSocketPacket.SDK_TEST_MESSAGE_TYPE, msg_id,
                                                     data_dict)

    @staticmethod
    def sdk_notification(conn, msg_id, query_type):
        params = {}
        params['offset'] = 0
        params['limit'] = 100
        params['query_type'] = query_type
        params['clear_cache'] = false
        return InterfaceSocketSend.send_data_to_comm(conn, InterfaceSocketPacket.GET_NOTIFICATION_MESSAGE, msg_id,
                                                     params)

    @staticmethod
    def ping_resp(conn, msg_id):
        packet = InterfaceSocketSend(InterfaceSocketPacket.PING_MESSAGE_TYPE)
        data_dict = {}
        packet.packet.direction = 'response'
        packet.packet.msg_id = msg_id
        packet.packet.content = data_dict
        data = packet.packet.Build()
        conn.send(data)

    @staticmethod
    def disconnect(conn, msg_id):
        packet = InterfaceSocketSend(InterfaceSocketPacket.DISCONNECT_MESSAGE_TYPE)
        data_dict = {}
        packet.packet.direction = 'request'
        packet.packet.msg_id = msg_id
        packet.packet.content = data_dict
        data = packet.packet.Build()
        conn.send(data)

    @staticmethod
    def disconnect_resp(conn, msg_id):
        packet = InterfaceSocketSend(InterfaceSocketPacket.DISCONNECT_MESSAGE_TYPE)
        data_dict = {}
        packet.packet.direction = 'response'
        packet.packet.msg_id = msg_id
        packet.packet.content = data_dict
        data = packet.packet.Build()
        conn.send(data)

    @staticmethod
    def get_info(conn, msg_id):
        packet = InterfaceSocketSend(InterfaceSocketPacket.GET_INFO_MESSAGE_TYPE)
        data_dict = {}
        packet.packet.direction = 'request'
        packet.packet.msg_id = msg_id
        packet.packet.content = data_dict
        data = packet.packet.Build()
        conn.send(data)

    @staticmethod
    def connect_resp(conn, msg_id):
        packet = InterfaceSocketSend(InterfaceSocketPacket.CONNECT_MESSAGE_TYPE)
        data_dict = {}
        packet.packet.direction = 'response'
        packet.packet.msg_id = msg_id
        packet.packet.content = data_dict
        data = packet.packet.Build()
        XLog.GetLogger().info('data:{0}'.format(data))
        conn.send(data)

    #
    @staticmethod
    def send_data_to_comm(conn, msg_type, msg_id, content):
        packet = InterfaceSocketSend(msg_type)
        packet.packet.direction = 'request'
        packet.packet.msg_id = msg_id
        packet.packet.content = content
        data = packet.packet.Build()
        conn.send(data)
        XLog.GetLogger().info('SERVER->APP:{0}'.format(data))
        return data
