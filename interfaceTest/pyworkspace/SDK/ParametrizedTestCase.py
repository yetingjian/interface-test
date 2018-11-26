import unittest

from xlinkutils.xlog import XLog


class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """

    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param

    @staticmethod
    def parametrize(testcase_klass, param=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite

    def assertRet(self, ret, data):
        request = ret[0]
        result = ret[1]
        if 'error' in result.keys():
            self.assertTrue(False, '\r\ndata: ' + data + '\r\nrequest:' + str(request) + '\r\nresult:' + str(result))
