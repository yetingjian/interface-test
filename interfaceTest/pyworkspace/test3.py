#-*- coding=utf-8

import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
import time


def send_report():
    file_new = 'C:\\wq\\APItest\\output\\result.html'
    username = 'wangqi@xlink.cn'
    password = '120211Qq'
    sender = username
    receivers = ','.join(['wangqi@xlink.cn'])
    f = open(file_new, 'rb')
    mail_body = f.read()
    f.close()

    msg = MIMEMultipart()
    msg['Subject'] = u'接口自动化测试报告'
    msg['From'] = sender
    msg['To'] = receivers

    text = MIMEText(u"<p>详细内容请查看附件</p>", 'html', 'GB2312')
    puretext = MIMEText(mail_body, 'html', 'GB2312')
    msg.attach(text)
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


def get_result():
    os.system("cmd /c rd /s/q C:\\wq\\APItest\\output")
    os.chdir("C:/apache-jmeter-3.1/bin")
    os.system("jmeter -n -t C:\\wq\\APItest\\AVS.jmx -l C:\\wq\\APItest\\output\\result.jtl")
    os.chdir("C:/apache-jmeter-3.1/extras")
    os.system("ant -Dtest=result -Dtestpath=C:\wq\APItest\output")


if __name__ == '__main__':
    get_result()
    send_report()
