import logging
from logging.handlers import RotatingFileHandler
import sys
import os

# XLOG_FILENAME = "xlinkptp.log"
XLOG_FILENAME = 'AutomationTesting.log'

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
LOG_FILEPATH = os.path.join(LOG_DIR, XLOG_FILENAME)
class XLog:
    __log_instance = None

    def __init__(self):
        pass

    @staticmethod
    def GetLogger():
        if XLog.__log_instance is None:
            XLog.__log_instance = logging.getLogger()
            XLog.__log_instance.setLevel(logging.DEBUG)

            terminal = logging.StreamHandler(sys.stdout)
            terminal.setLevel(logging.DEBUG)
            terminal.setFormatter(
                logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                  '%a, %d %b %Y %H:%M:%S'))
            XLog.__log_instance.addHandler(terminal)
            # log_dir = '/tmp/logs/'
            log_dir = LOG_DIR
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            # log_file = log_dir
            # log_file += XLOG_FILENAME
            log_file = LOG_FILEPATH
            file_out = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=2)
            file_out.setLevel(logging.DEBUG)
            file_out.setFormatter(
                logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                  '%a, %d %b %Y %H:%M:%S'))
            XLog.__log_instance.addHandler(file_out)

        return XLog.__log_instance


if __name__ == '__main__':
    XLog.GetLogger().info("Hello info log")
    XLog.GetLogger().warn("Hello warn log")
