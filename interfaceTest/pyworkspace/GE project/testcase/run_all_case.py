# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import HTMLTestRunner
import time
import unittest
from appium import webdriver
from time import sleep
import re
sys.path.append("E:\\app-tests\\LLR-PURE\\case\\test1")
import test_03
import test_04

# def run_all_case():
#     pj = test_03
#     pj.Test_all()
#     pi = test_04
#     pi.Test_all()

if __name__ == '__main__':
    timestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    filename = "E:\\test-reports\\result_" + timestr + ".html"
    # runner = unittest.TextTestRunner()
    # runner.run(test_03.Test_all())

    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title='导游端测试结果',
        description='领路人APP导游端测试报告'
    )
    # runner.run(run_all_case())
    runner.run(test_03.Test_all())
    runner.run(test_04.Test_all())
    fp.close()
