# -------------------------------------------------------------------
# encoding: UTF-8
from EventManager import *

# 事件名称  新文章
EVENT_SET_DATAPONIT = "Event_SET_DATAPONIT"

eventManager = EventManager()


if __name__ == '__main__':
    eventManager.Start()


    eventManager.AddEventListener('0001',EVENT_SET_DATAPONIT, lambda event: print(event.data))
    eventManager.AddEventListener('MAC',EVENT_SET_DATAPONIT, lambda event: print('aa'+str(event.data)))

    # 事件对象，写了新文章
    event = Event(type_=EVENT_SET_DATAPONIT)
    event.data["device_id"] = 123456789
    event.data["dataponit"] = {"index": 1, "type": 1, "value": 2}

    # 发送事件
    eventManager.SendEvent(event)

