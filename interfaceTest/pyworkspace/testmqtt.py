# -*- coding: utf-8 -*-


import re
import os
import tempfile
import paramiko
from time import sleep
import datetime
import threading


class Properties:

    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}
        try:
            fopen = open(self.file_name, 'r')
            for line in fopen:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    self.properties[strs[0].strip()] = strs[1].strip()
        except Exception, e:
            raise e
        else:
            fopen.close()

    def has_key(self, key):
        return self.properties.has_key(key)

    def get(self, key, default_value=''):
        if self.properties.has_key(key):
            return self.properties[key]
        return default_value

    def put(self, key, value):
        self.properties[key] = value
        replace_property(self.file_name, key + '=.*', key + '=' + value, True)


def parse(file_name):
    return Properties(file_name)


def replace_property(file_name, from_regex, to_str, append_on_not_exists=True):
    file = tempfile.TemporaryFile()         #创建临时文件

    if os.path.exists(file_name):
        r_open = open(file_name,'r')
        pattern = re.compile(r'' + from_regex)
        found = None
        for line in r_open: #读取原文件
            if pattern.search(line) and not line.strip().startswith('#'):
                found = True
                line = re.sub(from_regex, to_str, line)
            file.write(line)   #写入临时文件
        if not found and append_on_not_exists:
            file.write('\n' + to_str)
        r_open.close()
        file.seek(0)

        content = file.read()  #读取临时文件中的所有内容

        if os.path.exists(file_name):
            os.remove(file_name)

        w_open = open(file_name,'w')
        w_open.write(content)   #将临时文件中的内容写入原文件
        w_open.close()

        file.close()  #关闭临时文件，同时也会自动删掉临时文件
    else:
        print "file %s not found" % file_name

class Linux(object):

    def __init__(self,hostname,username,password,timeout=30):
        self.hosetname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout
        self.t = ''
        self.chan = ''

    def connect_to_cmd(self):
        self.t = paramiko.SSHClient()
        self.t.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.t.connect(hostname=hostname, port=22, username=username, password=password)


    def connect_to_upload(self):
        self.t = paramiko.Transport((hostname, 22))
        self.t.connect(username=username, password=password)

    def upload(self,local_dir,remote_dir):
        sftp = paramiko.SFTPClient.from_transport(self.t)
        sftp.put(localpath=local_dir, remotepath=remote_dir)
        sftp.close()

    def close(self):
        self.t.close()

    def send_cmd(self, cmd):
        stdin, stdout, stderr = self.t.exec_command(cmd)
        res = stdout.read()
        res_errpr = stderr.read()
        # print res
        # print res_errpr

    def send_cmd1(self, cmd):
        stdin, stdout, stderr = self.t.exec_command(cmd)
        res = stdout.read()
        res_errpr = stderr.read()
        print res
        print res_errpr

    def send_cmd2(self, cmd):
        stdin, stdout, stderr = self.t.exec_command(cmd)
        res = stdout.read()
        res_errpr = stderr.read()
        return res

def command(cmd):
    host = Linux(hostname, username, password)
    host.connect_to_cmd()
    host.send_cmd(cmd)
    host.close()

def command1(cmd):
    host = Linux(hostname, username, password)
    host.connect_to_cmd()
    host.send_cmd1(cmd)
    host.close()

def command2(cmd):
    host = Linux(hostname, username, password)
    host.connect_to_cmd()
    str = host.send_cmd2(cmd)
    host.close()
    return str



# t2 = threading.Thread(target=command1, args=('pwd',))
# threads.append(t2)


if __name__ == '__main__':
    hostname = '47.106.106.91'
    username = 'mint'
    password = 'P@ssw0rd123456!'
    file_path = 'C:/wq/config.properties'
    remotr_path = '/home/mint/config/config.properties'
    host = Linux(hostname,username,password)
    host.connect_to_upload()
    host.upload(file_path, remotr_path)
    # host.connect_to_cmd()
    # host.send_cmd('ls mqtt-client/logs -l')
    # host.send_cmd('cd /home/mint/xlink/mqtt-client/;pwd')


    threads = []
    t1 = threading.Thread(target=command, args=('nohup /home/mint/xlink/jdk1.8.0_172/bin/java -jar /home/mint/xlink/mqtt-client/mqtt-client.jar &',))
    threads.append(t1)
    print('thread 1 start: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    for t in threads:
        t.setDaemon(True)
        t.start()
    sleep(20)
    print('thread 1 end: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    command1('tail -n 20 logs/mqtt-server.log')
    strs = command2('ps -ef | grep mqtt-client.jar| awk "{print $2}"')
    ids = int(strs[9:15])
    command2('kill -9 '+str(ids))
    # sleep(3)
    # threads = []
    # t1 = threading.Thread(target=command, args=('nohup /home/mint/xlink/jdk1.8.0_172/bin/java -jar '
    #                                             '/home/mint/xlink/mqtt-client/mqtt-client.jar &',))
    # threads.append(t1)
    # print('thread 2 start: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    # sleep(20)
    # print('thread 2 end: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # command1('tail -n 20 logs/mqtt-server.log')
    # strs = command2('ps -ef | grep mqtt-client.jar| awk "{print $2}"')
    # ids = int(strs[9:15])
    # command('kill -9 ' + str(ids))
    

    # host.send_cmd('nohup /home/mint/xlink/jdk1.8.0_172/bin/java -jar /home/mint/xlink/mqtt-client/mqtt-client.jar &')
    # sleep(3)
    # host.send_cmd('pwd')
    # host.send_cmd('cat mqtt-server.log.99')
    # host.close()
    # props = parse(file_path)  # 读取文件
    # props.put('api.host', 'http://10.1.1.34')  # 修改/添加key=value
    # print props.get('api.host')  # 根据key读取value
    # print "props.has_key('api.host')=" + str(props.has_key('api.host'))  # 判断是否包含该key
    # upload(file_path, remotr_path)


