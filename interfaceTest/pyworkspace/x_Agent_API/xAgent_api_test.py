# coding=utf-8

import unittest
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
from common import function
from HTMLTestRunner import HTMLTestRunner
import time


def send_mail(file_new):
    username = 'wangqi@xlink.cn'
    password = '120211Qq'
    sender = username
    receivers = ','.join(['wangqi@xlink.cn'])
    f = open(file_new, 'rb')
    mail_body = f.read()
    f.close()

    msg = MIMEMultipart()
    msg['Subject'] = u'自动化测试报告'
    msg['From'] = sender
    msg['To'] = receivers

    puretext = MIMEText(mail_body, 'html', 'utf-8')
    msg.attach(puretext)

    att = MIMEApplication(open(file_new, 'rb').read())
    att.add_header('Content-Disposition', 'attachment', filename='xlink_report.html')
    msg.attach(att)

    smtp = smtplib.SMTP()
    smtp.connect('smtp.exmail.qq.com')
    smtp.login(username, password)
    smtp.sendmail(sender, receivers, msg.as_string())
    time.sleep(2)
    smtp.quit()


def new_report(testreport):
    lists = os.listdir(testreport)
    lists.sort(key=lambda fn: os.path.getatime(testreport + '\\' + fn))
    file_new = os.path.join(testreport, lists[-1])
    return file_new


if __name__ == '__main__':
    base_path = function.find_path()
    now = time.strftime("%Y-%m-%d.%H.%M.%S")
    filename = base_path + '/report/' + now + 'result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp, title='X-Agent_test_report', description='X-Agent_API_test')
    discover = unittest.defaultTestLoader.discover(base_path + '/case/', pattern='*_test.py')
    function.log(u'------------------------------------用例开始执行----------------------------------')
    runner.run(discover)
    function.log(u'------------------------------------用例执行结束----------------------------------')
    fp.close()
    file_path = new_report(base_path + '/report/')
    try:
        send_mail(file_path)
    except Exception as msg:
        print(msg.message)

