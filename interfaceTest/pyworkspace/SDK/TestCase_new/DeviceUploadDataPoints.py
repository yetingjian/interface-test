import threading
from time import sleep

import sys

from Interface.Commands import Commands
from Interface.DeviceDataConvert import Convert
from Interface.DataPoint import DataPoint
from Interface.DeviceManager import DeviceManager
from Interface.Notification import Notification
# from Interface.SerialPacket import DeviceManager, DataPoint, Commands, Convert
from ParametrizedTestCase import ParametrizedTestCase
from xlinkutils.EventManager import EventManager
from xlinkutils.xlog import XLog


class DeviceUploadDataPoints(ParametrizedTestCase):

    def __init__(self, methodName='runTest', param=None):
        super().__init__(methodName, param)
        self.app = self.param['app']
        self.device = DeviceManager.get_instance().active_list
        self.event_obj = threading.Event()
        self.event_app = threading.Event()

    def setUp(self):
        self.result = []
        self.data_point_update = dict.fromkeys([dev.mac for dev in self.device], [])
        for dev in self.device:
            EventManager.get_instance().AddEvent(dev.mac, Commands.SET_DATA_POINT_83, self.upDataDp)
        EventManager.get_instance().AddEvent(self.app.client_id, Notification.DATAPOINT_UPDATE,
                                             self.datapoint_notification)
        self.app.sync_devices_list()

    def tearDown(self):
        for dev in self.device:
            EventManager.get_instance().RemoveEvent(dev.mac, Commands.SET_DATA_POINT_83, self.upDataDp)
        EventManager.get_instance().RemoveEvent(self.app.client_id, Notification.DATAPOINT_UPDATE,
                                                self.datapoint_notification)

    def upDataDp(self, event):
        XLog.GetLogger().info('设置数据端点回复 %s', event.data['data'])
        self.result.append(event.data['data'])
        if [2] in self.result:
            self.event_obj.set()

    def datapoint_notification(self, event):
        XLog.GetLogger().info('数据端点更新的通知 %s', event.data['notify_content'])
        mac, point_result = Convert.data_points_convert_from_notification(event.data['notify_content'])

        self.data_point_update[mac].append(point_result)
        # self.event_app.set()

    # def test_bool_normal(self):
    #     """设备上报布尔类型数据端点true"""
    #     XLog.GetLogger().info('start case:' + sys._getframe().f_code.co_name)
    #     data = self.param['device_datapoints']['bool_normal_true']
    #     dp = DataPoint(int(data['索引']), int(data['数据类型']), int(data['值']))
    #     for dev in self.device:
    #         XLog.GetLogger().info('result %s', self.result)
    #         dev.set_data_point_83(dp)
    #         self.event_obj.wait(10)
    #         self.assertIn([2], self.result)
    #         self.app.sync_devices_list()
    #         ret = self.app.probe_device_datapoint([int(data['索引'])], dev.mac, dev.pid, timeout=30)
    #         XLog.GetLogger().info('test_bool_normal %s', ret[1])
    #         point_result = Convert.data_points_convert_from_search_result(ret[1])
    #         self.assertTrue([dp] == point_result,
    #                         'app未收到设备上报的数据端点的数据端点\r\n设备上报数据端点为：' + str([dp]) + '\r\napp收到的数据为：' + str(point_result))

    def test_bool_normal1(self):
        """设备上报布尔类型数据端点true"""
        XLog.GetLogger().info('start case:' + sys._getframe().f_code.co_name)
        data = self.param['device_datapoints']['bool_normal_true']
        dp = DataPoint(int(data['索引']), int(data['数据类型']), int(data['值']))
        for dev in self.device:
            XLog.GetLogger().info('result %s', self.result)
            dev.set_data_point_83(dp)
            self.event_obj.wait(10)
            self.assertIn([2], self.result)
            sleep(5)
            self.assertNotIn([dp], self.data_point_update[dev.mac], 'app未收到设备上报的数据端点的数据端点')
            # self.event_app.wait(10)
            # self.assertTrue([dp] == point_result,
            #                 'app未收到设备上报的数据端点的数据端点\r\n设备上报数据端点为：' + str([dp]) + '\r\napp收到的数据为：' + str(point_result))
