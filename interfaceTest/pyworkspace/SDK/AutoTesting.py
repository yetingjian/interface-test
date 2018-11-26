import json
import socketserver
import threading
import time, os
import unittest
import HTMLTestRunner_new
# from Interface.SerialPacket import DeviceManager, Device
from Interface.DeviceManager import Device, DeviceManager
from Interface.TestServices import ThreadedTCPRequestHandler, TestServices
from ParametrizedTestCase import ParametrizedTestCase
from Interface.AppManager import AppEvent, APP, APPManager
from TestCase_new import Device_init
from TestCase_new.DeviceUploadDataPoints import DeviceUploadDataPoints
from TestCase_new.Device_init import DeviceInit
from TestCase_new.SDK_Login import Login
from TestCase_new.SDK_SetAppDataPoints import SetDataPoints
from xlinkutils.EventManager import EventManager
from xlinkutils.Xlink_Utils import find_path, load_data_points, get_user_list, load_test_excel
from xlinkutils.xlog import XLog


def appconnect(event):
    app = event.data['app']
    param['app'] = app
    connect = threading.Thread(target=addTest, args=(
    [Login, DeviceUploadDataPoints], param, '_client_id_' + str(app.client_id) + '.html'))
    connect.setDaemon(True)
    connect.start()


def addTest(clsList, param, reportName):
    print(reportName)
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = os.path.abspath(path) + "\\" + now + reportName
    # filename = './' + now + 'result.html'
    fp = open(filename, 'wb')

    runner = HTMLTestRunner_new.HTMLTestRunner(
        stream=fp,
        title=u'测试报告',
        description=u'用例的执行情况',
        server="服务器地址：" + str(ThreadedTCPRequestHandler.Serdata),
        device="设备mac : " + '',
        phone='',
    )
    suite = unittest.TestSuite()
    XLog.GetLogger().info("Start creat_suite!")
    for cls in clsList:
        suite.addTest(ParametrizedTestCase.parametrize(cls, param=param))
    XLog.GetLogger().info("creat_suite END!")
    XLog.GetLogger().info("Start run test!")
    runner.run(suite)
    XLog.GetLogger().info("run test end!")
    # app = param['app']
    # app.disConnect()


if __name__ == "__main__":
    path = ".\\logs\\"
    param = {}
    test_path = find_path() + "/date/sdk_test.xlsx"
    data_list = load_test_excel(test_path)
    param['server_config'] = data_list['server_config']
    param['datapoints'] = data_list['datapoints']
    param['user'] = data_list['user']
    param['devs'] = data_list['device']
    param['device_datapoints'] = data_list['device_datapoints']
    device_list = []
    for key in param['devs'].keys():
        device = Device()
        device.mac = param['devs'][key]['mac']
        device.time_out = int(param['devs'][key][u'超时'])
        device.comm = param['devs'][key][u'串口']
        device.baud_rate = int(param['devs'][key][u'码率'])
        device_list.append(device)
    TestServices(device_list)
    # 事件监听，当收到AppEvent.CONNECTED的时间后，执行appconnect方法
    EventManager.get_instance().AddEventListener(AppEvent.CONNECTED, appconnect)
    ##设备用例加载
    for device in DeviceManager.get_instance().device_list:
        param['device'] = device
        addTest([DeviceInit], param, device.mac + '.html')
