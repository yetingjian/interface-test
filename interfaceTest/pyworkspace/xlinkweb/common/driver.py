from selenium.webdriver import Remote
from selenium import webdriver
#driver = None


def broswer():
    host = 'http://127.0.0.1:4444/wd/hub'
    dc = {'platform':'ANY',
          'browserName':'firefox',
          'version':'',
          'javascriptEnabled':True,
          'marionette':False
         }

    driver = Remote(command_executor=host, desired_capabilities=dc)
    return driver


def broswer_no_remote():
    driver = webdriver.Chrome()
    return driver


class Broswer(object):
    __dirver = None

    @classmethod
    def get_instance(cls):
        if cls.__dirver is None:
            cls.__dirver = Broswer.__broswer_no_remote()
        return cls.__dirver

    @staticmethod
    def __broswer_no_remote():
        #global driver
        # directory = r'C:\Users\wq\AppData\Roaming\Mozilla\Firefox\Profiles\l1obfdm3.default'
        profile = webdriver.Chrome()
        profile.assume_untrusted_cert_issuer = True
        profile.accept_untrusted_certs = True
        driver = webdriver.Chrome(profile)
        return driver


if __name__ == '__main__':
    dr = broswer_no_remote()
    # dr.get("http://admin-test.xlink.io:1081/#/auth/login")
    # dr.quit()
    # print id(Broswer.get_instance())
    # print id(Broswer.get_instance())
    # print id(Broswer.get_instance())