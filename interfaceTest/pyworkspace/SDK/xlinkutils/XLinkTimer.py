#coding=utf8

from threading import Thread
import time

class XLinkTimer(Thread):

    def __init__(self, interval, func=None,  func_args=(), func_kwargs=None,group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(XLinkTimer, self).__init__(group=group, target=target, name=name, args=args, kwargs=kwargs,
                                         verbose=verbose)

        if func_kwargs is None:
            func_kwargs = {}

        self.__interval = interval
        self.__start_time = 0
        self.__func = func
        self.__func_args = func_args
        self.__func_kwargs = func_kwargs


    def reload(self):
        self.__start_time = time.time()

    def run(self):
        self.__start_time = time.time()
        # print self.__start_time
        while True:
            time.sleep(0.1)
            if self.__start_time == 0:
                continue
            # print time.time(), self.__start_time + self.__interval
            if time.time() > self.__start_time + self.__interval:
                # print 'timeout'
                if self.__func:
                    self.__func(*self.__func_args, **self.__func_kwargs)
                self.__start_time = 0



if __name__ == '__main__':

    def test(var):
       pass


    xlinktimer = XLinkTimer(1, test, func_args=("test",))
    xlinktimer.setDaemon(True)
    xlinktimer.start()
    # print xlinktimer
    while True:
        time.sleep(1.6)
        xlinktimer.reload()
        # print xlinktimer