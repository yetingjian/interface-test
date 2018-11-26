import threading

# from Interface.SerialPacket import DeviceManager, DataPoint, Commands
from Interface.Commands import Commands
from Interface.DataPoint import DataPoint
from Interface.DeviceManager import DeviceManager
from ParametrizedTestCase import ParametrizedTestCase
from xlinkutils.EventManager import EventManager
from xlinkutils.xlog import XLog


class SetDataPoints(ParametrizedTestCase):

    def __init__(self, methodName='runTest', param=None):
        super().__init__(methodName, param)
        self.app = self.param['app']
        self.device = DeviceManager.get_instance().active_list
        self.result = []
        self.event_obj = threading.Event()

    def setUp(self):
        for dev in self.device:
            EventManager.get_instance().AddEvent(dev.mac, Commands.SET_DATA_POINT_82, self.upDataDp)

    def tearDown(self):
        for dev in self.device:
            EventManager.get_instance().RemoveEvent(dev.mac, Commands.SET_DATA_POINT_82, self.upDataDp)

    def upDataDp(self, event):
        XLog.GetLogger().info('设置数据端点回复 %s', event.data['data'])
        self.result.append(event.data['data'])
        self.event_obj.set()


    def test_00_bool_normal_true(self):
        data = self.param['datapoints']['bool_normal_true']
        self.app.sync_devices_list()
        dp = DataPoint(int(data['索引']), int(data['数据类型']), int(data['值']))
        for dev in self.device:
            ret = self.app.set_device_datapoint(dp, dev.mac, dev.pid)
            # XLog.GetLogger().info('bool_normal_true %s', ret)
            self.assertRet(ret, '数据端点布尔类型设置true失败')
            self.event_obj.wait(5)
            self.assertIn([dp], self.result)

    def test_01_bool_normal_false(self):
        data = self.param['datapoints']['bool_normal_false']
        self.app.sync_devices_list()
        dp = DataPoint(int(data['索引']), int(data['数据类型']), int(data['值']))
        for dev in self.device:
            ret = self.app.set_device_datapoint(dp, dev.mac, dev.pid)
            # XLog.GetLogger().info('bool_normal_false %s', ret)
            self.assertRet(ret, '数据端点布尔类型设置false失败')
            self.event_obj.wait(5)
            self.assertIn([dp], self.result)

    def test_02_set_datapoints(self):
        """app设置多个数据端点"""
        data = self.param['datapoints']['set_datapoints']
        dps = [DataPoint(int(x['索引']), int(x['数据类型']), int(x['值'])) for x in data]
        self.app.sync_devices_list()
        for dev in self.device:
            ret = self.app.set_device_datapoint(dps, dev.mac, dev.pid)
            XLog.GetLogger().info('bool_normal_false %s', ret[1])
            ret1 = self.app.sdk_notification(['cloud_state','datapoint_update'])
            XLog.GetLogger().info('sdk_notification %s', ret1[1])
            self.assertRet(ret, '设置多个数据端点失败')
            self.event_obj.wait(5)
            self.assertIn(dps, self.result, '设备未收到app发送的数据端点')



