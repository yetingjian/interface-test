# coding=utf-8
from selenium import webdriver
import logging,datetime
import os,time,re
import imaplib
import random,string
from HTMLTestRunner import HTMLTestRunner
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib



def find_path():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    base_dir = str(base_dir)
    base_dir = base_dir.replace('\\', '/')
    base = base_dir.split('/deployment')[0]
    return base + '/deployment'


def log(massage):
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    path = find_path() + '/log/'
    isexists = os.path.exists(path)
    if not isexists:
        os.makedirs(path)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=path+'/'+now+'.log')
    logging.info(massage)


def get_now_date():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    return str(year) + str(month) + str(day)


def random_num():
    return random.randint(10000000, 99999999)


def random_string():
    return string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i',
                                      'h','g','f','e','d','c','b','a','1','2','3','4','5','6','7','8','9'], 10)).replace(" ","")


def random_string_mac():
    return string.join(random.sample(['d','c','b','a','1','2','3','4','5','6','7','8','9'], 6)).replace(" ","")


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


def get_email_unseen(account, password):
    r = imaplib.IMAP4_SSL('smtp.exmail.qq.com')
    r.login(account, password)
    x, y = r.status('INBOX', '(MESSAGES UNSEEN)')
    allmes, unseenmes = re.match(r'.*\s+(\d+)\s+.*\s+(\d+)', y[0]).groups()
    return unseenmes


def set_email_seen(account, password):
    r = imaplib.IMAP4_SSL('smtp.exmail.qq.com')
    r.login(account, password)
    r.list()
    r.select('inbox')
    typ, data = r.search(None, 'UNSEEN')
    for num in data[0].split():
        r.store(num, '+FLAGS', '\Seen')


def get_code(result):
    s = result.find('code=')
    e = len(result)
    return result[s + 5:e-2]


def get_code_google_home(result):
    s = result.find('code=')
    e = result.find('&state=')
    return result[s + 5:e]




