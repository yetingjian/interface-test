from ParametrizedTestCase import ParametrizedTestCase
from xlinkutils import Xlink_Utils


class DeviceInit(ParametrizedTestCase):

    def __init__(self, methodName='runTest', param=None):
        super().__init__(methodName, param)
        self.device=param['device']


    def test_getPidPkey(self):
        self.device.get_pid_pkey()

    def test_getMac(self):
        self.device.get_mac()

    def test_get_connect_statue(self):
        self.device.get_connect_statue()

