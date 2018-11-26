#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from time import sleep

def Time(self):
    sleep(15)
    # if(self.assertIsNotNone(self.driver.find_element('id', 'com.ge.cbyge:id/id_4'))):
    #     for i in range(0, 3):
    #         sleep(10)
    #         print i
    #     print u"网络连接超时失败"
    # else:
    #     print u"网络连接正常"
    try:
        # 循环判断3次后，如果失败则提示连接网络失败
        for i in range(0, 3):
            self.assertIsNotNone(self.driver.find_element('id', 'com.ge.cbyge:id/id_4'))
            sleep(10)
            # print i
        print u"网络连接超时失败"
        # exit()
    except:
        print u"网络连接正常"
