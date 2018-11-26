# encoding: utf-8
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from common import function as func
from time import sleep
from selenium.common.exceptions import *
import SendKeys


handel = None


class Page(object):
    u'''页面继承类，用于所有页面的继承'''

    host = "http://dev-admin.xlink.cn/v5.3.2"
    V4_host = 'https://admin.xlink.cn/#!'
    #host = "http://admin-test.xlink.io:1081"
    plant_url = host + "/#/auth/login"
    home_page = host + "/#/apps/home"
    V4_home_page = host + '/home'

    # def __init__(self, selenium_driver, parent=None):
    #     self.base_url = Page.plant_url
    #     self.driver = selenium_driver
    #     self.timeout = 30
    #     self.parent = parent

    def __new__(cls, selenium_driver):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Page, cls).__new__(cls)
            cls.driver = selenium_driver
            cls.base_url = Page.plant_url
        return cls._instance

    def __del__(self):
        pass

    def find_element(self, loc):
        return self.driver.find_element(*loc)

    def find_child_element(self, parent_loc, child_loc):
        elem = self.driver.find_element(*parent_loc)
        child = elem.find_element(*child_loc)
        return child

    def find_elements(self, loc):
        return self.driver.find_elements(*loc)

    def open(self):
        self.driver.get(self.base_url)
        #assert self.on_page(), u'未能正确打开指定网页'

    def script(self, src):
        self.driver.execute_script(src)

    def clear_input_text(self, loc):
        obj = self.driver.find_element(*loc)
        self.clear(obj)

    def wait_class_visible(self, _str):
        for i in range(60):
            try:
                obj = self.find_element((By.CLASS_NAME, _str))
                if obj.is_displayed():
                    return 'Y'
                else:
                    sleep(1)
                    continue
            except Exception:
                sleep(1)
        else:
            return 'N'

    def wait_element_visible_by_class_with_text(self, name, text):
        func.log(u'等待' + text + u'元素可见')
        msg = self.wait_class_visible_text(name, text)
        if msg == 'Y':
            func.log(u'元素已可见')
            return 'Y'
        else:
            func.log(u'【异常】60秒后元素仍不可见')
            return 'N'

    def wait_element_visible_by_css_with_text(self, name, text):
        func.log(u'等待' + text + u'元素可见')
        msg = self.wait_css_visible_text(name, text)
        if msg == 'Y':
            func.log(u'元素已可见')
            return 'Y'
        else:
            func.log(u'【异常】60秒后元素仍不可见')
            return 'N'

    def wait_class_visible_text(self, _str, text):
        for i in range(60):
            try:
                obj = self.find_element((By.CLASS_NAME, _str))
                if obj.is_displayed() and obj.text == text:
                    return 'Y'
                else:
                    sleep(1)
                    continue
            except Exception:
                sleep(1)
                continue
        else:
            return 'N'

    def wait_id_visible(self, _str):
        for i in range(60):
            try:
                if self.find_element((By.ID, _str)).is_displayed():
                    return 'Y'
            except Exception:
                sleep(1)
        else:
            return 'N'

    def wait_css_visible(self, _str):
        for i in range(60):
            try:
                if self.find_element((By.CSS_SELECTOR, _str)).is_displayed():
                    return 'Y'
            except Exception:
                sleep(1)
        else:
            return 'N'

    def wait_css_visible_text(self, _str, text):
        for i in range(60):
            try:
                obj = self.find_element((By.CSS_SELECTOR, _str))
                if obj.is_displayed() and obj.text == text:
                    return 'Y'
                else:
                    sleep(1)
                    continue
            except Exception:
                sleep(1)
                continue
        else:
            return 'N'

    @staticmethod
    def wait_css_locate(_str):
        for i in range(60):
            if EC.visibility_of_element_located((By.CSS_SELECTOR, _str)):
                sleep(1)
                return 'Y'
            elif i == 59:
                return 'N'
            else:
                sleep(1)

    def wait_button_visible(self, name):
        for i in range(60):
            buttons = self.find_elements((By.TAG_NAME, 'button'))
            for j in buttons:
                if j.text == name and j.is_displayed():
                    return 'Y'
                elif i == 59:
                    return 'N'
                else:
                    sleep(1)

    def wait_text_visible(self, loc, text):
        for i in range(60):
            obj = self.find_element(loc)
            if obj.is_displayed() and obj.text == text:
                return 'Y'
            elif i == 59:
                return 'N'
            else:
                sleep(1)

    def wait_obj_enabled(self, loc, text):
        for i in range(60):
            obj = self.driver.find_element(*loc)
            if obj.text == text and obj.is_enabled():
                return 'Y'
            elif i == 59:
                return 'N'
            else:
                sleep(1)

    def wait_obj_disabled(self, loc, text):
        for i in range(60):
            obj = self.driver.find_element(*loc)
            if obj.text == text and not obj.is_enabled():
                return 'Y'
            elif i == 59:
                return 'N'
            else:
                sleep(1)

    def get_host(self):
        lists = self.plant_url.split('#')
        return lists[0]

    def on_page(self):
        return self.driver.current_url == self.base_url

    def get_current_url(self):
        return self.driver.current_url

    def _open(self, url):
        url = self.base_url + url
        self.driver.get(url)
        self.wait_class_visible('account')
        assert self.on_page(), u'未能正确打开指定网页'

    def click_button(self, text):
        try:
            buttons = self.driver.find_elements_by_tag_name('button')
            for i in range(len(buttons)):
                if buttons[i].text == text and buttons[i].is_displayed():
                    buttons[i].click()
                    func.log(u'点击按钮：' + text)
                    break
                elif i == len(buttons)-1:
                    func.log(u'【异常】按钮【' + text + u'】未找到')
        except Exception:
            func.log(u'【异常】按钮【' + text + u'】未找到')
            raise

    def click_obj(self, loc, text):
        if text != '':
            try:
                objs = self.find_elements(loc)
                for i in range(len(objs)):
                    if objs[i].text == text:
                        objs[i].click()
                        func.log(u'点击对象：' + text)
                        break
            except Exception:
                func.log(u'【异常】对象' + text + u'未找到')
                raise

    def click_obj_by_class(self, loc):
        try:
            objs = self.find_elements((By.CLASS_NAME, loc))
            for i in range(len(objs)):
                if objs[i].is_displayed():
                    objs[i].click()
                    func.log(u'点击对象：' + loc)
                    break
        except Exception:
            func.log(u'【异常】对象' + loc + u'未找到')
            raise

    def click_obj_by_css(self, loc):
        try:
            objs = self.find_elements((By.CSS_SELECTOR, loc))
            for i in range(len(objs)):
                if objs[i].is_displayed():
                    objs[i].click()
                    func.log(u'点击对象：' + loc)
                    break
        except Exception:
            func.log(u'【异常】对象' + loc + u'未找到')
            raise

    def find_element_by_xpath(self, loc):
        return self.driver.find_element_by_xpath(loc)

    def open_url(self, url):
        self.driver.get(self.get_host() + url)

    def open_url_with_host(self, url):
        self.driver.get(url)

    def open_home_page(self):
        self.driver.get(self.home_page)

    def open_V4_home_page(self):
        self.driver.get(self.V4_home_page)

    def refresh_page(self):
        self.driver.refresh()

    def move_to_element(self, obj):
        self.driver.execute_script("arguments[0].scrollIntoView();", obj)

    def mouse_move_to(self, obj):
        ActionChains(self.driver).move_to_element(obj).perform()

    def element_select_item(self, obj_name, item, obj_loc, item_loc, case_name):
        if item != '':
            self.find_element(obj_loc).click()
            sleep(1)
            try:
                list1 = self.find_elements(item_loc)
                for j in range(len(list1)):
                    self.move_to_element(list1[j])
                    if list1[j].text == item:
                        list1[j].click()
                        func.log(obj_name + u'选择' + item)
                        break
                    elif j == len(list1) - 1:
                        raise NoFoundItemException
            except NoFoundItemException:
                func.log(u'【异常】' + obj_name + u'选项' + item + u'未找到')
                func.scream_shot(self.driver, case_name + '.jpg')
                raise

    def element_select_item_by_div_title(self, obj_name, item, obj_loc, case_name):
        if item != '':
            self.find_element(obj_loc).click()
            sleep(1)
            try:
                obj = self.find_elements((By.XPATH, '//div[@title="'+item+'"]'))
                for i in obj:
                    if i.is_displayed() is True:
                        i.click()
                        func.log(obj_name + u'选择' + item)
                        break
            except NoFoundItemException:
                func.log(u'【异常】' + obj_name + u'选项' + item + u'未找到')
                func.scream_shot(self.driver, case_name + '.jpg')
                raise

    def wait_dialog_visible(self):
        func.log(u'等待对话框出现')
        for i in range(60):
            lists = self.find_elements((By.CLASS_NAME, 'x-modal-dialog'))
            for j in lists:
                if j.is_displayed():
                    func.log(u'对话框已可见')
                    break
            else:
                sleep(1)
                continue
            break

    def input_text(self, text, content):
        if content != '':
            try:
                lists = self.find_elements((By.CSS_SELECTOR, '.x-form-item__label'))
                for i in range(len(lists)):
                    if lists[i].text == text:
                        obj = self.find_element_by_xpath("//form/div[" + str(i + 1) + "]/div/div/input")
                        self.clear(obj)
                        if content != u'空':
                            obj.send_keys(content)
                            func.log(text + u'输入：' + content)
                            break
            except Exception:
                func.log(u'【异常】' + text + u'输入框未找到')
                raise

    def clear(self, obj):
        obj.click()
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        ActionChains(self.driver).key_down(Keys.DELETE).key_up(Keys.DELETE).perform()

    def input_textarea(self, text, content):
        if content != '':
            try:
                lists = self.find_elements((By.CSS_SELECTOR, '.x-form-item__label'))
                for i in range(len(lists)):
                    if lists[i].text == text:
                        obj = self.find_element_by_xpath("//form/div[" + str(i + 1) + "]/div/div/textarea")
                        self.clear(obj)
                        if content != u'空':
                            obj.send_keys(content)
                        func.log(text + u'输入：' + content)
                        break
            except Exception:
                func.log(u'【异常】' + text + u'输入框未找到')
                raise

    def select_text1(self, text, item):
        if item != '':
            try:
                lists = self.find_elements((By.CSS_SELECTOR, '.x-form-item__label'))
            except Exception:
                func.log(u'【异常】' + text + u'选择框未找到')
                raise
            try:
                for i in range(len(lists)):
                    if lists[i].text == text:
                        obj = self.find_element_by_xpath("//form/div[" + str(i + 1) + "]/div/div/div/div[1]")
                        obj.click()
                        obj.click()
                        sleep(1)
                        list1 = self.find_elements((By.CLASS_NAME, "x-tree-title-wrap"))
                        for j in range(len(list1)):
                            self.move_to_element(list1[j])
                            if list1[j].text == item:
                                list1[j].click()
                                list1[j].click()
                                sleep(1)
                                lists[i].click()
                                sleep(1)
                                func.log(text + u'选择：' + item)
                                break
                            elif j == len(list1) - 1 and list1[j].text != item:
                                raise NoFoundItemException
                        break
            except NoFoundItemException:
                func.log(u'【异常】选项' + item + u'未找到')
                raise

    def select_text2(self, text, item):
        if item != '':
            try:
                lists = self.find_elements((By.CSS_SELECTOR, '.x-form-item__label'))
            except Exception:
                func.log(u'【异常】' + text + u'选择框未找到')
                raise
            try:
                for i in range(len(lists)):
                    if lists[i].text == text:
                        obj = self.find_element_by_xpath("//form/div[" + str(i + 1) + "]/div/div/div")
                        obj.click()
                        sleep(1)
                        list1 = self.find_elements((By.CSS_SELECTOR, '.x-select-item'))
                        for j in range(len(list1)):
                            self.move_to_element(list1[j])
                            if list1[j].text == item:
                                list1[j].click()
                                sleep(1)
                                func.log(text + u'选择：' + item)
                                break
                            elif j == len(list1) - 1 and list1[j].text != item:
                                raise NoFoundItemException
                        break
            except NoFoundItemException:
                func.log(u'【异常】选项' + item + u'未找到')
                raise

    def error_message(self):
        try:
            text = self.find_element((By.CLASS_NAME, 'x-message')).text
            func.log(u'错误提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】错误提示未找到')
            raise

    def wait_message_visible(self):
        func.log(u'等待x-message元素可见')
        msg = self.wait_class_visible('x-message')
        if msg == 'Y':
            func.log(u'元素已可见')
        else:
            func.log(u'【异常】60秒后元素仍不可见')

    def get_message(self):
        try:
            text = self.find_element((By.CLASS_NAME, 'x-message')).text
            func.log(u'提示信息：' + text)
            return text
        except Exception:
            func.log(u'【异常】提示信息未找到')
            raise

    def get_error_message(self, text):
        try:
            lists = self.find_elements((By.CSS_SELECTOR, '.x-form-item__label'))
            for i in range(len(lists)):
                if lists[i].text == text:
                    message = self.find_element_by_xpath("//form/div[" + str(i + 1) + "]/div/div[2]").text
                    func.log(text + u'错误时提示信息：' + message)
                    return message
        except Exception:
            func.log(u'【异常】错误时提示未找到')
            raise

    def get_error_by_class(self):
        try:
            lists = self.find_element((By.CLASS_NAME, 'x-form-item__error'))
            func.log(u'错误时提示信息：' + lists.text)
            return lists.text
        except Exception:
            func.log(u'【异常】错误时提示未找到')
            raise

    def input_date(self, text, placeholder):
        a = 0
        if text != '':
            date_list = text.split('-')
            year = date_list[0]
            month = date_list[1]
            day = date_list[2]
            obj = self.find_element((By.XPATH, u'//input[@placeholder="' + placeholder + '"]'))
            obj.click()
            sleep(1)
            lists = self.find_elements((By.CLASS_NAME, 'x-date-picker-header-label'))
            lists[0].click()
            for i in range(100):
                year_list = self.find_elements((By.XPATH, '//em[@index="' + year[-1] + '"]'))
                year_min = self.find_elements((By.XPATH, '//em[@index="0"]'))
                year_max = self.find_elements((By.XPATH, '//em[@index="9"]'))
                if year_list[1].text == year:
                    year_list[1].click()
                    break
                elif int(year_min[1].text) > int(year):
                    left_icon = self.find_elements((By.CSS_SELECTOR, '.iconfont.icon-angle-double-left'))
                    left_icon[1].click()
                elif int(year_max[1].text) < int(year):
                    left_icon = self.find_element((By.CSS_SELECTOR, '.iconfont.icon-angle-double-right'))
                    left_icon.click()
            month_list = self.find_elements((By.XPATH, '//em[@index="' + str(int(month) - 1) + '"]'))
            for j in month_list:
                if j.is_displayed():
                    j.click()
                    break
            day_list = self.find_elements((By.XPATH, '//span[@class="x-date-picker-cells__cell"]'))
            for k in day_list:
                if k.is_displayed() and int(day) == int(k.text):
                    day_ele = k.find_element(By.TAG_NAME, 'em')
                    day_ele.click()
                    day_ele.click()
                    a = 1
                    break
            if a == 0:
                day_list = self.find_element((By.XPATH, '//span[@class="x-date-picker-cells__cell x-date-picker-cells__cell--today"]'))
                day_ele = day_list.find_element(By.TAG_NAME, 'em')
                day_ele.click()
                day_ele.click()
            button = self.find_element((By.CSS_SELECTOR, '.x-btn.x-btn--primary.x-btn--mini'))
            button.click()
            func.log(u'日期选择：' + text)

    def close_dialog(self):
        lists = self.find_elements((By.CSS_SELECTOR, '.close-icon.iconfont.icon-guanbi'))
        for i in lists:
            if i.is_displayed():
                i.click()
                func.log(u'点击关闭对话框')
                break

    def upload_file(self, path):
        SendKeys.SendKeys(path)
        sleep(3)
        SendKeys.SendKeys('{ENTER}')
        sleep(1)
        SendKeys.SendKeys('{ENTER}')


    def get_upload_file_src(self):
        try:
            obj = self.find_element((By.TAG_NAME, 'img'))
            func.log(u'图片上传成功,路径为：'+obj.get_attribute('src'))
            return True
        except NoSuchElementException:
            func.log(u'删除产品的checkbox不存在')
            return False

    def get_obj_text_by_class(self, _str):
        return self.find_element((By.CLASS_NAME, _str)).text


class NoFoundItemException(Exception):

    def __init__(self):
        pass






