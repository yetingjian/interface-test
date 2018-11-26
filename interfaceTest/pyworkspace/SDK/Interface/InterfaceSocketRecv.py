# coding=utf8
import os
# from TestCase.Start_device import excel_table_byindex
from Interface import InterfaceSocketPacket
from Interface import InterfaceSocketSend
# import InterfaceSocketPacket
# import InterfaceSocketSend
from xlinkutils.xlog import XLog

path_sdkuser = os.path.abspath(".\\date\\sdk_user.xlsx")
# data3 = excel_table_byindex(path_sdkuser,0)
from xlinkutils.AsyncHelper import AsyncHelper


class InterfaceSocketRecv(object):
    last_str = ''
    last_flag = False

    def __init__(self):
        pass

    @classmethod
    def user_auth_resp(cls, conn, data, **kwargs):
        print(data)

    @classmethod
    def start_sdk_resp(cls, conn, data, **kwargs):
        messages = kwargs['messages']
        message_id = InterfaceSocketPacket.InterfaceSocketPacket.get_msg_id()
        messages.put(message_id, cls.user_auth_resp)
        # InterfaceSocketSend.InterfaceSocketSend.user_auth(conn, message_id, '1234567890', 'Kaven@xlink.cn', '123456')
        # InterfaceSocketSend.InterfaceSocketSend.user_auth(conn, message_id, str(data3[0][u"企业id"]), str(data3[0][u"用户账号"]),str(data3[0][u"用户密码"]))
        return data

    @classmethod
    def connect_handler(cls, conn, data, **kwargs):
        XLog.GetLogger().info("connect_handler")
        InterfaceSocketSend.InterfaceSocketSend.connect_resp(conn, data.msg_id)
        return 0

    @classmethod
    def disconnect_handler(cls, conn, data, **kwargs):
        XLog.GetLogger().info('disconnect_handler')
        InterfaceSocketSend.InterfaceSocketSend.disconnect_resp(conn, data.msg_id)
        return 0

    @classmethod
    def get_info_handler(cls, conn, data, **kwargs):
        XLog.GetLogger().info('get_info_handler')

        return 0

    @classmethod
    def ping_handler(cls, conn, data, **kwargs):
        XLog.GetLogger().info('ping_handler')
        InterfaceSocketSend.InterfaceSocketSend.ping_resp(conn, data.msg_id)
        return 0

    @classmethod
    def notification_handler(cls, conn, data, **kwargs):
        XLog.GetLogger().info('base notification_handler')
        return 0

    @classmethod
    def get_notification_handler(cls, conn, data, **kwargs):
        XLog.GetLogger().info('base notification_handler')
        messages = kwargs['messages']
        message = messages.get_by_message_id(data.msg_id)
        if message is None:
            return -1
        ret = 0
        # XLog.GetLogger().debug('msg_id:{0}, data:{1}'.format(message.msg_id, data.content))
        if message.callback is not None:
            if isinstance(message.callback, AsyncHelper):
                async = message.callback
                async.setResult(data.content)
            else:
                ret = message.callback(conn, data, **kwargs)
                XLog.GetLogger().info('callback')
        # print data
        return ret

    @classmethod
    def msg_test_handler(cls, conn, data, **kwargs):
        XLog.GetLogger().info('msg_test_handler')
        messages = kwargs['messages']
        message = messages.get_by_message_id(data.msg_id)
        if message is None:
            return -1
        ret = 0
        # XLog.GetLogger().debug('msg_id:{0}, data:{1}'.format(message.msg_id, data.content))
        if message.callback is not None:
            if isinstance(message.callback, AsyncHelper):
                async = message.callback
                async.setResult(data.content)
            else:
                ret = message.callback(conn, data, **kwargs)
                XLog.GetLogger().info('callback')
        # print data
        return ret

    @classmethod
    def recv_handler(cls, conn, data, **kwargs):
        if len(data) <= 0:
            return -1
        if data == b'socketclose':
            return 3
        packet = InterfaceSocketPacket.InterfaceSocketPacket()
        if packet.Parse(data) != 0:
            # print 'packet.Parse(d) != 0'
            XLog.GetLogger().info("packet.Parse(d) != 0")
            cls.last_str = data
            cls.last_flag = True

        method_mapped = {
            InterfaceSocketPacket.CONNECT_MESSAGE_TYPE: cls.connect_handler,
            InterfaceSocketPacket.DISCONNECT_MESSAGE_TYPE: cls.disconnect_handler,
            InterfaceSocketPacket.GET_INFO_MESSAGE_TYPE: cls.get_info_handler,
            InterfaceSocketPacket.PING_MESSAGE_TYPE: cls.ping_handler,
            InterfaceSocketPacket.SDK_NOTIFICATION_MESSAGE_TYPE: cls.notification_handler,
            InterfaceSocketPacket.SDK_TEST_MESSAGE_TYPE: cls.msg_test_handler,
            InterfaceSocketPacket.GET_NOTIFICATION_MESSAGE: cls.get_notification_handler,
        }

        method = method_mapped.get(packet.msg_type, None)

        if method is not None:
            # XLog.GetLogger().info("method:{0}".format(method))
            method(conn, packet, **kwargs)
            # if ret > 0:
            #     return ret
        else:
            XLog.GetLogger().debug("{0} not support".format(packet.msg_type))
            # print '{0} not support'.format(packet.msg_type)
        # return ret
        return 0
