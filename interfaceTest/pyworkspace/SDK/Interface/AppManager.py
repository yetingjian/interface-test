import queue
import time
import traceback
from threading import Thread
import os
from Interface import InterfaceSocketPacket
from Interface.InterfaceSocketRecv import InterfaceSocketRecv
from Interface.InterfaceSocketSend import InterfaceSocketSend
from Message import MessageList
from xlinkutils import Xlink_Utils
from xlinkutils.AsyncHelper import AsyncHelper
from xlinkutils.Xlink_Utils import find_path
from xlinkutils.xlog import XLog
from xlinkutils.EventManager import Event, EventManager
from Interface.AppEvent import AppEvent

global false, true
false = False
true = True


class APP:
    class ConnSt:
        def __init__(self, request=None):
            self.request = request
            self.queue = queue.Queue()
            self.messageList = MessageList.MessageList()

    def __init__(self, conn):
        self.client_id = 0
        self.conn = APP.ConnSt(conn)
        self.userName = ''
        self.password = ''
        self.status = None
        self.recv_data = None
        self.device_model = ''
        self.device_name = ''
        self.device_current_timestamp = 0
        self.system_version = None
        self.network_status = ''
        self.message_id = None
        self.client_address = None
        self.api_server = 'https://api2.xlink.cn:443'
        self.cloud_server = 'mqtt.xlink.cn'
        self.cloud_server_port = 1884
        self.keepalive_interval = 60
        self.ssl = true
        self.support_version_flag = 1
        self.corp_id = ''
        self.last_active = None

    def disConnect(self):
        async = AsyncHelper(self.conn.messageList)
        async.request = InterfaceSocketSend.disconnect(self.conn.request, async.message_id)
        XLog.GetLogger().info('msg_id:{0}, method:{1}'.format(async.message_id, async))
        return async.   getResult()

    def isDisConnected(self):
        return (not self.status) or ((self.status != false) and (self.last_active + 30 <= int(time.time())))

    def start_sdk(self):
        async = AsyncHelper(self.conn.messageList)
        async.request = InterfaceSocketSend.start_sdk(self.conn.request, async.message_id, self.api_server,
                                                      self.cloud_server,
                                                      self.cloud_server_port, self.keepalive_interval, self.ssl, 3)
        XLog.GetLogger().info('msg_id:{0}, method:{1}'.format(async.message_id, async))
        return async.getResult()

    def stop_sdk(self):
        async = AsyncHelper(self.conn.messageList)
        async.request = InterfaceSocketSend.stop_sdk(self.conn.request, async.message_id)
        return async.getResult()

    def logout_and_stop_sdk(self):
        async = AsyncHelper(self.conn.messageList)
        async.request = InterfaceSocketSend.logout_and_stop_sdk(self.conn.request, async.message_id)
        return async.getResult()

    def user_auth(self, timeout=30):
        async = AsyncHelper(self.conn.messageList)
        async.request = InterfaceSocketSend.user_auth(self.conn.request, async.message_id, self.corp_id, self.userName,
                                                      self.password, timeout)
        return async.getResult(timeout + 5)

    def third_party_user_auth(self, open_id, access_token, source, nick_name, timeout=30):
        async = AsyncHelper(self.conn.messageList)
        async.request = InterfaceSocketSend.third_party_user_auth(self.conn.request, async.message_id, self.corp_id,
                                                                  open_id, access_token, source, nick_name,
                                                                  timeout=timeout)
        return async.getResult(timeout + 5)

    def scan_devices(self, product_ids, timeout=30):
        async = AsyncHelper(self.conn.messageList)
        async.request = InterfaceSocketSend.scan_devices(self.conn.request, async.message_id, product_ids,
                                                         timeout=timeout)
        return async.getResult(timeout + 5)

    def add_device(self, mac, product_id, timeout=30):
        async = AsyncHelper(self.conn.messageList)
        async.request = InterfaceSocketSend.add_device(self.conn.request, async.message_id, mac, product_id,
                                                       timeout=timeout)
        return async.getResult(timeout + 5)

    def delete_device(self, device_id, timeout=30):
        async = AsyncHelper(self.conn.messageList)
        async.request = InterfaceSocketSend.delete_device(self.conn.request, async.message_id, device_id,
                                                          timeout=timeout)
        return async.getResult(timeout + 5)

    def sync_devices_list(self, timeout=30):
        async = AsyncHelper(self.conn.messageList)
        async.request = InterfaceSocketSend.sync_devices_list(self.conn.request, async.message_id, timeout=timeout)
        return async.getResult(timeout + 5)

    def get_device_datapoint(self, mac, product_id, timeout=30):
        async = AsyncHelper(self.conn.messageList)
        async.request = InterfaceSocketSend.get_device_datapoint(self.conn.request, async.message_id, mac, product_id,
                                                                 timeout=timeout)
        return async.getResult(timeout + 5)

    def set_device_datapoint(self, datapoints, mac, product_id, timeout=30):
        async = AsyncHelper(self.conn.messageList)
        async.request = async.request = InterfaceSocketSend.set_device_datapoint(self.conn.request, async.message_id,
                                                                                 datapoints, mac, product_id,
                                                                                 timeout=timeout)
        return async.getResult(timeout + 5)

    def probe_device_datapoint(self, indexes, mac, product_id, timeout=30):
        async = AsyncHelper(self.conn.messageList)
        async.request = InterfaceSocketSend.probe_device_datapoint(self.conn.request, async.message_id, indexes, mac,
                                                                   product_id, timeout=timeout)
        return async.getResult(timeout + 5)

    def share_device(self, mac, product_id, device_id, account, mode, authority, expire, source, timeout=30):
        async = AsyncHelper(self.conn.messageList)
        async.request = InterfaceSocketSend.share_device(self.conn.request, async.message_id, mac, product_id,
                                                         device_id, account, mode,
                                                         authority=authority, expire=expire, source=source,
                                                         timeout=timeout)
        return async.getResult(timeout + 5)

    def handle_share_device(self, invite_code, handle_share_type, timeout=30):
        async = AsyncHelper(self.conn.messageList)
        async.request = InterfaceSocketSend.handle_share_device(self.conn.request, async.message_id, invite_code,
                                                                handle_share_type,
                                                                timeout=timeout)
        return async.getResult(timeout + 5)

    def sdk_notification(self, query_type):
        async = AsyncHelper(self.conn.messageList)
        async.request = InterfaceSocketSend.sdk_notification(self.conn.request, async.message_id, query_type)
        return async.getResult(5)


