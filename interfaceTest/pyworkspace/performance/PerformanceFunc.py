# -*- coding: utf-8 -*-


import re
import os
import tempfile
import paramiko
import ApiFunc as af
import Function as func
from time import sleep
import datetime
import threading
import ExcelFunc


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
    file = tempfile.TemporaryFile()         # 创建临时文件

    if os.path.exists(file_name):
        r_open = open(file_name,'r')
        pattern = re.compile(r'' + from_regex)
        found = None
        for line in r_open: # 读取原文件
            if pattern.search(line) and not line.strip().startswith('#'):
                found = True
                line = re.sub(from_regex, to_str, line)
            file.write(line)   # 写入临时文件
        if not found and append_on_not_exists:
            file.write('\n' + to_str)
        r_open.close()
        file.seek(0)

        content = file.read()  # 读取临时文件中的所有内容

        if os.path.exists(file_name):
            os.remove(file_name)

        w_open = open(file_name,'w')
        w_open.write(content)   # 将临时文件中的内容写入原文件
        w_open.close()

        file.close()  # 关闭临时文件，同时也会自动删掉临时文件
    else:
        print "file %s not found" % file_name

class Linux(object):

    def __init__(self,hostname,username,password,timeout=30):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout
        self.t = ''
        self.chan = ''

    def connect_to_cmd(self):
        self.t = paramiko.SSHClient()
        self.t.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.t.connect(hostname=self.hostname, port=22, username=self.username, password=self.password)

    def connect_to_upload(self):
        self.t = paramiko.Transport((self.hostname, 22))
        self.t.connect(username=self.username, password=self.password)

    def upload(self,local_dir,remote_dir):
        sftp = paramiko.SFTPClient.from_transport(self.t)
        sftp.put(localpath=local_dir, remotepath=remote_dir)
        sftp.close()

    def download(self,local_dir,remote_dir):
        sftp = paramiko.SFTPClient.from_transport(self.t)
        sftp.get(localpath=local_dir, remotepath=remote_dir)
        sftp.close()

    def close(self):
        self.t.close()

    def send_cmd(self, cmd):
        stdin, stdout, stderr = self.t.exec_command(cmd)
        res = stdout.read()
        res_errpr = stderr.read()
        return res


def command(cmd):
    host = Linux(cm_hostname, cm_username, cm_password)
    host.connect_to_cmd()
    res = host.send_cmd(cmd)
    host.close()
    return res


def command_2(cmd):
    host = Linux(cm_hostname_2, cm_username_2, cm_password_2)
    host.connect_to_cmd()
    res = host.send_cmd(cmd)
    host.close()
    return res


def command_3(cmd):
    host = Linux(cm_hostname_3, cm_username_3, cm_password_3)
    host.connect_to_cmd()
    res = host.send_cmd(cmd)
    host.close()
    return res


def ab_command2(cmd):
    host2 = Linux(ab_hostname, ab_username, ab_password)
    host2.connect_to_cmd()
    res = host2.send_cmd(cmd)
    host2.close()
    return res


def modify_sh(path, new):
    f1 = open(path, 'w')
    f1.write(new)
    f1.close()


def upload_file(host, name, password, local, remote):
    host = Linux(host, name, password)
    host.connect_to_upload()
    host.upload(local, remote)
    func.log(u'上传postdata.txt至ab命令服务器成功')


def down_file(host, name, password, local, remote):
    if not os.path.exists('C:/mqtt-client/'):
        os.makedirs('C:/mqtt-client/')
    if not os.path.exists(local):
        fobj = open(local, 'w')
        fobj.close()
    host = Linux(host, name, password)
    host.connect_to_upload()
    host.download(local, remote)
    func.log(u'下载config配置文件到本地成功')


def modify_1_config_upload(active, online, sync, offset, limit):
    props1 = parse(local_config_path)
    props1.put('device.is.active', active)
    props1.put('device.is.online', online)
    props1.put('device.is.datapoint.sync', sync)
    props1.put('device.offset', offset)
    props1.put('device.limit', limit)
    host = Linux(cm_hostname, cm_username, cm_password)
    host.connect_to_upload()
    host.upload(local_config_path, remote_config_path)


def modify_2_config_upload(active, online, sync, offset, limit):
    props2 = parse(local_config_path)
    props2.put('device.is.active', active)
    props2.put('device.is.online', online)
    props2.put('device.is.datapoint.sync', sync)
    props2.put('device.offset', offset)
    props2.put('device.limit', limit)
    host = Linux(cm_hostname_2, cm_username_2, cm_password_2)
    host.connect_to_upload()
    host.upload(local_config_path, remote_config_path_2)


def modify_3_config_upload(active, online, sync, offset, limit):
    props3 = parse(local_config_path)
    props3.put('device.is.active', active)
    props3.put('device.is.online', online)
    props3.put('device.is.datapoint.sync', sync)
    props3.put('device.offset', offset)
    props3.put('device.limit', limit)
    host = Linux(cm_hostname_3, cm_username_3, cm_password_3)
    host.connect_to_upload()
    host.upload(local_config_path, remote_config_path_3)


def modify_ab_config_upload(active, online, sync, offset, limit):
    props_ab = parse(local_config_path)
    props_ab.put('device.is.active', active)
    props_ab.put('device.is.online', online)
    props_ab.put('device.is.datapoint.sync', sync)
    props_ab.put('device.offset', offset)
    props_ab.put('device.limit', limit)
    host = Linux(ab_hostname, ab_username, ab_password)
    host.connect_to_upload()
    host.upload(local_config_path, ab_remote_config_path)
    
    
