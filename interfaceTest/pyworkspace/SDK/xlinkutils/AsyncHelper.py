import asyncio
import threading

from Interface.InterfaceSocketPacket import InterfaceSocketPacket
from xlinkutils.xlog import XLog
from time import sleep


# async def asyncFun(future):
#     XLog.GetLogger().info('1')
#     XLog.GetLogger().info('future:{0}'.format(future))
#     return await future
#

#
# class AsyncHelper:
#
#     def __init__(self, messages):
#         self.loop = asyncio.get_event_loop()
#         self.future = asyncio.Future(loop=self.loop)
#         XLog.GetLogger().info('future:{0}'.format(self.future))
#         self.task = asyncio.ensure_future(asyncFun(self.future))
#         # self.task = self.loop.create_task(asyncFun(self.future))
#         XLog.GetLogger().info('task:{0}'.format(self.task))
#         self.message_id = InterfaceSocketPacket.get_msg_id()
#         messages.put(self.message_id, self)
#
#     def getResult(self):
#         XLog.GetLogger().info('22')
#         XLog.GetLogger().info('task:{0}'.format(self.task))
#         sleep(5)
#         self.loop.run_until_complete(self.task)
#         XLog.GetLogger().info('2')
#         return self.future.result()
#
#     def setResult(self, data):
#         XLog.GetLogger().info('3')
#         self.future.set_result(data)
#         XLog.GetLogger().info('4')


# class AsyncHelper:
#
#     def __init__(self, messages):
#         self.message_id = InterfaceSocketPacket.get_msg_id()
#         self.result = None
#         messages.put(self.message_id, self)
#
#     def getResult(self, timeout=10):
#         wait = 0
#         while self.result is None and wait < timeout * 1000:
#             sleep(0.001)
#             wait = wait + 1
#         return self.result
#
#     def setResult(self, data):
#         self.result = data

class AsyncHelper:

    def __init__(self, messages):
        self.event_obj = threading.Event()
        self.message_id = InterfaceSocketPacket.get_msg_id()
        self.result = None
        self.request = None
        messages.put(self.message_id, self)

    def getResult(self, timeout=15):
        """监听回调结果，超时时间15秒，返回接口请求数据和返回结果数据"""
        self.event_obj.wait(timeout)
        return self.request, self.result

    def setResult(self, data):
        """接收到回调后把返回结果赋值给result，线程解锁"""
        self.result = data
        self.event_obj.set()
