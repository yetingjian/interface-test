import socketserver
import threading

import time

from Interface.AppManager import APP, APPManager
from Interface.DeviceManager import DeviceManager
from xlinkutils.EventManager import EventManager
from xlinkutils.xlog import XLog


class TestServices:
    def __init__(self, device_list, host='0.0.0.0', port=12366, ):
        self.device_list = device_list
        self.host = host
        self.port = port
        self.server = ThreadedTCPServer((self.host, self.port), ThreadedTCPRequestHandler)
        t = threading.Thread(target=self.start)
        t.setDaemon(True)
        t.start()
        DeviceManager.get_instance().start(self.device_list)
        EventManager.get_instance().Start()

    def start(self):
        with self.server:
            s_ip, s_port = self.server.server_address
            XLog.GetLogger().info("Server start at {0}:{1}".format(s_ip, s_port))
            self.server.serve_forever()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler):
    Serdata = ''

    def handle(self):
        ThreadedTCPRequestHandler.Serdata = self.client_address
        cur_thread = threading.current_thread()
        XLog.GetLogger().info('{0} connected，thread:{1}'.format(self.client_address, cur_thread.name))
        app = APP(self.request)
        app.last_active = int(time.time())
        app.status = True
        app.client_address = self.client_address
        APPManager.get_instance().addApp(app)
        APPManager.get_instance().handle_request(app)
