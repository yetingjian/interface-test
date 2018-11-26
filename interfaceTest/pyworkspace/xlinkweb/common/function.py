# coding=utf-8
from selenium import webdriver
import logging,datetime
import os,re
import imaplib
import random,string


def scream_shot(dr, filename):
    base = find_path()
    fil = filename.split('/')[0]
    file_path = base + "/report/image/" + fil
    isexists = os.path.exists(file_path)
    if not isexists:
        os.makedirs(file_path)
    file_path = base + "/report/image/" + filename
    dr.get_screenshot_as_file(file_path)


def find_path():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    base_dir = str(base_dir)
    base_dir = base_dir.replace('\\', '/')
    base = base_dir.split('/xlinkweb')[0]
    return base + '/xlinkweb'


def log(massage):
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    path = find_path() + '/report/log/'
    isexists = os.path.exists(path)
    if not isexists:
        os.makedirs(path)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=path+'/'+now+'.log')
    logging.info(massage)


def get_now_date():
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    return now


def random_num():
    return random.randint(10000000, 99999999)


def random_string():
    return string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i',
                                      'h','g','f','e','d','c','b','a'], 8)).replace(" ","")


def get_email_unseen():
    r = imaplib.IMAP4_SSL('smtp.exmail.qq.com')
    r.login('wangqi@xlink.cn', '120211Qq')
    x, y = r.status('INBOX', '(MESSAGES UNSEEN)')
    allmes, unseenmes = re.match(r'.*\s+(\d+)\s+.*\s+(\d+)', y[0]).groups()
    return unseenmes


def set_email_seen():
    r = imaplib.IMAP4_SSL('smtp.exmail.qq.com')
    r.login('wangqi@xlink.cn', '120211Qq')
    r.list()
    r.select('inbox')
    typ, data = r.search(None, 'UNSEEN')
    for num in data[0].split():
        r.store(num, '+FLAGS', '\Seen')


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get("http://admin-test.xlink.io:1081/#/auth/login")
    scream_shot(driver, 'test1/test.jpg')
    driver.quit()
