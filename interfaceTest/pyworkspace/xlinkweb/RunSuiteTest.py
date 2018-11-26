# coding=utf-8
from test_case.a_login import z_login_test
from test_case.b_devplatform import a_create_product_test, b_product_info_test, d_regist_device_test, e_connector_test
from HTMLTestRunner import HTMLTestRunner
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from common import function
import smtplib
import unittest
import time
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


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

    pure_text = MIMEText(mail_body, 'html', 'utf-8')
    msg.attach(pure_text)

    att = MIMEApplication(open(file_new, 'rb').read())
    att.add_header('Content-Disposition', 'attachment', filename='xlink_report.html')
    msg.attach(att)

    smtp = smtplib.SMTP()
    smtp.connect('smtp.exmail.qq.com')
    smtp.login(username, password)
    smtp.sendmail(sender, receivers, msg.as_string())
    time.sleep(2)
    smtp.quit()


def new_report(test_report):
    lists = os.listdir(test_report)
    lists.sort(key=lambda fn: os.path.getatime(test_report + '\\' + fn))
    file_new = os.path.join(test_report, lists[-1])
    return file_new


if __name__ == '__main__':
    base_path = function.find_path()
    now = time.strftime("%Y-%m-%d.%H.%M.%S")
    filename = base_path + '/report/' + now + 'result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp, title='xlink_test_report', description='env:win10 broswer:Chrome')
    suite = unittest.TestSuite()
    #suite.addTest(z_login_test.LoginTest('test_z_login_success'))
    suite.addTest(e_connector_test.ConnectorTest('test_a1_create_connector_success'))
    runner.run(suite)
    fp.close()
    file_path = new_report(base_path + '/report/')
    try:
        send_mail(file_path)
    except Exception, msg:
        function.log(u'结果邮件发送失败')
        raise
