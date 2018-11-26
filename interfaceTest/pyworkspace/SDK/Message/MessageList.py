#coding=utf8
import time
import threading
#import Message
from Message import Message

class MessageList(object):

    def __init__(self):
        self._messages = []
        self.timecnt = 0
        self.isend = False
        self.lock = threading.Lock()

    def get_queue_length(self):
        return len(self._messages)

    def put(self, msg_id, callback, timeout=60):
        create_time = time.time()
        message = Message.Message(msg_id, callback, create_time, timeout)
        self.lock.acquire()
        self._messages.append(message)
        self.lock.release()
        return 0

    def get_by_message_id(self, msg_id):
        if self.get_queue_length() <= 0:
            # print ('self.get_queue_length() <= 0:')
            return None
        for message in self._messages:
            # print('message.msg_id', message.msg_id)
            # print('msg_id', msg_id)
            if message.msg_id == msg_id:
                self.lock.acquire()
                self._messages.remove(message)
                self.lock.release()
                return message
        return None

    def endprocess(self):
        self.isend = True

    def process(self):
        while True:
            if self.isend:
                break
            time.sleep(1)
            now = time.time()
            # if int(now) % 5 == 0:
            #     print('MessageList process', now)
            if self.get_queue_length() <= 0:
                # print('MessageList empty')
                continue
            for message in self._messages:
                if message.timeout == 0:
                    print('MessageList process no timeout')
                if message.create_time + message.timeout < now:
                    print('message.create_time + message.timeout:{0} now：{1}'.format(message.create_time + message.timeout, now))
                    print('MessageList process message.remove, msg_id:{0}'.format(message.msg_id))
                    self.lock.acquire()
                    self._messages.remove(message)
                    self.lock.release()

    def clear_process(self):
        for message in self._messages:
            self.lock.acquire()
            self._messages.remove(message)
            self.lock.release()

