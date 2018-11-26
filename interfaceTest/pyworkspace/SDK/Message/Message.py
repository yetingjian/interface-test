#coding=utf8


class Message(object):

    def __init__(self, msg_id, callback, create_time, timeout=180):
        self.__msg_id = msg_id
        self.__callback = callback
        self.__create_time = create_time
        self.__timeout = timeout

    @property
    def msg_id(self):
        return self.__msg_id

    @property
    def callback(self):
        return self.__callback

    @property
    def create_time(self):
        return self.__create_time

    @property
    def timeout(self):
        return self.__timeout