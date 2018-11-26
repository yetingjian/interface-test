# coding=utf-8
from selenium.webdriver.common.by import By
from test_case.page_obj import loginPage
from test_case.page_obj import base
from selenium.common.exceptions import *
from common import exceluitl as EX, function as func
from base import Page
from time import sleep


class ProductInfo(Page):
    obj = None
    data_path = func.find_path() + '/test_data/devplatform/product_info.xlsx'
    data_sheet = 'locator'
    dev_platform_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'dev_platform_loc'))
    add_product = EX.get_locator_value(data_path, data_sheet, 'add_product_loc')
    product_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'product_loc'))
    quota_sum_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'quota_sum_loc'))
    quota_sum = EX.get_locator_value(data_path, data_sheet, 'quota_sum_loc')
    qrcode_loc = (By.CSS_SELECTOR, EX.get_locator_value(data_path, data_sheet, 'qrcode_loc'))
    check_message = EX.get_locator_value(data_path, data_sheet, 'message_loc')
    select_loc = (By.CSS_SELECTOR, EX.get_locator_value(data_path, data_sheet, 'select_loc'))
    select_item_loc = (By.CSS_SELECTOR, EX.get_locator_value(data_path, data_sheet, 'select_item_loc'))

    def click_main_tab(self, name):
        try:
            lists = self.find_elements(self.dev_platform_loc)
            for i in range(len(lists)):
                if lists[i].text == name:
                    lists[i].click()
                    func.log(u'点击：' + name)
                    sleep(2)
                    break
                elif i == len(lists) - 1:
                    func.log(u'模块【' + name + u'】未找到')
        except Exception:
            func.log(u'【异常】模块【' + name + u'】未找到')
            raise

    def wait_add_product_visible(self):
        func.log(u'等待添加产品按钮可见')
        msg = self.wait_css_locate(self.add_product)
        if msg == 'Y':
            func.log(u'添加产品按钮已可见')
        else:
            func.log(u'【异常】60秒后添加产品按钮仍不可见')

    def wait_quota_visible(self):
        func.log(u'等待quota元素可见')
        msg = self.wait_class_visible(self.quota_sum)
        if msg == 'Y':
            func.log(u'元素已可见')
        else:
            func.log(u'【异常】60秒后元素仍不可见')

    def click_dev_plant(self):
        self.find_element_by_xpath('//body/div[1]/div/div/div[1]/div[1]/div/div[4]/button').click()
        sleep(1)

    def wait_element_visible_by_class(self, name):
        func.log(u'等待' + name + u'元素可见')
        msg = self.wait_class_visible(name)
        if msg == 'Y':
            func.log(u'元素已可见')
        else:
            func.log(u'【异常】60秒后元素仍不可见')

    def click_product_info(self, value_list):
        i = None
        if value_list[0] == u'自动化产品':
            value_list[0] = value_list[0] + func.get_now_date()
        lists = self.find_elements((By.CLASS_NAME, 'nav-item'))
        for i in lists:
            self.move_to_element(i)
            if i.text == value_list[0]:
                pro = i.find_element_by_css_selector('.first-nav-box.hover-bg-color')
                pro.click()
                func.log(u'点击：' + value_list[0])
                break
        info = i.find_elements_by_css_selector('.second-nav-item.hover-bg-color')
        for j in info:
            if j.text == value_list[1]:
                j.click()
                func.log(u'点击：' + value_list[1])
                break

    def search_product_and_click(self, value_list):
        value_list[0] = value_list[0] + func.get_now_date()
        input_text = self.find_element((By.XPATH, u'//input[@placeholder="请输入关键字"]'))
        input_text.send_keys(value_list[0])
        search_button = self.find_element((By.CSS_SELECTOR, u'.x-search-box__button.x-btn.x-btn--default.x-btn--small'))
        search_button.click()
        sleep(2)
        lists = self.find_elements((By.XPATH, '//tbody/tr'))
        product_name = self.find_element((By.XPATH, '//table/tbody/tr[%d]/td[1]/div/div/a' %len(lists)))
        product_name.click()

    def search_product(self, value_list):
        value_list[0] = value_list[0] + func.get_now_date()
        input_text = self.find_element((By.XPATH, u'//input[@placeholder="请输入关键字"]'))
        input_text.send_keys(value_list[0])
        search_button = self.find_element((By.CSS_SELECTOR, u'.x-search-box__button.x-btn.x-btn--default.x-btn--small'))
        search_button.click()
        sleep(2)



    def edit_product(self):
        self.find_element((By.XPATH, '//i[@class="iconfont icon-gengduomore10"]')).click()
        sleep(1)
        lists = self.find_elements((By.CLASS_NAME, 'x-dropdown-item'))
        for i in lists:
            if i.text == u'编辑':
                i.click()
                func.log(u'点击编辑产品')
                sleep(1)
                break

    def config_attr(self, text):
        self.find_element((By.XPATH, '//i[@class="iconfont icon-gengduomore10"]')).click()
        sleep(1)
        lists = self.find_elements((By.CLASS_NAME, 'x-dropdown-item'))
        for i in lists:
            if i.text == u'排序配置':
                i.click()
                func.log(u'点击排序配置')
                sleep(1)
                break
        lists = self.find_elements((By.CSS_SELECTOR, '.x-checkbox-wrapper.x-checkbox-group-item'))
        for i in lists:
            if i.text == text:
                i.find_element(By.CLASS_NAME, 'x-checkbox-input').click()
                func.log(u'勾选 '+text)
                icons = self.find_elements((By.CSS_SELECTOR, '.x-btn.x-btn--primary.x-btn--long.x-btn--small'))
                for j in icons:
                    if j.is_enabled() is True:
                        j.click()
                        func.log(u'添加到显示字段列表')
                        self.click_button(u'确定')
                        break
                else:
                    continue
                break

    def click_trigger(self):
        self.find_element((By.CLASS_NAME, 'trigger')).click()
        func.log(u'点击trigger')

    def get_lable_text(self, text):
        list = self.find_elements((By.CLASS_NAME, 'x-label'))
        for i in range(len(list)):
            if list[i].text == text:
                lists = self.find_elements((By.CLASS_NAME, 'x-val'))
                func.log(u'字段'+text+u'的值为：'+lists[i].text)
                return lists[i].text

    def get_quota(self):
        quota = self.find_element(self.quota_sum_loc).text
        func.log(u'产品配额为：' + quota)
        return quota

    def click_quota(self):
        self.find_element(self.quota_sum_loc).click()

    def get_secret_key(self):
        lists = self.find_elements((By.CLASS_NAME, 'action'))
        for i in lists:
            if i.text == u'产品密钥':
                i.click()
                func.log(u'点击查看产品密钥')
                break
        self.wait_dialog_visible()
        text = self.find_element((By.CLASS_NAME, 'product-key')).text
        func.log(u'产品密钥为：' + text)
        self.close_dialog()
        return text

    def get_qrcode(self):
        lists = self.find_elements((By.CLASS_NAME, 'action'))
        for i in lists:
            if i.text == u'产品二维码':
                i.click()
                func.log(u'点击查看二维码')
                break
        self.wait_dialog_visible()
        qrcode = self.find_element(self.qrcode_loc).text
        func.log(u'产品二维码为：' + qrcode)
        self.close_dialog()
        return qrcode

    def release_product(self):
        self.click_button(u'发布产品')
        self.wait_dialog_visible()
        sleep(1)
        self.find_element((By.XPATH, 'html/body/div[3]/div/div/div/div[3]/div/button[1]')).click()

    def get_product_release_text(self):
        text = self.find_element((By.CSS_SELECTOR, '.fr.x-btn.x-btn--default.x-btn--small')).text
        return text

    def wait_edit_product_page(self):
        func.log(u'等待产品信息编辑页面可见')
        for i in range(60):
            obj = self.find_element((By.CLASS_NAME, 'main-title'))
            if obj.text.find(u'产品设置') >= 0:
                func.log(u'产品信息编辑页面已可见')
                return True
        else:
            return False

    def wait_register_page(self):
        func.log(u'等待设备注册页面可见')
        for i in range(60):
            obj = self.find_element((By.CSS_SELECTOR, '.main-title.bordered'))
            if obj.text.find(u'设备注册') >= 0:
                func.log(u'设备注册页面已可见')
                return True
        else:
            return False

    def add_attr(self):
        button = self.find_element((By.CLASS_NAME, 'add-attr-btn'))
        button.click()
        func.log(u'点击添加属性按钮')

    def click_tab_item(self, value_list):
        lists = self.find_elements((By.CLASS_NAME, 'x-tabs__item'))
        for i in lists:
            if i.text == value_list[1]:
                i.click()
                func.log(u'点击 '+value_list[1]+'tab')
                break

    def get_attr_value(self, texts):
        lists = self.find_elements((By.CSS_SELECTOR, '.x-form-item__label'))
        for i in range(len(lists)):
            if lists[i].text == texts:
                message = self.find_element_by_xpath("//form/div[" + str(i + 1) + "]/div/div/div[1]/input")
                func.log(u'属性名【' + texts + u'】的值为：' + message.get_attribute('value'))
                return message.get_attribute('value')

    def get_date_attr_value(self, texts):
        lists = self.find_elements((By.CSS_SELECTOR, '.x-form-item__label'))
        for i in range(len(lists)):
            if lists[i].text == texts:
                message = self.find_element_by_xpath("//form/div[" + str(i + 1) + "]/div/div/div[1]/div[1]/div/input")
                func.log(u'属性名【' + texts + u'】的值为：' + message.get_attribute('value'))
                return message.get_attribute('value')

    def input_para_name(self, text):
        try:
            obj = self.find_element((By.XPATH, u'//input[@placeholder="例：y_voltage_rated"]'))
            if text != '':
                self.clear(obj)
                obj.send_keys(text)
                func.log(u'字段名输入：' + text)
        except Exception:
            func.log(u'【异常】字段名未找到')
            raise

    def input_attr_name(self, text):
        try:
            obj = self.find_element((By.XPATH, u'//input[@placeholder="例：额定电压"]'))
            if text != '':
                self.clear(obj)
                obj.send_keys(text)
                func.log(u'属性名称输入：' + text)
        except Exception:
            func.log(u'【异常】属性名称未找到')
            raise

    def input_text_len(self, text):
        try:
            obj = self.find_element((By.XPATH, u'//input[@placeholder="例：10"]'))
            if text != '':
                self.clear(obj)
                obj.send_keys(text)
                func.log(u'文本长度输入：' + text)
        except Exception:
            func.log(u'【异常】文本长度未找到')
            raise

    def input_init_value(self, text):
        try:
            obj = self.find_element((By.XPATH, u'//input[@placeholder="例：240V"]'))
            if text != '':
                self.clear(obj)
                obj.send_keys(text)
                func.log(u'初始值输入：' + text)
        except Exception:
            func.log(u'【异常】初始值未找到')
            raise

    def input_descript(self, text):
        try:
            obj = self.find_element((By.XPATH, u'//textarea[@placeholder="例：额定电压属性"]'))
            if text != '':
                self.clear(obj)
                obj.send_keys(text)
                func.log(u'描述输入：' + text)
        except Exception:
            func.log(u'【异常】描述未找到')
            raise

    def input_float_len(self, text):
        try:
            obj = self.find_element((By.XPATH, u'//input[@placeholder="例：1"]'))
            if text != '':
                self.clear(obj)
                obj.send_keys(text)
                func.log(u'小数长度输入：' + text)
        except Exception:
            func.log(u'【异常】小数长度未找到')
            raise

    def input_unit(self, text):
        try:
            obj = self.find_element((By.XPATH, u'//input[@placeholder="例：V"]'))
            if text != '':
                self.clear(obj)
                obj.send_keys(text)
                func.log(u'单位输入：' + text)
        except Exception:
            func.log(u'【异常】单位未找到')
            raise

    def input_init_value_number(self, text):
        try:
            obj = self.find_element((By.XPATH, u'//input[@placeholder="例：240V"]'))
            if text != '':
                self.clear(obj)
                obj.send_keys(text)
                func.log(u'初始值输入：' + text)
        except Exception:
            func.log(u'【异常】初始值未找到')
            raise

    def input_attr_name_date(self, text):
        try:
            obj = self.find_element((By.XPATH, u'//input[@placeholder="例：生产日期"]'))
            if text != '':
                self.clear(obj)
                obj.send_keys(text)
                func.log(u'属性名称输入：' + text)
        except Exception:
            func.log(u'【异常】属性名称未找到')
            raise

    def input_descript_date(self, text):
        try:
            obj = self.find_element((By.XPATH, u'//textarea[@placeholder="例：制造产品的日期"]'))
            if text != '':
                self.clear(obj)
                obj.send_keys(text)
                func.log(u'描述输入：' + text)
        except Exception:
            func.log(u'【异常】描述未找到')
            raise

    def delete_attr(self, value_list):
        lists = self.find_elements((By.CSS_SELECTOR, '.x-form-item__label'))
        for i in range(len(lists)):
            if lists[i].text == value_list[1]:
                del_button = self.find_element_by_xpath("//form/div[" + str(i + 1) + "]/div/div/div[2]/i[2]")
                del_button.click()
                func.log(u'点击 '+value_list[1]+u'属性的删除按钮')
                break
        self.wait_dialog_visible()
        sleep(1)
        obj = self.find_element((By.XPATH, u'//input[@placeholder="立即执行"]'))
        obj.send_keys(value_list[4])
        func.log(u'输入：'+value_list[4])
        self.click_button(u'确定')

    def edit_attr(self, value_list):
        lists = self.find_elements((By.CSS_SELECTOR, '.x-form-item__label'))
        for i in range(len(lists)):
            if lists[i].text == value_list[1]:
                del_button = self.find_element_by_xpath("//form/div[" + str(i + 1) + "]/div/div/div[2]/i[1]")
                del_button.click()
                func.log(u'点击 '+value_list[1]+u'属性的编辑按钮')
                break
        self.input_attr_name(value_list[6])
        self.input_text_len(value_list[7])
        self.click_button(u'保存')

    def check_lable_in_page(self, texts):
        lists = self.find_elements((By.CSS_SELECTOR, '.x-form-item__label'))
        for i in range(len(lists)):
            if lists[i].text == texts:
                return True
            elif i == len(lists)-1 and lists[i].text != texts:
                return False

    def delete_product(self):
        checkbox = self.find_element((By.CSS_SELECTOR, '.x-checkbox-input'))
        checkbox.click()
        self.click_button(u'提交')
        self.wait_dialog_visible()
        sleep(1)
        obj = self.find_element((By.XPATH, u'//input[@placeholder="立即执行"]'))
        obj.send_keys(u'立即执行')
        func.log(u'输入立即执行')
        self.click_button(u'确定')

    def delete_checkbox_check(self):
        try:
            self.find_element((By.CLASS_NAME, 'x-checkbox-input'))
            func.log(u'删除产品的checkbox存在')
            return True
        except NoSuchElementException:
            func.log(u'删除产品的checkbox不存在')
            return False

    def click_upload_img(self):
        self.find_element((By.XPATH, '//form/div[1]/div/div/div/label')).click()
        func.log(u'点击上传图片按钮')

    def wait_count_visible(self):
        func.log(u'等待count元素可见')
        msg = self.wait_class_visible('count')
        if msg == 'Y':
            func.log(u'元素已可见')
            return True
        else:
            func.log(u'【异常】60秒后元素仍不可见')
            return False

    def click_mac(self, text):
        objs = self.find_elements((By.CLASS_NAME, 'hl-primary'))
        for i in objs:
            if i.text == text and i.is_displayed():
                i.click()
                func.log(u'点击mac：'+text)
                break
        else:
            func.log(u'mac：' + text + u'未找到')

    def click_sn(self, mac):
        lines = self.find_elements((By.XPATH, '//table/tr'))
        lines = len(lines) - 2
        for i in range(lines):
            mac_name = self.find_element((By.XPATH, "//table/tr[%d]/td[1]/div/a" % (i + 1))).text
            if mac_name == mac:
                sn = self.find_element((By.XPATH, "//table/tr[%d]/td[5]/div/a" % (i + 1)))
                sn.click()
                func.log(u'点击sn：' + sn.text)
                break

    def input_sn(self, text):
        self.wait_dialog_visible()
        input_sn = self.find_element((By.XPATH, u'//input[@placeholder="请输入序列号"]'))
        self.clear(input_sn)
        input_sn.send_keys(text)
        func.log(u'输入sn：' + text)
        self.click_button(u'确定')

    def get_sn(self, mac):
        lines = self.find_elements((By.XPATH, '//table/tr'))
        lines = len(lines) - 2
        for i in range(lines):
            mac_name = self.find_element((By.XPATH, "//table/tr[%d]/td[1]/div/a" % (i + 1))).text
            if mac_name == mac:
                sn = self.find_element((By.XPATH, "//table/tr[%d]/td[5]/div/a" % (i + 1)))
                func.log(u'sn为：' + sn.text)
                return sn.text

    def click_search_type(self, name):
        lists = self.find_elements((By.CLASS_NAME, 'x-select__selected-value'))
        for i in lists:
            if i.text == u'MAC地址':
                i.click()
                break
        sleep(1)
        items = self.find_elements((By.CLASS_NAME, 'x-select-item'))
        for i in items:
            if i.text == name:
                i.click()
                func.log(u'选择筛选类型为：' + name)
                break

    def click_statue_type(self, name):
        lists = self.find_element((By.XPATH, '//header/div[1]/div/div[1]/div[1]/span[2]'))
        lists.click()
        sleep(1)
        items = self.find_elements((By.CLASS_NAME, 'x-select-item'))
        for i in items:
            if i.text == name:
                i.click()
                func.log(u'选择筛选状态为：' + name)
                break

    def click_search_button(self):
        button = self.find_element((By.CSS_SELECTOR,'.x-search-box__button.x-btn.x-btn--default.x-btn--small'))
        button.click()
        func.log(u'点击查询：')

    def input_search_text(self, text):
        obj = self.find_element((By.XPATH, '//header/div[2]/div/div/div[2]/input'))
        obj.send_keys(text)
        func.log(u'查询条件输入：'+text)

    def get_result_rows(self):
        rows = self.find_elements((By.XPATH, '//table/tr'))
        return len(rows) - 1

    def input_device_id(self,text):
        did = self.find_element((By.XPATH, '//table/tr[1]/td[2]/div')).text
        obj = self.find_element((By.XPATH, '//header/div[2]/div/div/div[2]/input'))
        if text == 'all':
            obj.send_keys(did)
            func.log(u'查询条件输入：' + did)
        elif text == 'fuzzy':
            obj.send_keys(did[:3])
            func.log(u'查询条件输入：' + did[:3])
        else:
            obj.send_keys(text)
            func.log(u'查询条件输入：' + text)





















