# -*- coding: utf-8 -*-
import imaplib
import re
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from selenium import webdriver

import poplib

import os


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def read_email(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            read_email(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            # print(type(content))
            # print('%sText: %s' % ('  ' * indent, content + '...'))
            path = 'C:/dep/content.txt'
            if not os.path.exists('C:/dep/'):
                os.mkdir('C:/dep/')
            if not os.path.exists(path):
                fobj = open(path, 'w')
                fobj.close()
            f = open(path, 'w')
            f.write(content)
            f.close()
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))


def get_active_url(username, password):
    url = ''
    glag = 0
    server = poplib.POP3_SSL('smtp.exmail.qq.com', 995)
    server.set_debuglevel(1)
    server.user(username)
    server.pass_(password)
    resp, mails, octets = server.list()
    index = len(mails)
    resp, lines, octets = server.retr(index)
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    # 稍后解析出邮件:
    msg = Parser().parsestr(msg_content)
    read_email(msg)
    server.quit()
    path = 'C:/dep/content.txt'
    f = open(path, 'r')
    lines = f.readlines()
    for i in lines:
        if u'激活' in i:
            glag = 1
        if U'密码' in i:
            glag = 2
        if 'html"  >' in i:
            start = i.find('html"  >')
            url = i[start + 8:-10]
            if 'amp;' in url:
                url = url.replace('amp;','')
            break
    f.close()
    return url,glag

def check_user_register_email(url):
    driver = webdriver.Chrome()
    driver.get(url)

def reset_password(url, password):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.find_element_by_id('new_password').send_keys(password)
    driver.find_element_by_name('confirm_password').send_keys(password)
    driver.find_element_by_css_selector('.btn.btn-primary').click()

def set_email_seen(account, password):
    r = imaplib.IMAP4_SSL('smtp.exmail.qq.com')
    r.login(account, password)
    r.list()
    r.select('inbox')
    typ, data = r.search(None, 'UNSEEN')
    for num in data[0].split():
        r.store(num, '+FLAGS', '\Seen')

def get_email_unseen(account, password):
    r = imaplib.IMAP4_SSL('smtp.exmail.qq.com')
    r.login(account, password)
    x, y = r.status('INBOX', '(MESSAGES UNSEEN)')
    allmes, unseenmes = re.match(r'.*\s+(\d+)\s+.*\s+(\d+)', y[0]).groups()
    return unseenmes

if __name__ == '__main__':
    url, str = get_active_url('wangqi@xlink.cn', '120211Qq')
    print(url)
    print(str)
