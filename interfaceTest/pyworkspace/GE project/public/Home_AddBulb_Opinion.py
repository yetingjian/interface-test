#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from time import sleep
sys.path.append("C:\Users\Demon\Desktop\GE project\public")
from Start import ContactsAndroid
from TimeOut import Time

def AddBulb_Opinion(self):
    try:
        self.assertIsNone(self.driver.find_element('name', 'Add a bulb').text, ',没有添加灯按钮')
        self.driver.find_element('name', 'Add a bulb').click()
        sleep(3)
    except:
        ContactsAndroid().swipeUp(1000,0.8,0.8,0.2)
        # ContactsAndroid(1000,0.8,0.8,0.2).swipeUp()
        # ContactsAndroid().swipeUp(1000, 0.8, 0.8, 0.2)
        sleep(3)
        self.driver.find_element('name', 'Add a bulb').click()
        sleep(3)