def kill_1_pid():
    pid = command('ps -ef | grep mqtt-client.jar| awk "{print $2}"')
    path = 'C:/mqtt-client/pid.txt'
    if not os.path.exists(path):
        fobj = open(path, 'w')
        fobj.close()
    f = open(path, 'w')
    f.write(pid)
    f.close()
    f1 = open(path, 'r')
    for line in f1.readlines():
        ids = int(line[9:15])
        command('kill -9 ' + str(ids))


def kill_2_pid():
    pid = command_2('ps -ef | grep mqtt-client.jar| awk "{print $2}"')
    path = 'C:/mqtt-client/pid.txt'
    if not os.path.exists(path):
        fobj = open(path, 'w')
        fobj.close()
    f = open(path, 'w')
    f.write(pid)
    f.close()
    f1 = open(path, 'r')
    for line in f1.readlines():
        ids = int(line[9:15])
        command_2('kill -9 ' + str(ids))


def kill_3_pid():
    pid = command_3('ps -ef | grep mqtt-client.jar| awk "{print $2}"')
    path = 'C:/mqtt-client/pid.txt'
    if not os.path.exists(path):
        fobj = open(path, 'w')
        fobj.close()
    f = open(path, 'w')
    f.write(pid)
    f.close()
    f1 = open(path, 'r')
    for line in f1.readlines():
        ids = int(line[9:15])
        command_3('kill -9 ' + str(ids))


def kill_ab_pid():
    pid = ab_command2('ps -ef | grep mqtt-client.jar| awk "{print $2}"')
    path = 'C:/mqtt-client/pid.txt'
    if not os.path.exists(path):
        fobj = open(path, 'w')
        fobj.close()
    f = open(path, 'w')
    f.write(pid)
    f.close()
    f1 = open(path, 'r')
    for line in f1.readlines():
        ids = int(line[9:15])
        ab_command2('kill -9 ' + str(ids))


def write_1_cm_result(name, times, start, end):
    result1 = command('tail -n 30 logs/mqtt-server.log')
    msg1 = af.get_msg_by_cm_result(name, result1, '1')
    record1 = [name, '1', times, start, end, msg1[0], msg1[1], msg1[2], msg1[3], msg1[4]]
    cm_tableValues.append(record1)
    ExcelFunc.write_cm_excel(cm_tableValues)


def write_2_cm_result(name, times, start, end):
    result2 = command_2('tail -n 30 logs/mqtt-server.log')
    msg2 = af.get_msg_by_cm_result(name, result2, '2')
    record2 = [name, '2', times, start, end, msg2[0], msg2[1], msg2[2], msg2[3], msg2[4]]
    cm_tableValues.append(record2)
    ExcelFunc.write_cm_excel(cm_tableValues)


def write_3_cm_result(name, times, start, end):
    result3 = command_3('tail -n 30 logs/mqtt-server.log')
    msg3 = af.get_msg_by_cm_result(name, result3, '3')
    record3 = [name, '3', times, start, end, msg3[0], msg3[1], msg3[2], msg3[3], msg3[4]]
    cm_tableValues.append(record3)
    ExcelFunc.write_cm_excel(cm_tableValues)


def write_ab_cm_result(name, times, start, end):
    result_ab = ab_command2('tail -n 30 logs/mqtt-server.log')
    msg_ab = af.get_msg_by_cm_result(name, result_ab, 'ab')
    record_ab = [name, 'ab', times, start, end, msg_ab[0], msg_ab[1], msg_ab[2], msg_ab[3], msg_ab[4]]
    cm_tableValues.append(record_ab)
    ExcelFunc.write_cm_excel(cm_tableValues)


def copy_config_to_base_path():
    command('cp -r ' + config_old_path + ' ' + config_new_path)
    ab_command2('cp -r ' + ab_config_old_path + ' ' + ab_config_new_path)
    # command_2('cp -r ' + config_old_path + ' ' + config_new_path_2)
    # command_3('cp -r ' + config_old_path + ' ' + config_new_path_3)复制配置文件到服务器登录后根目录
    func.log(u'复制配置文件到服务器登录后根目录成功')


