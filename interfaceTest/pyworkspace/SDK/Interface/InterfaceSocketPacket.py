# coding=utf8
import json

CONNECT_MESSAGE_TYPE = 'connect'
PING_MESSAGE_TYPE = 'ping'
GET_INFO_MESSAGE_TYPE = 'get_info'
DISCONNECT_MESSAGE_TYPE = 'disconnect'
SDK_TEST_MESSAGE_TYPE = 'sdk_test'
SDK_NOTIFICATION_MESSAGE_TYPE = 'sdk_notification'
GET_NOTIFICATION_MESSAGE = 'get_sdk_notification'


class InterfaceSocketPacket(object):
    msg_id = 1

    def __init__(self, msg_type='', msg_id='', direction='', content=''):
        self.msg_type = msg_type
        self.msg_id = msg_id
        self.direction = direction
        self.content = content

    def __unicode__(self):
        return 'msg_type:{0}, msg_id:{1}, direction:{2}, content:{3}'.format(self.msg_type, self.msg_id, self.direction,
                                                                             self.content)

    def Build(self):
        data = {}
        data['msg_type'] = self.msg_type
        data['msg_id'] = self.msg_id
        data['direction'] = self.direction
        data['content'] = self.content
        return (json.dumps(data) + '\r\n').encode()

    def Parse(self, data):
        try:
            _data = json.loads(data)
            self.msg_type = _data.get('msg_type', None)
            self.msg_id = _data.get('msg_id', None)
            self.direction = _data.get('direction', None)
            self.content = _data.get('content', None)
            return 0
        except (AttributeError, ValueError) as e:
            return -1

    @classmethod
    def get_msg_id(cls):
        cls.msg_id += 1
        if cls.msg_id == 0:
            cls.msg_id = 1
        return cls.msg_id
