 #coding=utf-8
# 导游端APP测试

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import HTMLTestRunner
import time
import unittest
from appium import webdriver
from time import sleep
import re
import xlrd
import os
timestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

# def mkdir(path):
#      # 去除首位空格
#      path = path.strip()
#      # 去除尾部 \ 符号
#      path = path.rstrip("\\")
#
#      # 判断路径是否存在
#      # 存在     True
#      # 不存在   False
#      isExists = os.path.exists(path)
#
#      # 判断结果
#      if not isExists:
#          # 如果不存在则创建目录
#          # print path + ' 创建成功'
#          # 创建目录操作函数
#          os.makedirs(path)
#          return True
#      else:
#          # 如果目录存在则不创建，并提示目录已存在
#          # print path + ' 目录已存在'
#          return False
#
#  # 定义要创建的目录
# mkpath = ".\\report\\"   + os.environ["ymd"]
# # mkpath = ".\\report\\"
#  # 调用函数
# mkdir(mkpath)

class LoadBaiduSearchTestData:
    def __init__(self, path):
        self.path = path

    def load_data(self):
        # 打开excel文件
        excel = xlrd.open_workbook(self.path)
        # 获取第一个工作表
        table = excel.sheets()[0]
        # 获取行数
        nrows = table.nrows

        # 从第二行开始遍历数据
        # 存入一个list中
        test_data = []
        for i in range(1, nrows):
            test_data.append(table.row_values(i))

            # 返回读取的数据列表
        return test_data