if __name__ == '__main__':
    cm_hostname = '47.106.106.91'                   # 测试cm的linux服务器地址
    cm_username = 'mint'                            # 测试cm的linux服务器登录名称
    cm_password = 'P@ssw0rd123456!'                 # 测试cm的linux服务器登录密码
    cm_hostname_2 = ''                              # 测试cm的linux服务器地址
    cm_username_2 = ''                              # 测试cm的linux服务器登录名称
    cm_password_2 = ''                              # 测试cm的linux服务器登录密码
    cm_hostname_3 = ''                              # 测试cm的linux服务器地址
    cm_username_3 = ''                              # 测试cm的linux服务器登录名称
    cm_password_3 = ''                              # 测试cm的linux服务器登录密码
    ab_hostname = '39.108.133.232'                  # 测试api压力的linux服务器地址
    ab_username = 'root'                            # 测试api压力的linux服务器登录名称
    ab_password = 'Mint-parking!@'                  # 测试api压力的linux服务器登录密码
    base_path = '/home/mint'                        # 测试cm的linux服务器登录后路径
    base_path_2 = ''                                # 测试cm的linux服务器登录后路径
    base_path_3 = ''                                # 测试cm的linux服务器登录后路径
    ab_base_path = '/root'                          # 测试api压力的linux服务器登录后路径
    api_host = 'http://mint-api.homecity365.com'    # 管理台api地址
    api_port = ''                                   # 管理台api端口
    member = 'rym@xlink.cn'                         # 企业成员
    mem_password = 'Test1234'                       # 企业成员密码
    user_email = 'test@xlink.cn'                    # 用于注册登录的用户名
    user_password = 'Test1234'                      # 用户密码
    api_host_config = 'http://172.18.222.15'        # 配置的api.host
    api_port_config = ':8887'
    user_id = '290727677'
    user_token = 'QTRFOTMxQ0FCODQ4Q0QxMTkyMTk2NzlCNjdDNjcxRDQzQ0MzNzBFMEFGMUU3Mzk4NjY0NTcxRUQwM0YzNTZCNA=='
    corp_id = '1007d2b5e0046800'
    accesskey_id = '3207d4b748eaec00'
    accesskey_secret = 'bbe06f759c780d803b1c68af545bc713'
    product_id = '1607d4b748ea1f411607d4b748eaea01'
    product_key = 'd650a24e38e90805c22d653661fb414f'
    device_id = '290726071'
    local_body_path = 'C:/mqtt-client/postdata.txt'
    local_config_path = 'C:/mqtt-client/config.properties'
    cm_command = 'nohup ' + base_path + '/xlink/jdk1.8.0_172/bin/java -jar ' + base_path + '/xlink/mqtt-client/mqtt-client.jar &'
    cm_command_2 = 'nohup ' + base_path_2 + '/xlink/jdk1.8.0_172/bin/java -jar ' + base_path_2 + '/xlink/mqtt-client/mqtt-client.jar &'
    cm_command_3 = 'nohup ' + base_path_3 + '/xlink/jdk1.8.0_172/bin/java -jar ' + base_path_3 + '/xlink/mqtt-client/mqtt-client.jar &'
    ab_command = 'nohup ' + ab_base_path + '/xlink/jdk1.8.0_172/bin/java -jar ' + ab_base_path + '/xlink/mqtt-client/mqtt-client.jar &'
    remote_ab_body_path = ab_base_path + '/postdata.txt'
    remote_config_path = base_path+'/config/config.properties'
    remote_config_path_2 = base_path_2 + '/config/config.properties'
    remote_config_path_3 = base_path_3 + '/config/config.properties'
    ab_remote_config_path = ab_base_path + '/config/config.properties'
    config_old_path = base_path+'/xlink/mqtt-client/config/'
    config_new_path = base_path
    config_old_path_2 = base_path_2 + '/xlink/mqtt-client/config/'
    config_new_path_2 = base_path_2
    config_old_path_3 = base_path_3 + '/xlink/mqtt-client/config/'
    config_new_path_3 = base_path_3
    ab_config_old_path = ab_base_path+'/xlink/mqtt-client/config/'
    ab_config_new_path = ab_base_path
    tableValues = []
    cm_tableValues = []
    func.log(u'-------------------------开始初始化环境------------------------')
    # 创建产品、数据端点1个int16（0-100）、设置异常规则（<100）、设置报警规则、新建一个用户和一个设备并建立订阅关系、外部访问许可拿accesskey、用户设置设备的扩展属性
    # corp_id = af.get_access_token(api_host, api_port, member, mem_password)               # 获取token
    # product_id, product_key = af.create_product(api_host, api_port)                       # 创建产品
    # point_index, point_id = af.add_data_point_custom(api_host, api_port, product_id)      # 添加数据端点int16(0-100)
    # # exception_id, tag_id = af.alter_rule_new(api_host, api_port, product_id, point_id)    # V5.2创建异常规则int16<=100
    # # af.alarm_setting_new(api_host, api_port, product_id, point_id, exception_id, tag_id)  # V5.2设置报警规则
    # af.alarm_setting_old(api_host, api_port, product_id, point_id)                        # 旧版设置告警int16<=100
    # device_id, user_id, user_token = af.user_subscribe_device(api_host, api_port, product_id, corp_id, user_email, user_password)  # 新建一个用户和一个设备并建立订阅关系
    # accesskey_id, accesskey_secret = af.get_access_key(api_host, api_port)                # 添加accesskey
    # af.set_device_property(api_host, api_port, product_id, device_id)                     # 设置设备扩展属性
    af.write_login_body_to_txt(corp_id, user_email, user_password, local_body_path)         # 登录的body写入txt文件
    # upload_file(ab_hostname, ab_username, ab_password, local_body_path, remote_ab_body_path)    # 上传登录body文件到ab可执行服务器
    # copy_config_to_base_path()                                                                  # 复制配置文件到服务器登录后根目录
    # down_file(cm_hostname, cm_username, cm_password, local_config_path, remote_config_path)     # 下载配置文件到本地
    # func.log(u'-------------------------初始化环境结束-------------------------')
    # func.log(u'---------------------------------------------------------------')
    # func.log(u'-------------------------开始api压力测试------------------------')
    # # 用户登录api-1万
    # func.log(u'--------开始用户登录api-1万个并发')
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ab_com = 'ab -c 5000 -n 10000 -T "application/json" -p postdata.txt '+api_host_config+api_port_config+'/v2/user_auth'
    # func.log(u'命令为： ' + ab_com)
    # result = ab_command2(ab_com)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # func.log(u'用户登录api-1万个并发结束')
    # msg = af.get_msg_by_ab_result(u'用户登录api-1万', result)
    # record = [u'用户登录api-1万', start_time, end_time, msg[0], msg[1], msg[2], msg[4]]
    # tableValues.append(record)
    # ExcelFunc.write_api_excel(tableValues)
    #
    # # 用户登录api-5万
    # func.log(u'--------开始用户登录api-5万个并发')
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ab_com = 'ab -c 5000 -n 50000 -T "application/json" -p postdata.txt ' + api_host_config + api_port_config + '/v2/user_auth'
    # func.log(u'命令为： ' + ab_com)
    # result = ab_command2(ab_com)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # func.log(u'用户登录api-5万个并发结束')
    # msg = af.get_msg_by_ab_result(u'用户登录api-5万', result)
    # record = [u'用户登录api-5万', start_time, end_time, msg[0], msg[1], msg[2], msg[4]]
    # tableValues.append(record)
    # ExcelFunc.write_api_excel(tableValues)
    #
    # # 用户登录api-10万
    # func.log(u'--------开始用户登录api-10万个并发')
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ab_com = 'ab -c 5000 -n 100000 -T "application/json" -p postdata.txt ' + api_host_config + api_port_config + '/v2/user_auth'
    # func.log(u'命令为： ' + ab_com)
    # result = ab_command2(ab_com)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # func.log(u'用户登录api-10万个并发结束')
    # msg = af.get_msg_by_ab_result(u'用户登录api-10万', result)
    # record = [u'用户登录api-10万', start_time, end_time, msg[0], msg[1], msg[2], msg[4]]
    # tableValues.append(record)
    # ExcelFunc.write_api_excel(tableValues)
    #
    # # 获取用户订阅列表api-1万
    # func.log(u'--------开始获取用户订阅列表api-1万个并发')
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ab_com = 'ab -c 5000 -n 10000 -T "application/json" -H "Access-Token:' + user_token + '"' + " " + api_host_config +\
    #     api_port_config + '/v2/user/' + str(user_id) + '/subscribe/devices'
    # func.log(u'命令为： ' + ab_com)
    # result = ab_command2(ab_com)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # func.log(u'获取用户订阅列表api-1万个并发结束')
    # msg = af.get_msg_by_ab_result(u'获取用户订阅列表api-1万', result)
    # record = [u'获取用户订阅列表api-1万', start_time, end_time, msg[0], msg[1], msg[2], msg[4]]
    # tableValues.append(record)
    # ExcelFunc.write_api_excel(tableValues)
    #
    # # 获取用户订阅列表api-5万
    # func.log(u'--------开始获取用户订阅列表api-5万个并发')
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ab_com = 'ab -c 5000 -n 50000 -T "application/json" -H "Access-Token:' + user_token + '"' + " " + api_host_config +\
    #     api_port_config + '/v2/user/' + str(user_id) + '/subscribe/devices'
    # func.log(u'命令为： ' + ab_com)
    # result = ab_command2(ab_com)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # func.log(u'获取用户订阅列表api-5万个并发结束')
    # msg = af.get_msg_by_ab_result(u'获取用户订阅列表api-5万', result)
    # record = [u'获取用户订阅列表api-5万', start_time, end_time, msg[0], msg[1], msg[2], msg[4]]
    # tableValues.append(record)
    # ExcelFunc.write_api_excel(tableValues)
    #
    # # 获取用户订阅列表api-10万
    # func.log(u'--------开始获取用户订阅列表api-10万个并发')
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ab_com = 'ab -c 5000 -n 100000 -T "application/json" -H "Access-Token:' + user_token + '"' + " " + api_host_config +\
    #     api_port_config + '/v2/user/' + str(user_id) + '/subscribe/devices'
    # func.log(u'命令为： ' + ab_com)
    # result = ab_command2(ab_com)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # func.log(u'获取用户订阅列表api-10万个并发结束')
    # msg = af.get_msg_by_ab_result(u'获取用户订阅列表api-10万', result)
    # record = [u'获取用户订阅列表api-10万', start_time, end_time, msg[0], msg[1], msg[2], msg[4]]
    # tableValues.append(record)
    # ExcelFunc.write_api_excel(tableValues)
    #
    # # 获取设备订阅关系api-1万
    # func.log(u'--------开始获取设备订阅关系api-1万个并发')
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ab_com = 'ab -c 5000 -n 10000 -T "application/json" -H "Access-Token:' + user_token + '"' + " " + api_host_config +\
    #     api_port_config + '/v2/user/' + str(user_id) + '/subscribe_users?device_id=' + str(device_id)
    # func.log(u'命令为： ' + ab_com)
    # result = ab_command2(ab_com)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # func.log(u'获取设备订阅关系api-1万个并发结束')
    # msg = af.get_msg_by_ab_result(u'获取设备订阅关系api-1万', result)
    # record = [u'获取设备订阅关系api-1万', start_time, end_time, msg[0], msg[1], msg[2], msg[4]]
    # tableValues.append(record)
    # ExcelFunc.write_api_excel(tableValues)
    #
    # # 获取设备订阅关系api-5万
    # func.log(u'--------开始获取设备订阅关系api-5万个并发')
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ab_com = 'ab -c 5000 -n 50000 -T "application/json" -H "Access-Token:' + user_token + '"' + " " + api_host_config +\
    #     api_port_config + '/v2/user/' + str(user_id) + '/subscribe_users?device_id=' + str(device_id)
    # func.log(u'命令为： ' + ab_com)
    # result = ab_command2(ab_com)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # func.log(u'获取设备订阅关系api-5万个并发结束')
    # msg = af.get_msg_by_ab_result(u'获取设备订阅关系api-5万', result)
    # record = [u'获取设备订阅关系api-5万', start_time, end_time, msg[0], msg[1], msg[2], msg[4]]
    # tableValues.append(record)
    # ExcelFunc.write_api_excel(tableValues)
    #
    # # 获取设备订阅关系api-10万
    # func.log(u'--------开始获取设备订阅关系api-10万个并发')
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ab_com = 'ab -c 5000 -n 100000 -T "application/json" -H "Access-Token:' + user_token + '"' + " " + api_host_config + \
    #          api_port_config + '/v2/user/' + str(user_id) + '/subscribe_users?device_id=' + str(device_id)
    # func.log(u'命令为： ' + ab_com)
    # result = ab_command2(ab_com)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # func.log(u'获取设备订阅关系api-10万个并发结束')
    # msg = af.get_msg_by_ab_result(u'获取设备订阅关系api-10万', result)
    # record = [u'获取设备订阅关系api-10万', start_time, end_time, msg[0], msg[1], msg[2], msg[4]]
    # tableValues.append(record)
    # ExcelFunc.write_api_excel(tableValues)
    #
    # # 获取用户信息api-1万
    # func.log(u'--------开始获取用户信息api-1万个并发')
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ab_com = 'ab -c 5000 -n 10000 -T "application/json" -H "Access-Token:' + user_token + '"' + " " + api_host_config +\
    #     api_port_config + '/v2/user/' + str(user_id)
    # func.log(u'命令为： ' + ab_com)
    # result = ab_command2(ab_com)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # func.log(u'获取用户信息api-1万个并发结束')
    # msg = af.get_msg_by_ab_result(u'获取用户信息api-1万', result)
    # record = [u'获取用户信息api-1万', start_time, end_time, msg[0], msg[1], msg[2], msg[4]]
    # tableValues.append(record)
    # ExcelFunc.write_api_excel(tableValues)
    #
    # # 获取用户信息api-5万
    # func.log(u'--------开始获取用户信息api-5万个并发')
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ab_com = 'ab -c 5000 -n 50000 -T "application/json" -H "Access-Token:' + user_token + '"' + " " + api_host_config +\
    #     api_port_config + '/v2/user/' + str(user_id)
    # func.log(u'命令为： ' + ab_com)
    # result = ab_command2(ab_com)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # func.log(u'获取用户信息api-5万个并发结束')
    # msg = af.get_msg_by_ab_result(u'获取用户信息api-5万', result)
    # record = [u'获取用户信息api-5万', start_time, end_time, msg[0], msg[1], msg[2], msg[4]]
    # tableValues.append(record)
    # ExcelFunc.write_api_excel(tableValues)
    #
    # # 获取用户信息api-10万
    # func.log(u'--------开始获取用户信息api-10万个并发')
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ab_com = 'ab -c 5000 -n 100000 -T "application/json" -H "Access-Token:' + user_token + '"' + " " + api_host_config +\
    #     api_port_config + '/v2/user/' + str(user_id)
    # func.log(u'命令为： ' + ab_com)
    # result = ab_command2(ab_com)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # func.log(u'获取用户信息api-10万个并发结束')
    # msg = af.get_msg_by_ab_result(u'获取用户信息api-10万', result)
    # record = [u'获取用户信息api-10万', start_time, end_time, msg[0], msg[1], msg[2], msg[4]]
    # tableValues.append(record)
    # ExcelFunc.write_api_excel(tableValues)
    #
    # # 获取设备扩展属性api-1万
    # func.log(u'--------开始获取设备扩展属性api-1万个并发')
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ab_com = 'ab -c 5000 -n 10000 -T "application/json" -H "Access-Token:' + user_token + '"' + " " + api_host_config +\
    #     api_port_config + '/v2/product/' + product_id + '/device/' + str(device_id) + '/property'
    # func.log(u'命令为： ' + ab_com)
    # result = ab_command2(ab_com)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # func.log(u'获取设备扩展属性api-1万个并发结束')
    # msg = af.get_msg_by_ab_result(u'获取设备扩展属性api-1万', result)
    # record = [u'获取设备扩展属性api-1万', start_time, end_time, msg[0], msg[1], msg[2], msg[4]]
    # tableValues.append(record)
    # ExcelFunc.write_api_excel(tableValues)
    #
    # # 获取设备扩展属性api-5万
    # func.log(u'--------开始获取设备扩展属性api-5万个并发')
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ab_com = 'ab -c 5000 -n 50000 -T "application/json" -H "Access-Token:' + user_token + '"' + " " + api_host_config +\
    #     api_port_config + '/v2/product/' + product_id + '/device/' + str(device_id) + '/property'
    # func.log(u'命令为： ' + ab_com)
    # result = ab_command2(ab_com)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # func.log(u'获取设备扩展属性api-5万个并发结束')
    # msg = af.get_msg_by_ab_result(u'获取设备扩展属性api-5万', result)
    # record = [u'获取设备扩展属性api-5万', start_time, end_time, msg[0], msg[1], msg[2], msg[4]]
    # tableValues.append(record)
    # ExcelFunc.write_api_excel(tableValues)
    #
    # # 获取设备扩展属性api-10万
    # func.log(u'--------开始获取设备扩展属性api-10万个并发')
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ab_com = 'ab -c 5000 -n 100000 -T "application/json" -H "Access-Token:' + user_token + '"' + " " + api_host_config +\
    #     api_port_config + '/v2/product/' + product_id + '/device/' + str(device_id) + '/property'
    # func.log(u'命令为： ' + ab_com)
    # result = ab_command2(ab_com)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # func.log(u'获取设备扩展属性api-10万个并发结束')
    # msg = af.get_msg_by_ab_result(u'获取设备扩展属性api-10万', result)
    # record = [u'获取设备扩展属性api-10万', start_time, end_time, msg[0], msg[1], msg[2], msg[4]]
    # tableValues.append(record)
    # ExcelFunc.write_api_excel(tableValues)
    # func.log(u'-------------------------api压力测试结束-------------------------')
    # func.log(u'---------------------------------------------------------------')
    #
    # # 添加设备10万
    # # func.log(u'--------开始导入设备---------')
    # for i in range(20):
    #     func.log(u'每次导入5000条，导入次数： '+ str(i))
    #     af.import_devices(api_host, api_port, product_id, 5000)
    # func.log(u'导入设备结束')
    # # ab命令查产品设备列表性能10万
    #
    # # ab命令查设备管理所有设备性能10万
    #
    # # 添加设备10万
    #
    # # ab命令查产品设备列表性能20万
    #
    # # ab命令查设备管理所有设备性能20万
    #
    # # 添加用户10万
    #
    # # ab命令查用户列表性能10万
    #
    # # 添加用户10万
    #
    # # ab命令查用户列表性能20万
    #
    # # 初始化环境
    # func.log(u'-------------------------开始初始化cm测试环境----------------------------')
    # props = parse(local_config_path)
    # props.put('api.host', api_host_config)
    # props.put('accesskey.id', accesskey_id)
    # props.put('accesskey.secret', accesskey_secret)
    # props.put('product.id', product_id)
    # props.put('product.key', product_key)
    # func.log(u'-------------------------cm测试环境环境初始化结束-------------------------')
    # func.log(u'-----------------------------------------------------------------------')
    # func.log(u'----------------------------开始cm测试并发-----------------    ----------')
    # # #
    # # # 连接：添加缓存
    # func.log(u'--------开始cm连接测试-添加缓存')
    # modify_1_config_upload('false', 'false', 'false', '0', '50000')
    # modify_ab_config_upload('false', 'false', 'false', '50000', '50000')
    # # modify_2_config_upload('false', 'false', 'false', '50000', '50000')
    # # modify_3_config_upload('false', 'false', 'false', '50000', '50000')
    # threads = []
    # t1 = threading.Thread(target=command, args=(cm_command,))
    # t2 = threading.Thread(target=ab_command2, args=(ab_command,))
    # # t3 = threading.Thread(target=command_2, args=(cm_command_2,))
    # # t4 = threading.Thread(target=command_3, args=(cm_command_3,))
    # threads.append(t1)
    # threads.append(t2)
    # # threads.append(t3)
    # # threads.append(t4)
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    # sleep(300)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # kill_1_pid()
    # kill_ab_pid()
    # # kill_2_pid()
    # # kill_3_pid()
    # write_1_cm_result(u'cm连接压力测试-缓存', u'添加到缓存', start_time, end_time)
    # write_ab_cm_result(u'cm连接压力测试-缓存', u'添加到缓存', start_time, end_time)
    # # write_2_cm_result(u'cm连接压力测试-缓存', u'添加到缓存', start_time, end_time)
    # # write_3_cm_result(u'cm连接压力测试-缓存', u'添加到缓存', start_time, end_time)
    # sleep(300)
    # #
    # # # # 连接：5万  全部是false   device.offset=0   device.limit=50000   等待5分钟  都拿两次 5分钟一次 15分钟二次
    # func.log(u'--------开始cm连接测试-5万个并发')
    # t5 = threading.Thread(target=command, args=(cm_command,))
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # t5.setDaemon(True)
    # t5.start()
    # sleep(900)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # kill_1_pid()
    # write_1_cm_result(u'cm连接压力测试-5万', u'第二次', start_time, end_time)
    # sleep(300)
    # #
    # # # # 连接：10万  要连两台 1、device.offset=0   device.limit=50000  2、device.offset=50000   device.limit=50000 等待5分钟 都拿两次 5分钟一次 15分钟二次
    # func.log(u'--------开始cm连接测试-10万个并发')
    # threads = []
    # t6 = threading.Thread(target=command, args=(cm_command,))
    # t7 = threading.Thread(target=ab_command2, args=(ab_command,))
    # threads.append(t6)
    # threads.append(t7)
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    # sleep(900)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # kill_1_pid()
    # kill_ab_pid()
    # write_1_cm_result(u'cm连接压力测试-10万', u'第二次', start_time, end_time)
    # write_ab_cm_result(u'cm连接压力测试-10万', u'第二次', start_time, end_time)
    # sleep(300)
    #
    # # # 连接：20万
    # # func.log(u'--------开始cm连接压力测试-20万个并发')
    # # threads = []
    # # t8 = threading.Thread(target=command, args=(cm_command,))
    # # t9 = threading.Thread(target=ab_command2, args=(ab_command,))
    # # t10 = threading.Thread(target=command_2, args=(cm_command_2,))
    # # t11 = threading.Thread(target=command_2, args=(cm_command_2,))
    # # threads.append(t8)
    # # threads.append(t9)
    # # threads.append(t10)
    # # threads.append(t11)
    # # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # # for t in threads:
    # #     t.setDaemon(True)
    # #     t.start()
    # # sleep(900)
    # # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # # kill_1_pid()
    # # kill_ab_pid()
    # # kill_2_pid()
    # # kill_3_pid()
    # # write_1_cm_result(u'cm连接压力测试-20万', u'第二次', start_time, end_time)
    # # write_ab_cm_result(u'cm连接压力测试-20万', u'第二次', start_time, end_time)
    # # write_2_cm_result(u'cm连接压力测试-20万', u'第二次', start_time, end_time)
    # # write_3_cm_result(u'cm连接压力测试-20万', u'第二次', start_time, end_time)
    # # sleep(300)
    #
    # # # 上线：添加缓存
    # func.log(u'--------开始cm上线压力测试-添加缓存')
    # modify_1_config_upload('false', 'true', 'false', '0', '50000')
    # modify_ab_config_upload('false', 'true', 'false', '50000', '50000')
    # # modify_2_config_upload('false', 'true', 'false', '50000', '50000')
    # # modify_3_config_upload('false', 'true', 'false', '50000', '50000')
    # threads = []
    # t12 = threading.Thread(target=command, args=(cm_command,))
    # t13 = threading.Thread(target=ab_command2, args=(ab_command,))
    # # t14 = threading.Thread(target=command_2, args=(cm_command_2,))
    # # t15 = threading.Thread(target=command_3, args=(cm_command_3,))
    # threads.append(t12)
    # threads.append(t13)
    # # threads.append(t14)
    # # threads.append(t15)
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    # sleep(300)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # kill_1_pid()
    # kill_ab_pid()
    # # kill_2_pid()
    # # kill_3_pid()
    # write_1_cm_result(u'cm上线压力测试-缓存', u'添加到缓存', start_time, end_time)
    # write_ab_cm_result(u'cm上线压力测试-缓存', u'添加到缓存', start_time, end_time)
    # # write_2_cm_result(u'cm上线压力测试-缓存', u'添加到缓存', start_time, end_time)
    # # write_3_cm_result(u'cm上线压力测试-缓存', u'添加到缓存', start_time, end_time)
    # sleep(300)

    # # 上线：5万  device.is.online=true 等待5分钟 都拿两次 5分钟一次 15分钟二次
    # func.log(u'--------开始cm上线压力测试-5万个并发')
    # t16 = threading.Thread(target=command, args=(cm_command,))
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # t16.setDaemon(True)
    # t16.start()
    # sleep(900)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # kill_1_pid()
    # write_1_cm_result(u'cm上线压力测试-5万', u'第二次', start_time, end_time)
    # sleep(300)

    # 上线：10万  要连两台 1、device.offset=0   device.limit=50000  2、device.offset=50000   device.limit=50000 等待5分钟 都拿两次 5分钟一次 15分钟二次
    # func.log(u'--------开始cm上线压力测试-10万个并发')
    # threads = []
    # t17 = threading.Thread(target=command, args=(cm_command,))
    # t18 = threading.Thread(target=ab_command2, args=(ab_command,))
    # threads.append(t17)
    # threads.append(t18)
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    # sleep(900)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # kill_1_pid()
    # kill_ab_pid()
    # write_1_cm_result(u'cm上线压力测试-10万', u'第二次', start_time, end_time)
    # write_ab_cm_result(u'cm上线压力测试-10万', u'第二次', start_time, end_time)
    # sleep(300)
    # #
    # # 上线：20万
    # func.log(u'--------开始cm上线压力测试-20万个并发')
    # threads = []
    # t19 = threading.Thread(target=command, args=(cm_command,))
    # t20 = threading.Thread(target=ab_command2, args=(ab_command,))
    # t21 = threading.Thread(target=command_2, args=(cm_command_2,))
    # t22 = threading.Thread(target=command_2, args=(cm_command_2,))
    # threads.append(t19)
    # threads.append(t20)
    # threads.append(t21)
    # threads.append(t22)
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    # sleep(900)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # kill_1_pid()
    # kill_ab_pid()
    # kill_2_pid()
    # kill_3_pid()
    # write_1_cm_result(u'cm上线压力测试-20万', u'第二次', start_time, end_time)
    # write_ab_cm_result(u'cm上线压力测试-20万', u'第二次', start_time, end_time)
    # write_2_cm_result(u'cm上线压力测试-20万', u'第二次', start_time, end_time)
    # write_3_cm_result(u'cm上线压力测试-20万', u'第二次', start_time, end_time)
    # sleep(300)

    # 激活：添加缓存
    # func.log(u'--------开始cm激活压力测试-添加缓存')
    # modify_1_config_upload('true', 'false', 'false', '0', '50000')
    # modify_ab_config_upload('true', 'false', 'false', '50000', '50000')
    # # modify_2_config_upload('true', 'false', 'false', '50000', '50000')
    # # modify_3_config_upload('true', 'false', 'false', '50000', '50000')
    # threads = []
    # t23 = threading.Thread(target=command, args=(cm_command,))
    # t24 = threading.Thread(target=ab_command2, args=(ab_command,))
    # # t25 = threading.Thread(target=command_2, args=(cm_command_2,))
    # # t26 = threading.Thread(target=command_3, args=(cm_command_3,))
    # threads.append(t23)
    # threads.append(t24)
    # # threads.append(t25)
    # # threads.append(t26)
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    # sleep(600)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # kill_1_pid()
    # kill_ab_pid()
    # # kill_2_pid()
    # # kill_3_pid()
    # write_1_cm_result(u'cm激活压力测试-缓存', u'添加到缓存', start_time, end_time)
    # write_ab_cm_result(u'cm激活压力测试-缓存', u'添加到缓存', start_time, end_time)
    # # write_2_cm_result(u'cm激活压力测试-缓存', u'添加到缓存', start_time, end_time)
    # # write_3_cm_result(u'cm激活压力测试-缓存', u'添加到缓存', start_time, end_time)
    # sleep(300)
    #
    # # 激活：5万   device.is.active=ture 等待5分钟 都拿两次 10分钟一次 20分钟二次
    func.log(u'--------开始cm激活压力测试-5万个并发')
    t27 = threading.Thread(target=command, args=(cm_command,))
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    t27.setDaemon(True)
    t27.start()
    sleep(1200)
    end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    kill_1_pid()
    write_1_cm_result(u'cm激活压力测试-5万', u'第二次', start_time, end_time)
    sleep(300)
    #
    # # 激活：10万  要连两台 1、device.offset=0   device.limit=50000  2、device.offset=50000   device.limit=50000 等待5分钟 都拿两次 10分钟一次 20分钟二次
    # func.log(u'--------开始cm激活压力测试-10万个并发')
    # threads = []
    # t28 = threading.Thread(target=command, args=(cm_command,))
    # t29 = threading.Thread(target=ab_command2, args=(ab_command,))
    # threads.append(t28)
    # threads.append(t29)
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    # sleep(1200)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # kill_1_pid()
    # kill_ab_pid()
    # write_1_cm_result(u'cm激活压力测试-10万', u'第二次', start_time, end_time)
    # write_ab_cm_result(u'cm激活压力测试-10万', u'第二次', start_time, end_time)
    # sleep(300)
    #
    # # 激活：20万
    # # func.log(u'--------开始cm激活压力测试-20万个并发')
    # # threads = []
    # # t30 = threading.Thread(target=command, args=(cm_command,))
    # # t31 = threading.Thread(target=ab_command2, args=(ab_command,))
    # # t32 = threading.Thread(target=command_2, args=(cm_command_2,))
    # # t33 = threading.Thread(target=command_2, args=(cm_command_2,))
    # # threads.append(t30)
    # # threads.append(t31)
    # # threads.append(t32)
    # # threads.append(t33)
    # # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # # for t in threads:
    # #     t.setDaemon(True)
    # #     t.start()
    # # sleep(1800)
    # # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # # kill_1_pid()
    # # kill_ab_pid()
    # # kill_2_pid()
    # # kill_3_pid()
    # # write_1_cm_result(u'cm激活压力测试-20万', u'第二次', start_time, end_time)
    # # write_ab_cm_result(u'cm激活压力测试-20万', u'第二次', start_time, end_time)
    # # write_2_cm_result(u'cm激活压力测试-20万', u'第二次', start_time, end_time)
    # # write_3_cm_result(u'cm激活压力测试-20万', u'第二次', start_time, end_time)
    # # sleep(300)
    #
    # # 上报：添加到缓存
    # func.log(u'--------开始cm上报压力测试-添加缓存')
    # modify_1_config_upload('false', 'true', 'true', '0', '50000')
    # modify_ab_config_upload('false', 'true', 'true', '50000', '50000')
    # # modify_2_config_upload('false', 'true', 'true', '50000', '50000')
    # # modify_3_config_upload('false', 'true', 'true', '50000', '50000')
    # threads = []
    # t34 = threading.Thread(target=command, args=(cm_command,))
    # t35 = threading.Thread(target=ab_command2, args=(ab_command,))
    # # t36 = threading.Thread(target=command_2, args=(cm_command_2,))
    # # t37 = threading.Thread(target=command_3, args=(cm_command_3,))
    # threads.append(t34)
    # threads.append(t35)
    # # threads.append(t36)
    # # threads.append(t37)
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    # sleep(600)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # kill_1_pid()
    # kill_ab_pid()
    # # kill_2_pid()
    # # kill_3_pid()
    # write_1_cm_result(u'cm上报压力测试-缓存', u'添加到缓存', start_time, end_time)
    # write_ab_cm_result(u'cm上报压力测试-缓存', u'添加到缓存', start_time, end_time)
    # # write_2_cm_result(u'cm上报压力测试-缓存', u'添加到缓存', start_time, end_time)
    # # write_3_cm_result(u'cm上报压力测试-缓存', u'添加到缓存', start_time, end_time)
    # sleep(300)
    #
    # # 上报：5万  device.is.datapoint.sync=ture   device.is.online=true 等待5分钟 都拿两次 10分钟一次 30分钟二次
    # func.log(u'--------开始cm上报压力测试-5万个并发')
    # t38 = threading.Thread(target=command, args=(cm_command,))
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # t38.setDaemon(True)
    # t38.start()
    # sleep(1800)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # kill_1_pid()
    # write_1_cm_result(u'cm上报压力测试-5万', u'第二次', start_time, end_time)
    # sleep(300)
    #
    # # 上报：10万  要连两台 1、device.offset=0   device.limit=50000  2、device.offset=50000   device.limit=50000 等待5分钟 都拿两次 10分钟一次 30分钟二次
    # func.log(u'--------开始cm上报压力测试-10万个并发')
    # threads = []
    # t39 = threading.Thread(target=command, args=(cm_command,))
    # t40 = threading.Thread(target=ab_command2, args=(ab_command,))
    # threads.append(t39)
    # threads.append(t40)
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    # sleep(1800)
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # kill_1_pid()
    # kill_ab_pid()
    # write_1_cm_result(u'cm上报压力测试-10万', u'第二次', start_time, end_time)
    # write_ab_cm_result(u'cm上报压力测试-10万', u'第二次', start_time, end_time)
    # sleep(300)
    #
    # # 上报：20万
    # # func.log(u'--------开始cm上报压力测试-20万个并发')
    # # threads = []
    # # t41 = threading.Thread(target=command, args=(cm_command,))
    # # t42 = threading.Thread(target=ab_command2, args=(ab_command,))
    # # t43 = threading.Thread(target=command_2, args=(cm_command_2,))
    # # t44 = threading.Thread(target=command_2, args=(cm_command_2,))
    # # threads.append(t41)
    # # threads.append(t42)
    # # threads.append(t43)
    # # threads.append(t44)
    # # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # # for t in threads:
    # #     t.setDaemon(True)
    # #     t.start()
    # # sleep(1800)
    # # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # # kill_1_pid()
    # # kill_ab_pid()
    # # kill_2_pid()
    # # kill_3_pid()
    # # write_1_cm_result(u'cm上报压力测试-20万', u'第二次', start_time, end_time)
    # # write_ab_cm_result(u'cm上报压力测试-20万', u'第二次', start_time, end_time)
    # # write_2_cm_result(u'cm上报压力测试-20万', u'第二次', start_time, end_time)
    # # write_3_cm_result(u'cm上报压力测试-20万', u'第二次', start_time, end_time)

    func.log(u'----------------------------cm测试并发结束---- -----------------------')