class APPManager:
    __instance = None
    apps = []

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = APPManager()
        return cls.__instance

    def __init__(self):
        self.apps = []
        thread2 = Thread(target=self.handle_data)
        thread2.setDaemon(True)
        thread2.start()

    @classmethod
    def addApp(cls, app):
        cls.apps.append(app)

    @classmethod
    def getApps(cls):
        return cls.apps

    @classmethod
    def getApp(cls, clientid):
        for app in cls.apps:
            if app.clientid == clientid:
                return app
        return None

    @classmethod
    def getAppByAddress(cls, address):
        for app in cls.apps:
            if app.client_address == address:
                return app
        return None

    @staticmethod
    def handle_request(app):
        """独立线程中监听app收到的数据，并讲数据放进queue队列"""
        try:
            while True:
                if app.isDisConnected():
                    XLog.GetLogger().info("All TestCase is run over~")
                    break
                data = app.conn.request.recv(4096)
                if not data:
                    closestr = 'socketclose'
                    app.conn.queue.put(closestr.encode())
                data = bytes.decode(data, encoding='utf8')
                dt = data.split('\r\n')
                XLog.GetLogger().info('APP->SERVER:' + data)
                for d in dt:
                    if d != '':
                        packet = InterfaceSocketPacket.InterfaceSocketPacket()
                        if packet.Parse(d) == 0:
                            app.conn.queue.put(d)
        except Exception:
            XLog.GetLogger().error(traceback.format_exc())
        finally:
            app.conn.request.close()

    @staticmethod
    def handle_data():
        """独立线程中监听queue队列中的数据，并调用recv_handler方发解析不同消息类型数据包"""
        while True:
            for app in APPManager.apps:
                if app.conn.queue is None:
                    return False
                if not app.conn.queue.empty():
                    try:
                        ret = AppRevcSocket.recv_handler(app.conn.request, app.conn.queue.get(),
                                                         messages=app.conn.messageList)
                        if ret > 0:
                            break
                    except Exception:
                        XLog.GetLogger().error(traceback.format_exc())


class AppRevcSocket(InterfaceSocketRecv):

    @classmethod
    def connect_handler(cls, conn, data, **kwargs):
        app = APPManager.get_instance().getAppByAddress(conn.getpeername())
        app.client_id = data.content['client_id']
        app.device_name = data.content['device_info']['device_name']
        app.device_current_timestamp = data.content['device_info']['device_current_timestamp']
        app.device_model = data.content['device_info']['device_model']
        app.system_version = data.content['device_info']['system_version']
        app.network_status = data.content['device_info']['network_status']
        app.status = True
        super(AppRevcSocket, cls).connect_handler(conn, data, **kwargs)
        try:
            event = Event(type_=AppEvent.CONNECTED)
            event.data['app'] = app
            EventManager.get_instance().SendEvent(event)
        except Exception:
            XLog.GetLogger().error(traceback.format_exc())
        # return super(AppRevcSocket, cls).connect_handler(conn, data, **kwargs)

    @classmethod
    def disconnect_handler(cls, conn, data, **kwargs):
        app = APPManager.get_instance().getAppByAddress(conn.getpeername())
        app.status = False
        return super(AppRevcSocket, cls).disconnect_handler(conn, data, **kwargs)

    @classmethod
    def ping_handler(cls, conn, data, **kwargs):
        app = APPManager.get_instance().getAppByAddress(conn.getpeername())
        app.last_active = int(time.time())
        return super(AppRevcSocket, cls).ping_handler(conn, data, **kwargs)

    @classmethod
    def get_info_handler(cls, conn, data, **kwargs):
        app = APPManager.get_instance().getAppByAddress(conn.getpeername())
        app.device_name = data.content['device_info']['device_name']
        app.device_current_timestamp = data.content['device_info']['device_current_timestamp']
        app.device_model = data.content['device_info']['device_model']
        app.system_version = data.content['device_info']['system_version']
        app.network_status = data.content['device_info']['network_status']
        return super(AppRevcSocket, cls).get_info_handler(conn, data, **kwargs)

    @classmethod
    def notification_handler(cls, conn, data, **kwargs):
        app = APPManager.get_instance().getAppByAddress(conn.getpeername())
        try:
            event = Event(type_=app.client_id + ':' + data.content['notify_type'])
            event.data['notify_content'] = data.content['notify_content']
            EventManager.get_instance().SendEvent(event)
        except Exception:
            XLog.GetLogger().error(traceback.format_exc())
        return super(AppRevcSocket, cls).notification_handler(conn, data, **kwargs)
