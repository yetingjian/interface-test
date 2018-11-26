from ParametrizedTestCase import ParametrizedTestCase
from xlinkutils.Xlink_Utils import find_path, get_user_list
from xlinkutils.xlog import XLog




class Login(ParametrizedTestCase):

    def __init__(self, methodName='runTest', param=None):
        super().__init__(methodName, param)
        self.app = self.param['app']
        self.app.userName = self.param['user'][self.app.client_id]['用户账号']
        self.app.password = self.param['user'][self.app.client_id]['用户密码']
        self.app.corp_id = self.param['user'][self.app.client_id]['企业id']


    def test_01_start_sdk(self):
        ret = self.app.start_sdk()
        self.assertRet(ret, '启动sdk失败')
        XLog.GetLogger().info("start_sdk ret result %s!", ret[1])

    def test_02_sdk_login(self):
        ret = self.app.user_auth()
        self.assertRet(ret,'登录用户失败 : username:'+self.app.userName + 'password:'+self.app.password)
        XLog.GetLogger().info("sdk_login ret result %s!",ret[1])