class ContactsAndroidTests(unittest.TestCase):

    def setUp(self):
        desired_caps = {'platformName': 'Android',
                        'platformVersion': '4.4.2',
                        'deviceName': '127.0.0.1:62001',#62001
                        'appPackage': 'com.euet.guider',
                        'appActivity': 'com.euet.guider.ui.login.activity.SplashActivity',
                        'unicodeKeyboard': (True,),
                        'resetKeyboard': True}
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub',desired_caps)#10.10.66.50  127.0.0.1

    def tearDown(self):
        self.driver.close_app()
        self.driver.quit()

    # 获得机器屏幕大小x,y
    def getSize(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        print u'x坐标=', x
        print u'y坐标=', y
        return (x, y)


    def swipelocation(self, t, xb1, yb1, xb2,yb2):
        l = self.getSize()
        x1 = int(l[0] * xb1)  # x坐标
        y1 = int(l[1] * yb1)  # 起始y坐标
        x2 = int(l[0] * xb2)  # x终点坐标
        y2 = int(l[1] * yb2)  # 终点y坐标
        self.driver.swipe(x1, y1, x2, y2, t)


    # 屏幕向上滑动
    def swipeUp(self, t, xb1, yb1, yb2):  # t=拖动时间 ; xb1=X坐标比例位置 ; yb1=起始y坐标比例位置 ;yb2=终点y坐标比例位置
        #备注：xb1,yb1为操作起始点位置坐标比例，xb2,yb2为操作结束点位置坐标比例，都是相对的，不是绝对，根据滑动方向而定
        l = self.getSize()
        x1 = int(l[0] * xb1)  # x坐标
        y1 = int(l[1] * yb1)  # 起始y坐标
        y2 = int(l[1] * yb2)  # 终点y坐标
        self.driver.swipe(x1, y1, x1, y2, t)

    # 屏幕向下滑动
    def swipeDown(self, t, xb1, yb1, yb2):
        l = self.getSize()
        x1 = int(l[0] * xb1)  # x坐标
        y1 = int(l[1] * yb1)  # 起始y坐标
        y2 = int(l[1] * yb2)  # 终点y坐标
        self.driver.swipe(x1, y1, x1, y2, t)

    # 屏幕向左滑动
    def swipLeft(self, t, xb1, yb1, xb2):
        l = self.getSize()
        x1 = int(l[0] * xb1)
        y1 = int(l[1] * yb1)
        x2 = int(l[0] * xb2)
        self.driver.swipe(x1, y1, x2, y1, t)

    # 屏幕向右滑动
    def swipRight(self, t, xb1, yb1, xb2):
        l = self.getSize()
        x1 = int(l[0] * xb1)
        y1 = int(l[1] * yb1)
        x2 = int(l[0] * xb2)
        self.driver.swipe(x1, y1, x2, y1, t)

    def screenshot(self,pngname):
        timestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        img_name = pngname + timestr + '.png'
        png_file = "D:\\appium_report\\png\\"
        self.driver.get_screenshot_as_file('%s%s' % (png_file, img_name))
        print u'截图位置:',png_file
        print u'截图名称:',img_name

    def Add_group_sucess(self):
         u'''判断是否获取到上团标题'''
         self.screenshot("Add_group_sucess") #截图
         try:
            text = self.driver.find_element('name', '行程已创建成功！').text
            print '标题='+text

            return True
         except:
             return False

    def Test_guider_login(self):
        # u"""导游登录"""
        time.sleep(8)
        # 点击使用密码登录
        self.driver.find_element('id', 'com.euet.guider:id/tv_login_password').click()
        # 点击注册账号
        # self.driver.find_element('id','com.euet.guider:id/tv_regist').click()
        # 输入手机号
        self.driver.find_element('id', 'com.euet.guider:id/et_phone').send_keys("18802036336")
        # 等待2秒
        time.sleep(2)
        # 输入密码
        self.driver.find_element('id', 'com.euet.guider:id/et_password').send_keys("123456")
        # self.driver.find_element('id','com.euet.guider:id/bnt_yanzheng').click()
        # 获取按钮文本内容
        anniu = self.driver.find_element('id', 'com.euet.guider:id/bnt_regist').text
        # 点击登录按钮或注册按钮
        self.driver.find_element('id', 'com.euet.guider:id/bnt_regist').click()
        print "登陆成功"
        time.sleep(5)
        # 打印获取到的信息
        print("anniu")

    def Test_Guider_Login_mm(self):
        u"""密码登陆"""
        time.sleep(5)
        # self.swipLeft(1000, 0.8, 0.5, 0.2)
        # self.swipLeft(1000, 0.8, 0.5, 0.2)
        # self.swipLeft(1000, 0.8, 0.5, 0.2)
        # self.swipLeft(1000, 0.8, 0.5, 0.2)
        # self.swipLeft(1000, 0.8, 0.5, 0.2)
        # self.driver.find_element_by_name('跳过').click()
        # time.sleep(2)
        # 使用密码登陆
        self.driver.find_element_by_id('com.euet.guider:id/tv_login_password').click()
        time.sleep(5)
        #输入手机号
        self.driver.find_element_by_id('com.euet.guider:id/et_phone').send_keys('18802036336')
        #输入验证码
        self.driver.find_element_by_id('com.euet.guider:id/et_password').send_keys('123456')
        #点击登陆
        self.driver.find_element_by_id('com.euet.guider:id/bnt_regist').click()
        time.sleep(2)
        zy = self.driver.find_element('id', 'com.euet.guider:id/tv_title_center').text
        print ("zy")
        if(zy == "领路人"):
            print u"登陆成功"
        else:
            print u"登陆失败"

    def Test_Guider_review(self):
        u"""游记评论"""
        time.sleep(3)
        self.driver.find_elements('id', 'com.euet.guider:id/tab_indicator_icon')[3].click()
        self.driver.find_element('id', 'com.euet.guider:id/iv_comment').click()
        self.driver.find_element('name', '请输入要评论的内容').send_keys(u'评论测试')
        self.driver.find_element('name', '发送').click()

    def Test_Guider_Login_yzm(self):
        # 输入手机号
        time.sleep(5)
        self.driver.find_element_by_id('com.euet.guider:id/et_phone').send_keys("18802036336")
        # 输入万能验证码前4位
        self.driver.find_element_by_id('com.euet.guider:id/et_vercode').send_keys("8954")
        # 再次点击验证码
        # self.driver.find_element_by_id('com.euet.guider:id/et_vercode').click()
        # 输入万能验证码后2位
        # self.driver.swipe(765,1300,765,1300,1)
        self.driver.find_element_by_id('com.euet.guider:id/et_vercode').send_keys("89")
        # 点击登陆
        self.driver.find_element_by_id('com.euet.guider:id/bnt_regist').click()

    def Test_Guider_logout(self):
        u"""退出登录"""
        time.sleep(5)
        self.driver.find_element('id', 'com.euet.guider:id/tiv_mine').click()
        time.sleep(2)
        self.driver.find_element_by_name('设置').click()
        self.driver.find_element_by_name('退出登录').click()
        self.driver.find_element_by_name('确定').click()
        time.sleep(2)
        zy = self.driver.find_element('id', 'com.euet.guider:id/bnt_regist').text
        print ("zy")
        if(zy == "登录"):
            print u"退出成功"
        else:
            print u"退出失败"

    def Test_route_edit(self):
        u"""添加行程照片"""
        time.sleep(5)
        self.driver.find_element_by_name('详情').click()
        time.sleep(5)
        self.driver.find_element_by_id('com.euet.guider:id/iv_title_right').click()
        time.sleep(3)
        s = self.driver.find_elements_by_class_name('android.widget.ImageView')
        a = len(s) - 1
        u"""添加图片"""
        self.driver.find_elements_by_class_name('android.widget.ImageView')[a].click()
        time.sleep(3)
        self.driver.find_element_by_name('从相册上传行程信息').click()
        x = self.driver.find_elements('id', 'com.euet.guider:id/iv_thumb_check')
        for j in range(len(x) - 1, len(x)):
            x[j].click()
            time.sleep(2)
        self.driver.find_element_by_id('com.euet.guider:id/btn_ok').click()
        print u"""行程图片添加成功"""

    def Test_route_delete(self):
        u"""删除行程照片"""
        time.sleep(5)
        self.driver.find_element_by_name('详情').click()
        time.sleep(5)
        self.driver.find_element_by_id('com.euet.guider:id/iv_title_right').click()
        u"""删除图片"""
        time.sleep(3)
        s = self.driver.find_elements_by_class_name('android.widget.ImageView')
        b = len(s) - 3
        self.driver.find_elements_by_class_name('android.widget.ImageView')[b].click()
        time.sleep(2)
        self.driver.find_element('name', '完成').click()
        print u"""行程图片删除成功"""
        self.driver.find_element('id', 'com.euet.guider:id/rl_title_back').click()

    def Test_Add_group(self):
        u"""新增团信息"""
        time.sleep(5)
        # 点击"+"号
        self.driver.find_element('id', 'com.euet.guider:id/iv_title_right').click()
        # 上传行程信息图片
        self.driver.find_element('name', '从相册上传行程信息').click()
        # self.driver.find_element_by_name('从相册上传行程信息').click()
        # # 上传名单com.euet.guider:id/bnt_up_mingdan
        # self.driver.find_element('id', 'com.euet.guider:id/image_view_album_image').click()
        sleep(1)
        # 截图
        self.screenshot(u'上传行程图片')
        # 选择图片
        xuan = self.driver.find_elements('id', 'com.euet.guider:id/iv_thumb_check')
        for i in range(len(xuan)-3, len(xuan)):
            print i, xuan[i].id
            xuan[i].click()
        self.driver.find_element('id', 'com.euet.guider:id/btn_ok').click()
        time.sleep(5)
        # 请输入行程名称
        self.driver.find_element('id', 'com.euet.guider:id/et_trip_name').send_keys(u"广州2日游"+timestr)
        # 请输入团号
        self.driver.find_element('id', 'com.euet.guider:id/et_trip_num').send_keys("123456")
        # 接团日期
        self.driver.find_element('id', 'com.euet.guider:id/ll_start_time').click()
        # self.swipeUp(1000, 0.54, 0.94, 0.47)        #选择月
        # self.swipeUp(1000, 0.65, 0.94, 0.58)        #选择日
        # self.driver.flick(380,1138,380,380)
        sleep(1)
        self.driver.find_element('name', '确定').click()
        # 送团日期
        self.driver.find_element('id', 'com.euet.guider:id/ll_end_time').click()
        self.swipeUp(100, 0.54, 0.94, 0.47)        #选择月
        self.swipeUp(500, 0.65, 0.94, 0.58)        #选择日
        self.driver.find_element('name', '确定').click()
        time.sleep(5)
        # # 请输入行程备注
        # self.driver.find_element('id', 'com.euet.guider:id/et_beizhu').send_keys(u"飞机在飞")
        # 行程信息
        # time.sleep(1)
        # # 上传行程图片(使用坐标点击事件)
        # self.swipeUp(1, 0.13, 0.73, 0.73)
        # # self.driver.find_element_by_class_name('android.widget.ImageView').click()
        # time.sleep(1)
        self.driver.find_element('name','下一步').click()
        # time.sleep(1)
        # # 点击拍照按钮
        # self.driver.find_element('id','com.android.camera:id/v6_shutter_button_internal').click()
        # time.sleep(2)
        # # 点击确定钩钩
        # self.driver.find_element('id','com.android.camera:id/v6_btn_done').click()

        # print ("看看就行")
        # self.driver.find_element('id','com.euet.guider:id/et_vercode').send_keys("12345")
        time.sleep(5)
        self.driver.find_element_by_id('com.euet.guider:id/ll_shoudong').click()
        self.driver.find_element_by_id('com.euet.guider:id/et_name').send_keys(u"测试")
        self.driver.find_element_by_id('com.euet.guider:id/et_phone').send_keys("18800000020")
        self.driver.find_element_by_id('com.euet.guider:id/bnt_save').click()
        time.sleep(8)
        # 判断结果
        result = self.Add_group_sucess()
        self.assertTrue(result)   #u"""上团结果"""
        #添加团成员
        # n = 9
        # while n > 0:
        #     n = n - 1
        #     name = u'乔峰'
        #     phone = str(13719214566 + n)
        #     print phone
        #     self.Add_user(name,phone)

    def Test_Groupping(self):
        u"""查看出团中信息"""
        time.sleep(8)
        self.driver.find_element_by_name('出团中').click()
        try:
            self.driver.find_element('id', 'com.euet.guider:id/tv_title').text == "详情"
            print u"出团中查看成功"
        except:
            self.driver.find_element('id', 'com.euet.guider:id/tv_no_date').text == "今日无出团"
            print u"出团中查看成功（暂时没有出团中信息）"

    def Test_The_group(self):
        u"""查看即将出团信息"""
        time.sleep(8)
        # 即将出团
        self.driver.find_element('name', '出团列表').click()
        # # 获取团名称
        # self.driver.get_screenshot_as_file('D:/appium_report/The_group.png')
        # var = self.driver.find_element('id', 'com.euet.guider:id/tv_name').text
        # # print(var)
        # # 这里用的css语法
        # s = self.driver.find_elements('id', 'com.euet.guider:id/tv_name')
        # # '获取即将出团名称'
        # for i in range(0, len(s)):
        #     print i, s[i].text
        try:
            self.driver.find_element('id', 'com.euet.guider:id/tv_time').text != 'null'
            print u"即将出团查看成功"
        except:
            self.driver.find_element('id', 'com.euet.guider:id/tv_no_date').text =="近期无出团安排"
            print  u"即将出团查看成功（暂时没有即将出团信息）"

    def Test_Add_tally_income(self):
        u"""记账-收入"""
        sleep(5)
        self.driver.find_element('name','记账').click()
        # '输入金额'
        self.driver.find_element('name','收入').click()
        self.driver.find_element('id','com.euet.guider:id/et_totle').send_keys('20')
        self.driver.find_element('name','保存').click()
        # 进入记账模块
        self.driver.find_element('name', '记账').click()
        # 查看账单
        self.driver.find_element('id','com.euet.guider:id/iv_title_right').click()
        sleep(2)
        # 获取每条金额数据对象
        s = self.driver.find_elements('id', 'com.euet.guider:id/tv_money')
        # '获取账单金额数据'
        hj = 0.0
        for i in range(0, len(s)):
            print i, s[i].text
            m = s[i].text
            # 将正则表达式编译成Pattern对象
            pattern = re.compile(r'[1-9]\d*\.\d*|0\.\d*[1-9]\d*$')
            # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
            match = pattern.search(m)
            print u'人民币', match.group()
            hj = hj + float(match.group())
            print u'合计:', hj
        sz=self.driver.find_element('id','com.euet.guider:id/tv_shou_zhi').text
        print u'总收支:',sz

    def Test_Add_bill_expenditure(self):
        u"""记账-支出"""
        # print "支出测试"
        time.sleep(5)
        #点击记账
        self.driver.find_element_by_name('记账').click()
        #选择类型-支出
        self.driver.find_element_by_name('支出').click()
        #输入金额
        self.driver.find_element_by_name('请输入您的金额').send_keys("5")
        #点击支出类型
        self.driver.find_element_by_id('com.euet.guider:id/ll_canyin').click()
        #选择支出类型-其他
        self.driver.find_element_by_name('其他').click()
        #选择金额类型
        self.driver.find_element_by_id('com.euet.guider:id/ll_xianjin').click()
        #选择支付类型微信
        self.driver.find_element_by_name('微信').click()
        #选择记账时间
        # self.driver.find_element_by_id('com.euet.guider:id/tv_naozhong').click()
        # time.sleep(2)
        # self.swipeUp(1000, 0.50, 0.62, 0.40)
        # self.swipeUp(1000, 0.57, 0.92, 0.62)
        # time.sleep(2)
        # self.driver.find_element_by_name('确定').click()
        self.driver.find_element_by_name('保存').click()
        # self.driver.find_element_by_id('com.euet.guider:id/bnt_baocun').click()
        time.sleep(5)
        # 进入记账模块
        self.driver.find_element('name', '记账').click()
        # 查看账单
        self.driver.find_element('id','com.euet.guider:id/iv_title_right').click()
        sleep(2)
        # 获取每条金额数据对象
        s = self.driver.find_elements('id', 'com.euet.guider:id/tv_money')
        # '获取账单金额数据'
        hj = 0.0
        for i in range(0, len(s)):
            print i, s[i].text
            m = s[i].text
            # 将正则表达式编译成Pattern对象
            pattern = re.compile(r'[1-9]\d*\.\d*|0\.\d*[1-9]\d*$')
            # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
            match = pattern.search(m)
            print u'人民币', match.group()
            hj = hj + float(match.group())
            print u'合计:', hj
        sz=self.driver.find_element('id','com.euet.guider:id/tv_shou_zhi').text
        print u'总收支:',sz

    def Test_user_sign(self):
        u"""点名-整组签到"""
        #点击点名
        time.sleep(5)
        self.driver.find_element_by_name('点名').click()
        self.driver.find_element_by_name('开始点名').click()
        time.sleep(2)
        #点击整组签到
        self.driver.find_element_by_id('com.euet.guider:id/ll_qianzhu').click()
        q = self.driver.find_element('id', 'com.euet.guider:id/tv_quanzhu').text
        time.sleep(2)
        if(q == "已到"):
            print u"整组签到成功"
        else:
            print u"整组签到失败"
        # 取消整组签到
        self.driver.find_element_by_id('com.euet.guider:id/ll_qianzhu').click()
        z = self.driver.find_element('id', 'com.euet.guider:id/tv_quanzhu').text
        time.sleep(2)
        if(z == "未到"):
            print u"整组签退成功"
        else:
            print u"整组签退失败"
        time.sleep(2)
        self.driver.find_element_by_name('结束点名').click()

    def Test_user_single(self):
        u"""单个签到"""
        time.sleep(5)
        self.driver.find_element('name','点名').click()
        time.sleep(3)
        self.driver.find_element_by_name('开始点名').click()
        time.sleep(5)
        s = self.driver.find_elements('id','com.euet.guider:id/tv_zuzhang')      #com.euet.guider:id/ll_baodao
        for i in range(0 ,len(s)):
            s[i].click()
            print i,s[i].text
            z = self.driver.find_element('id', 'com.euet.guider:id/tv_zuzhang').text
            if (z == "已到"):
                print u"单人签到成功"
            else:
                print u"单人签到失败"
            time.sleep(2)
        self.driver.find_element('name','结束点名').click()

    def Test_user_edit(self):
        u""""成员编辑测试"""
        # 点击成员
        time.sleep(5)
        self.driver.find_element_by_name('成员').click()
        time.sleep(3)
        # 向左滑动游客名单
        self.swipLeft(1000,0.9,0.2,0.45)
        # self.driver.swipe(711,300,372,300,1000)     #滑动正常
        time.sleep(5)
        # 点击编辑
        self.driver.find_element_by_id('com.euet.guider:id/tv_edite').click()
        # 修改姓名
        time.sleep(3)
        self.driver.find_element_by_id('com.euet.guider:id/et_name').clear()
        self.driver.find_element_by_id('com.euet.guider:id/et_name').send_keys(u"大白菜")
        y = self.driver.find_element_by_id('com.euet.guider:id/et_name').text
        time.sleep(3)
        # 点击修改性别
        self.driver.find_element_by_id('com.euet.guider:id/ll_sex').click()
        # 选择修改性别
        self.driver.find_element_by_name('女').click()
        # 点击保存
        self.driver.find_element_by_id('com.euet.guider:id/bnt_save').click()
        s = self.driver.find_elements('id', 'com.euet.guider:id/tv_name')
        for i in range(0,len(s)):
            try:
                s[i] = y
                print u"编辑成功"
                return True
            except:
                return False
        #点击返回按钮
        self.driver.find_element_by_id('com.euet.guider:id/rl_title_back').click()

    def Test_user_delete(self):
        u"""团成员删除"""
        # 点击成员
        time.sleep(5)
        self.driver.find_element_by_name('成员').click()
        time.sleep(2)
        # 向左滑动游客名单
        self.swipLeft(1000, 0.9, 0.2, 0.45)
        # 点击删除
        time.sleep(2)
        self.driver.find_element_by_id('com.euet.guider:id/tv_delete').click()
        time.sleep(2)
        self.swipLeft(1000, 0.9, 0.2, 0.45)
        # 点击删除
        time.sleep(2)
        self.driver.find_element_by_id('com.euet.guider:id/tv_edite').click()
        self.driver.find_element('id', 'com.euet.guider:id/rl_title_back').click()

    def Test_user_group(self):
        u"""成员分组"""
        time.sleep(5)
        self.driver.find_element('name', '成员').click()
        time.sleep(2)
        self.driver.find_element('id', 'com.euet.guider:id/iv_title_right').click()
        self.driver.find_element('name', '成员分组').click()
        time.sleep(2)
        self.driver.find_element('name', '新增分组').click()
        time.sleep(2)
        self.driver.find_element('id', 'com.euet.guider:id/et_content').send_keys(u'一组')
        time.sleep(2)
        self.driver.find_element('name', '添加组员').click()
        time.sleep(2)
        self.driver.find_elements('id', 'com.euet.guider:id/iv_check')[0].click()
        self.driver.find_element('name', '确定').click()
        time.sleep(2)
        self.driver.find_element('id', 'com.euet.guider:id/tv_title_right').click()
        time.sleep(2)
        self.driver.find_element('id', 'com.euet.guider:id/rl_title_back').click()
        time.sleep(5)
        self.driver.find_element('id', 'com.euet.guider:id/rl_title_back').click()

    def Test_Room_Assingment(self):
        u"""按性别分房"""
        # 点击分房
        time.sleep(5)
        self.driver.find_element_by_name('分房').click()
        #点击类型选择按
        self.driver.find_element_by_id('com.euet.guider:id/iv_title_right').click()
        #点击自动分房
        self.driver.find_element_by_id('com.euet.guider:id/tv_all_see').click()
        #选择按性别自动分房
        self.driver.find_element_by_id('com.euet.guider:id/tv_aoto_seprate').click()
        #点击确定按钮
        self.driver.find_element_by_id('com.euet.guider:id/bnt_ok').click()
        time.sleep(5)
        #点击返回按钮
        self.driver.find_element_by_id('com.euet.guider:id/rl_title_back').click()

    def Test_Room_Assingment_group(self):
        u"""按分组分房"""
        # 点击分房
        time.sleep(5)
        self.driver.find_element_by_name('分房').click()
        #点击类型选择按
        time.sleep(5)
        self.driver.find_element_by_id('com.euet.guider:id/iv_title_right').click()
        #点击自动分房
        self.driver.find_element_by_id('com.euet.guider:id/tv_all_see').click()
        time.sleep(2)
        #选择按分组自动分房
        # self.driver.find_element_by_name('按分组自动分房').click()
        self.driver.find_element_by_id('com.euet.guider:id/tv_sex_seprate').click()
        time.sleep(3)
        #点击确定按钮
        # self.driver.find_element_by_id('com.euet.guider:id/bnt_ok').click()
        self.driver.find_element('name','确定').click()

    def Test_Room_Assingment_handwork(self):
        u"""手工分房"""
        time.sleep(5)
        self.driver.find_element_by_name('分房').click()
        self.driver.find_elements('name','未分配')[0].click()
        self.swipelocation(1, 0.28, 0.89, 0.35, 0.95)
        # self.driver.find_elements_by_class_name('android.widget.LinearLayout')[0].click()
        # self.driver.find_elements_by_class_name('android.widget.LinearLayout')
        time.sleep(3)
        # w = self.driver.find_elements_by_class_name('android.widget.LinearLayout')
        # for i in range(0, 1):
        #     print w[i].click()
        # self.driver.find_element_by_id('com.euet.guider:id/iv_sex').click()
        # 点击返回按钮
        self.driver.find_element_by_id('com.euet.guider:id/rl_title_back').click()


    def Test_Add_user(self,name,card,phone):
        u"""团成员为空时,添加团成员"""
        time.sleep(2)
        # 点击手工添加
        try:
           text = self.driver.find_element('id', 'com.euet.guider:id/ll_shoudong').text
           print text
           self.driver.find_element('id', 'com.euet.guider:id/ll_shoudong').click()
        except:
            # 获取已添加成员信息
            s = self.driver.find_elements('id', 'com.euet.guider:id/tv_name')
            p = self.driver.find_elements('id', 'com.euet.guider:id/tv_zuzhang')
            # 打印'成员'名称和手机号
            for i in range(0, len(s)):
                print i, '姓名:' + s[i].text, '手机号:' + p[i].text
            self.driver.find_element('id', 'com.euet.guider:id/rl_title_right').click()
            self.driver.find_element('name', '增加成员').click()
            sleep(1)
            self.driver.find_element('name','单个添加').click()
        time.sleep(1)
        # 填写成员信息
        self.driver.find_element('id', 'com.euet.guider:id/et_name').send_keys(name)
        self.driver.find_element('id', 'com.euet.guider:id/et_cardId').send_keys(card)
        self.driver.find_element('id', 'com.euet.guider:id/et_phone').send_keys(phone)
        self.driver.find_element('id', 'com.euet.guider:id/et_urgent_person').send_keys("13580254613")
        self.driver.find_element('id', 'com.euet.guider:id/et_beizhu').send_keys(u"开飞机的成员")
        self.driver.find_element('id', 'com.euet.guider:id/bnt_save').click()

    def Test_Add_user2(self):
        u"""团成员非空时,添加团成员"""
        # 加载测试数据
        test_excel = LoadBaiduSearchTestData(u'游客名单.xls')
        data = test_excel.load_data()
        # print data
        time.sleep(8)
        # 点击成员按钮
        self.driver.find_element('name', '成员').click()
        time.sleep(2)
        for d in data:
        #     n = 9
        # while n > 0:
        #     n = n - 1
        #     name = u'乔峰'
        #     phone = str(13719214566 + n)
            name = b[1]
            # card = d[4]
            phone = e[5]
            # name = d[1]
            # card=d[4]
            # phone =d[5]
            print name
            print card
            print phone
            self.Test_Add_user(name,card,phone)
    def Test_Cut_group(self):
        u"""切换出团中的信息"""
        sleep(8)
        self.driver.find_element('name','切换团').click()
        self.Test_Add_user2()

    def Test_Notes(self):
        u"""发送通知"""
        time.sleep(5)
        self.driver.find_element_by_name('通知').click()
        #发送集合通知
        self.driver.find_element_by_id('com.euet.guider:id/et_remark').send_keys(u"集合通知发送测试")
        self.driver.find_element_by_id("com.euet.guider:id/bnt_sent").click()
        time.sleep(2)
        #发送公告通知
        self.driver.find_element_by_name('通知').click()
        self.driver.find_element_by_name('集合').click()
        self.driver.find_element_by_name('公告').click()
        time.sleep(2)
        self.driver.find_element_by_id('com.euet.guider:id/et_remark').send_keys(u"公告通知发送测试")
        self.driver.find_element_by_id("com.euet.guider:id/bnt_sent").click()

    def Test_Notes_timekeeper(self):
        u"""发送通知"""
        time.sleep(5)
        self.driver.find_element('name', '通知').click()
        time.sleep(2)
        self.driver.find_element('name', '集合').click()
        time.sleep(2)
        self.driver.find_element('name', '闹钟').click()
        time.sleep(2)
        self.driver.find_element('name', '提醒时间').click()
        self.swipeUp(500, 0.47, 0.92, 0.53)        #天数选择
        self.swipeUp(1000, 0.57, 0.92, 0.62)        #时间选择
        time.sleep(2)
        self.driver.find_element('name', '确定').click()
        time.sleep(2)
        self.driver.find_element('id', 'com.euet.guider:id/et_remark').send_keys(u'闹钟测试')
        time.sleep(2)
        self.driver.find_element('name', '发送').click()

    def Test_Notes_number(self):
        u"""已阅读通知人数检查"""
        time.sleep(5)
        self.driver.find_element('name', '通知').click()
        # self.driver.swipe(795,1296,1020,1386,1)
        self.swipelocation(1, 0.80, 0.68, 0.90, 0.71)
        time.sleep(5)

    def Test_Guider_group_chat(self):
        u"""团聊天发送"""
        #点击聊天
        time.sleep(3)
        self.driver.find_elements('id', 'com.euet.guider:id/tab_indicator_icon')[1].click()
        self.driver.find_element('id' ,'com.euet.guider:id/rl_add').click()
        #选择第一条团聊信息
        self.driver.find_elements('id','com.euet.guider:id/groupitem')[0].click()
        time.sleep(2)
        #发送文字内容
        self.driver.find_element('id','android:id/edit').send_keys(u'团聊消息发送')
        self.driver.find_element('name', '发送').click()
        time.sleep(3)
        #发送表情
        self.driver.find_element('id', 'android:id/icon').click()
        self.driver.find_elements('id','com.euet.guider:id/rc_emoji_item')[0].click()
        self.driver.find_element('name', '发送').click()
        #发送图片
        self.driver.find_element('id', 'android:id/icon2').click()
        self.driver.find_element('name', '图片').click()
        # 选择图片
        time.sleep(3)
        xuan = self.driver.find_elements('id', 'com.euet.guider:id/checkbox')
        for i in range(1, 2):
            print i, xuan[i].id
            xuan[i].click()
            time.sleep(2)
        self.driver.find_element('id', 'com.euet.guider:id/send').click()

    def Test_Guider_single_chat(self):
        u"""私聊发送"""
        time.sleep(3)
        self.driver.find_elements('id', 'com.euet.guider:id/tab_indicator_icon')[1].click()
        self.driver.find_element('id', 'com.euet.guider:id/rl_add').click()
        # self.driver.find_element('name', '[4-18]广州2日游2017051810361').click()
        # self.swipelocation(1,0.05,0.11,0.90,0.18)
        self.driver.find_elements('id','com.euet.guider:id/groupitem')[0].click()
        time.sleep(2)
        self.driver.find_element('id','com.euet.guider:id/rl_title_right').click()
        time.sleep(2)
        # self.driver.find_element('name', '18800000021').click()
        # self.swipelocation(1,0.05,0.28,0.90,0.36)
        self.driver.find_elements('id','com.euet.guider:id/frienditem')[0].click()
        time.sleep(2)
        # 发送文字内容
        self.driver.find_element('id', 'android:id/edit').send_keys(u'私聊信息发送')
        self.driver.find_element('name', '发送').click()
        time.sleep(3)

    def Test_Travel_Notes(self):
        u"""导游游记点赞"""
        #点击游记
        time.sleep(5)
        self.driver.find_elements('id', 'com.euet.guider:id/tab_indicator_icon')[3].click()
        self.driver.find_element_by_id('com.euet.guider:id/iv_love').click()

    def Travel_Notes_Publish(self):
        u"""发布游记"""
        sleep(5)
        # 点击游记模块
        self.driver.find_elements('id','com.euet.guider:id/tab_indicator_icon')[3].click()
        # 点击发游记图标
        self.driver.find_element('id','com.euet.guider:id/iv_title_right').click()
        sleep(1)
        self.driver.find_element('name','从手机相册中选择').click()
        sleep(2)
        # 截图
        self.screenshot(u'上传发布游记图片')
        # 选择图片所有图片
        xuan = self.driver.find_elements('id', 'com.euet.guider:id/iv_thumb_check')
        # print u'上传图片数量:',len(xuan)
        for i in range(len(xuan)-3, len(xuan)):
            xuan[i].click()
            time.sleep(2)
        self.driver.find_element('id','com.euet.guider:id/btn_ok').click()
        # 游记标题
        self.driver.find_element('id','com.euet.guider:id/et_say').send_keys(u'游记发表测试')
        # 点击发布按钮
        self.driver.find_element('name','发布').click()

    def Test_Guider_review(self):
        u"""游记评论"""
        time.sleep(3)
        self.driver.find_elements('id','com.euet.guider:id/tab_indicator_icon')[3].click()
        self.driver.find_element('id', 'com.euet.guider:id/iv_comment').click()
        self.driver.find_element('name','请输入要评论的内容').send_keys(u'评论测试')
        self.driver.find_element('name','发送').click()

    def Test_Guider_information(self):
        u"""短信群发"""
        time.sleep(5)
        self.driver.find_element_by_name('成员').click()
        #点击短信群发选项
        self.driver.find_element_by_id('com.euet.guider:id/iv_title_right').click()
        self.driver.find_element_by_name('短信群发').click()
        time.sleep(10)
        #输入短信内容
        self.driver.find_element_by_id('com.euet.guider:id/et_input').send_keys(u'短信群发测试')
        self.driver.find_element_by_name('发送').click()

    def Test_Guider_map(self):
        u"""定位"""
        #查看位置
        # self.swipelocation(0.47, 0.96,0.53,0.99,1)
        time.sleep(3)
        self.driver.find_element('id', 'com.euet.guider:id/tiv_positon').click()
        # self.driver.find_element('id','com.euet.guider:id/iv_circle').click()
def Test_all():
    Test_all = unittest.TestSuite()
    Test_all.addTest(ContactsAndroidTests("Test_Guider_Login_mm"))     # 密码登录
    # Test_all.addTest(ContactsAndroidTests("Test_The_group"))       #查看即将出团信息
    # Test_all.addTest(ContactsAndroidTests("Test_Add_group"))        # 新增团信息
    # Test_all.addTest(ContactsAndroidTests("Test_Groupping"))       #查看出团中信息
    # Test_all.addTest(ContactsAndroidTests("Test_user_edit"))       #编辑成员
    # Test_all.addTest(ContactsAndroidTests("Test_user_delete"))     #删除成员
    # Test_all.addTest(ContactsAndroidTests("Test_user_group"))        #成员分组
    # Test_all.addTest(ContactsAndroidTests("Test_Room_Assingment"))     #按性别自动分房
    # Test_all.addTest(ContactsAndroidTests("Test_Add_tally_income"))        #收入
    # Test_all.addTest(ContactsAndroidTests("Test_Add_bill_expenditure"))        #添加支出
    # Test_all.addTest(ContactsAndroidTests("Test_user_sign"))     #整组签到
    # Test_all.addTest(ContactsAndroidTests("Test_Notes"))           #集合、公告通知发送
    Test_all.addTest(ContactsAndroidTests("Test_Guider_logout"))       #退出登陆
    return Test_all
    # unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    # unittest.main(defaultTest= 'Test_all')
    # suite = unittest.TestSuite()
    # suite.addTest(ContactsAndroidTests("Test_all"))
    # suite.addTest(ContactsAndroidTests("Test_Guider_Login_mm"))     # 密码登录
    # suite.addTest(ContactsAndroidTests("Test_The_group"))       #查看即将出团信息
    # suite.addTest(ContactsAndroidTests("Test_Add_group"))        # 新增团信息
    # suite.addTest(ContactsAndroidTests("Test_Groupping"))       #查看出团中信息
    # suite.addTest(ContactsAndroidTests("Test_user_edit"))       #编辑成员
    # suite.addTest(ContactsAndroidTests("Test_user_delete"))     #删除成员
    # suite.addTest(ContactsAndroidTests("Test_user_group"))        #成员分组
    # suite.addTest(ContactsAndroidTests("Test_Room_Assingment"))     #按性别自动分房
    # suite.addTest(ContactsAndroidTests("Test_Add_tally_income"))        #收入
    # suite.addTest(ContactsAndroidTests("Test_Add_bill_expenditure"))        #添加支出
    # suite.addTest(ContactsAndroidTests("Test_user_sign"))     #整组签到
    # suite.addTest(ContactsAndroidTests("Test_Notes"))           #集合、公告通知发送
    # suite.addTest(ContactsAndroidTests("Test_Guider_logout"))       #退出登陆
    runner = unittest.TextTestRunner()
    runner.run(Test_all())
    # timestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    # filename = "E:\\test-reports\\result_" + timestr + ".html"
    #
    # # #相对路径
    # # result_file = mkpath + "\\result\\"
    # # mkdir(result_file)
    # # # print (os.environ["ymd"])
    # # filename = result_file + "trade_" + os.environ["ymd"] + ".html"
    # # # filename = result_file + "trade_" + ".html"
    #
    # fp = open(filename, 'wb')
    # runner = HTMLTestRunner.HTMLTestRunner(
    #     stream=fp,
    #     title='导游端测试结果',
    #     description='领路人APP导游端测试报告'
    # )
    # # # suite = unittest.TestLoader().loadTestsFromTestCase(ContactsAndroidTests)
    # # # unittest.TextTestRunner(verbosity=2).run(suite)
    # # # runner = unittest.TextTestRunner()
    # # runner.run(suite)
    # # # g_browser.quit()
    # fp.close()  # 测试报告关闭
