# coding=utf-8
from selenium.webdriver.common.by import By
from test_case.page_obj import loginPage
from test_case.page_obj import base
from common import exceluitl as EX, function as func
from base import Page
from time import sleep


class CreateProduct(Page):

    data_path = func.find_path() + '/test_data/devplatform/create_product.xlsx'
    data_sheet = 'locator'
    dev_platform_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'dev_platform_loc'))
    add_product = EX.get_locator_value(data_path, data_sheet, 'add_product_loc')
    add_product_loc = (By.CSS_SELECTOR, EX.get_locator_value(data_path, data_sheet, 'add_product_loc'))
    input_loc = (By.CSS_SELECTOR, EX.get_locator_value(data_path, data_sheet, 'input_loc'))
    create_success_loc = (By.CSS_SELECTOR, EX.get_locator_value(data_path, data_sheet, 'create_success_loc'))
    create_success = EX.get_locator_value(data_path, data_sheet, 'create_success_loc')
    select_loc = (By.CSS_SELECTOR, EX.get_locator_value(data_path, data_sheet, 'select_loc'))
    select_item_loc = (By.CSS_SELECTOR, EX.get_locator_value(data_path, data_sheet, 'select_item_loc'))
    sys_point_id_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'sys_point_id_loc'))
    sys_point_id_item_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'sys_point_id_item_loc'))
    radio_item_loc = (By.CSS_SELECTOR, EX.get_locator_value(data_path, data_sheet, 'radio_item_loc'))
    point_cancel_loc = (By.CSS_SELECTOR, EX.get_locator_value(data_path, data_sheet, 'point_cancel_loc'))
    point_sequence_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'first_point_sequence_loc'))
    point_type_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'point_type_loc'))
    point_id_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'point_id_loc'))
    point_name_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'point_name_loc'))
    point_save_loc = (By.CSS_SELECTOR, EX.get_locator_value(data_path, data_sheet, 'point_save_loc'))
    add_data_point = EX.get_locator_value(data_path, data_sheet, 'add_data_point_loc')
    add_data_point_loc = (By.CSS_SELECTOR, EX.get_locator_value(data_path, data_sheet, 'add_data_point_loc'))
    data_type_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'data_type_loc'))
    unit_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'unit_loc'))
    descript_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'descript_loc'))
    read_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'read_loc'))
    error_message_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'error_message_loc'))
    check_error_message = EX.get_locator_value(data_path, data_sheet, 'error_message_loc')
    point_type_item_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'point_type_item_loc'))
    data_type_item_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'data_type_item_loc'))
    read_type_item_loc = (By.CLASS_NAME, EX.get_locator_value(data_path, data_sheet, 'read_type_item_loc'))
    min_value_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'min_value_loc'))
    max_value_loc = (By.XPATH, EX.get_locator_value(data_path, data_sheet, 'max_value_loc'))
    dialog_loc = EX.get_locator_value(data_path, data_sheet, 'dialog_loc')
    mod_page_title = EX.get_locator_value(data_path, data_sheet, 'mod_page_title_loc')
    data_point_type_value = None
    data_point_id_value = None
    data_point_name_value = None
    data_type_value = None
    data_unit_value = None
    data_discript_value = None
    data_read_value = None
    mod_data_point_count = None

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

    def click_dev_plant(self):
        self.find_element_by_xpath('//body/div[1]/div/div/div[1]/div[1]/div/div[4]/button').click()
        sleep(1)

    def click_add_product(self):
        lists = self.find_elements(self.dev_platform_loc)
        try:
            for i in lists:
                if i.text == u'开发平台':
                    self.mouse_move_to(i)
                    sleep(1)
                    items = self.find_elements(self.add_product_loc)
                    for j in items:
                        if j.text == u'创建产品':
                            j.click()
                            sleep(1)
                            func.log(u'点击创建产品')
                    break
        except Exception:
            func.log(u'【异常】【创建产品】按钮未找到')
            raise

    def wait_add_data_point_button_visible(self):
        func.log(u'等待添加数据端点按钮可见')
        msg = self.wait_css_visible(self.add_data_point)
        if msg == 'Y':
            func.log(u'元素已可见')
        else:
            func.log(u'【异常】60秒后元素仍不可见')

    def wait_add_product_visible(self):
        func.log(u'等待添加产品按钮可见')
        msg = self.wait_css_locate(self.add_product)
        if msg == 'Y':
            func.log(u'添加产品按钮已可见')
        else:
            func.log(u'【异常】60秒后添加产品按钮仍不可见')

    def wait_element_visible_by_class(self, name):
        func.log(u'等待' + name + u'元素可见')
        msg = self.wait_class_visible(name)
        if msg == 'Y':
            func.log(u'元素已可见')
        else:
            func.log(u'【异常】60秒后元素仍不可见')

    def wait_element_visible_by_css(self, name):
        func.log(u'等待' + name + u'元素可见')
        msg = self.wait_css_visible(name)
        if msg == 'Y':
            func.log(u'元素已可见')
        else:
            func.log(u'【异常】60秒后元素仍不可见')

    def wait_button_visibled(self, name):
        func.log(u'等待' + name + u'按钮可见')
        msg = self.wait_button_visible(name)
        if msg == 'Y':
            func.log(name + u'已可见')
        else:
            func.log(u'【异常】60秒后' + name + u'仍不可见')

    def wait_error_message_visible(self):
        func.log(u'等待' + CreateProduct.check_error_message + u'元素可见')
        msg = self.wait_class_visible(self.check_error_message)
        if msg == 'Y':
            func.log(u'元素已可见')
        else:
            func.log(u'【异常】60秒后元素仍不可见')

    def wait_button_enabled_css(self, text):
        func.log(u'等待' + text + u'按钮可用')
        msg = self.wait_obj_enabled((By.CSS_SELECTOR, self.add_data_point), text)
        if msg == 'Y':
            func.log(text + u'按钮已可用')
            return True
        else:
            func.log(u'【异常】60秒后' + text + u'按钮仍不可用')
            return False

    def wait_button_disabled_css(self, text):
        func.log(u'等待' + text + u'按钮不可用')
        msg = self.wait_obj_disabled((By.CSS_SELECTOR, self.add_data_point), text)
        if msg == 'Y':
            func.log(text + u'按钮已不可用')
            return True
        else:
            func.log(u'【异常】60秒后' + text + u'按钮仍可用')
            return False

    def wait_button_css_visible(self):
        func.log(u'等待添加数据端点按钮元素可见')
        msg = self.wait_css_visible(self.add_data_point)
        if msg == 'Y':
            func.log(u'元素已可见')
        else:
            func.log(u'【异常】60秒后元素仍不可见')

    def count_data_point(self):
        num = self.find_elements((By.CSS_SELECTOR, '.border-bottom'))
        func.log(u'已添加数据端点个数：' + str(len(num)))
        return len(num)

    def count_mod_data_point(self):
        num = self.find_elements((By.XPATH, "//table/tr"))
        func.log(u'已添加数据端点个数：' + str(len(num) - 1))
        return len(num) - 1

    def point_type_select(self, obj_name, item, case_name):
        if item != '':
            self.element_select_item_by_div_title(obj_name, item, self.point_type_loc, case_name)

    def sys_point_id_select(self, obj_name, item, case_name):
        if item != '':
            self.element_select_item_by_div_title(obj_name, item, self.sys_point_id_loc, case_name)

    def data_type_select(self, obj_name, item, case_name):
        if item != '':
            self.element_select_item_by_div_title(obj_name, item, self.data_type_loc, case_name)

    def read_select(self, obj_name, item, case_name):
        if item != '':
            self.element_select_item_by_div_title(obj_name, item, self.read_loc, case_name)

    def input_point_id(self, text):
        if text != '':
            try:
                self.find_element(self.point_id_loc).send_keys(text)
                func.log(u'输入字段名称：' + text)
            except Exception:
                func.log(u'【异常】字段名称输入框未找到')
                raise

    def input_min_value(self, text):
        if text != '':
            try:
                obj = self.find_element(self.min_value_loc)
                obj.clear()
                obj.send_keys(text)
                func.log(u'输入最小值：' + text)
            except Exception:
                func.log(u'【异常】最小值输入框未找到')
                raise

    def input_max_value(self, text):
        if text != '':
            try:
                obj = self.find_element(self.max_value_loc)
                obj.clear()
                obj.send_keys(text)
                func.log(u'输入最大值：' + text)
            except Exception:
                func.log(u'【异常】最大值输入框未找到')
                raise

    def get_min_value(self):
        try:
            obj = self.find_element(self.min_value_loc)
            text = obj.get_attribute('value')
            return text
        except Exception:
            func.log(u'【异常】最小值输入框未找到')
            raise

    def get_max_value(self):
        try:
            obj = self.find_element(self.max_value_loc)
            text = obj.get_attribute('value')
            return text
        except Exception:
            func.log(u'【异常】最大值输入框未找到')
            raise

    def input_unit(self, text):
        if text != '':
            try:
                unit = self.find_element(self.unit_loc)
                unit.clear()
                unit.send_keys(text)
                func.log(u'输入单位：' + text)
            except Exception:
                func.log(u'【异常】单位输入框未找到')
                raise

    def input_point_name(self, text):
        if text != '':
            try:
                point_name = self.find_element(self.point_name_loc)
                point_name.clear()
                point_name.send_keys(text)
                func.log(u'输入单位：' + text)
            except Exception:
                func.log(u'【异常】单位输入框未找到')
                raise

    def input_descript(self, text):
        if text != '':
            try:
                descript = self.find_element(self.descript_loc)
                descript.clear()
                descript.send_keys(text)
                func.log(u'输入描述：' + text)
            except Exception:
                func.log(u'【异常】描述输入框未找到')
                raise

    def click_save(self, text):
        self.click_obj(self.point_save_loc, text)

    def click_cancel(self, text):
        self.click_obj(self.point_cancel_loc, text)

    def is_gateway(self, text):
        if text != '':
            try:
                lists = self.find_elements(self.radio_item_loc)
                if text == u'是':
                    lists[0].click()
                elif text == u'否':
                    lists[1].click()
                func.log(u'是否网关选择：' + text)
            except Exception:
                func.log(u'【异常】是否网关radiobutton未找到')
                raise

    def wait_success_tips_visible(self):
        func.log(u'等待产品创建成功信息出现')
        msg = self.wait_css_locate(self.create_success)
        if msg == 'Y':
            func.log(u'产品创建成功信息已可见')
        else:
            func.log(u'【异常】60秒后产品创建成功信息仍不可见')

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

    def create_success_message(self):
        try:
            text = self.find_element(self.create_success_loc).text
            func.log(u'创建产品成功后页面提示：' + text)
            return text
        except Exception:
            func.log(u'【异常】创建产品成功后页面提示未找到')
            raise

    def edit_input_point_id(self, text):
        if text != '':
            try:
                self.find_element(self.point_id_loc).send_keys(text)
                func.log(u'字段名称输入：' + text)
            except Exception:
                func.log(u'【异常】数据端点id输入框未找到')
                raise

    def edit_input_point_name(self, text):
        if text != '':
            try:
                if text != u'空':
                    self.find_element(self.point_name_loc).send_keys(text)
                    func.log(u'端点名称输入：' + text)
            except Exception:
                func.log(u'【异常】数据端点id输入框未找到')
                raise

    def edit_data_point(self, value_list, case_name):
        row = self.find_elements((By.XPATH, "//tbody"))
        for i in range(len(row)):
            text = self.find_element((By.XPATH, "//tbody[%d]/tr[2]/td[1]" % (i + 1))).text
            if text == value_list[0]:
                CreateProduct.data_point_type_value = (By.XPATH, "//tbody[%d]/tr[2]/td[2]" % (i + 1))
                CreateProduct.data_point_id_value = (By.XPATH, "//tbody[%d]/tr[2]/td[3]" % (i + 1))
                CreateProduct.data_point_name_value = (By.XPATH, "//tbody[%d]/tr[2]/td[4]" % (i + 1))
                CreateProduct.data_type_value = (By.XPATH, "//tbody[%d]/tr[2]/td[5]" % (i + 1))
                CreateProduct.data_unit_value = (By.XPATH, "//tbody[%d]/tr[2]/td[6]" % (i + 1))
                CreateProduct.data_discript_value = (By.XPATH, "//tbody[%d]/tr[2]/td[7]" % (i + 1))
                CreateProduct.data_read_value = (By.XPATH, "//tbody[%d]/tr[2]/td[8]" % (i + 1))
                self.find_element((By.XPATH, "//tbody[%d]/tr[2]/td[9]/a[1]" % (i + 1))).click()
                func.log(u'点击编辑按钮')
                self.wait_button_disabled_css(u'添加数据端点')
                CreateProduct.point_type_loc = (By.XPATH, "//tbody[%d]/tr[1]/td[2]/div/div[1]" % (i + 1))
                CreateProduct.point_type_item_loc = (By.XPATH, "//tbody[%d]/tr[1]/td[2]/div/div[2]/div/div[1]/ul[2]/li"
                                                     % (i + 1))
                CreateProduct.point_name_loc = (By.XPATH, "//tbody[%d]/tr[1]/td[4]/div/div/input" % (i + 1))
                CreateProduct.descript_loc = (By.XPATH, "//tbody[%d]/tr[1]/td[7]/div/div/input" % (i + 1))
                CreateProduct.point_id_loc = (By.XPATH, "//tbody[%d]/tr[1]/td[3]/div/div/input" % (i + 1))
                CreateProduct.data_type_loc = (By.XPATH, "//tbody[%d]/tr[1]/td[5]/div/div" % (i + 1))
                CreateProduct.data_type_item_loc = (By.XPATH, "//tbody[%d]/tr[1]/td[5]/div/div/div[2]/div/div[1]/ul[2]"
                                                              "/li" % (i + 1))
                CreateProduct.min_value_loc = (By.XPATH, "//tbody[%d]/tr[1]/td[5]/div/div/div[2]/div/div/input"
                                               % (i + 1))
                CreateProduct.max_value_loc = (By.XPATH, "//tbody[%d]/tr[1]/td[5]/div/div/div[3]/div/div/input"
                                               % (i + 1))
                CreateProduct.unit_loc = (By.XPATH, "//tbody[%d]/tr[1]/td[6]/div/div/input" % (i + 1))
                CreateProduct.read_loc = (By.XPATH, "//tbody[%d]/tr[1]/td[8]/div/div" % (i + 1))
                CreateProduct.read_type_item_loc = (By.XPATH, "//tbody[%d]/tr[1]/td[8]/div/div/div[2]/div/div[1]/ul[2]"
                                                              "/li" % (i + 1))
                CreateProduct.point_save_loc = (By.XPATH, "//tbody[%d]/tr[1]/td[9]/div/a[1]" % (i + 1))
                break
        self.point_type_select(u'端点类型', value_list[1], 'devplatform/' + case_name)
        if value_list[1] == u'系统':
            self.input_descript(value_list[7])
        else:
            if value_list[2] != '':
                self.clear_input_text(self.point_id_loc)
            self.edit_input_point_id(value_list[2])
            if value_list[3] != '':
                self.clear_input_text(self.point_name_loc)
            self.edit_input_point_name(value_list[3])
            self.data_type_select(u'数据类型', value_list[4], 'devplatform/' + case_name)
            self.input_min_value(value_list[5])
            self.input_max_value(value_list[6])
            if value_list[4] != u'布尔类型':
                if value_list[7] != '':
                    self.clear_input_text(self.unit_loc)
                self.input_unit(value_list[7])
            self.input_descript(value_list[8])
            self.read_select(u'读写', value_list[9], 'devplatform/' + case_name)
        if value_list[11] != u'是':
            self.click_save(u'保存')
        else:
            self.click_cancel(u'取消')

    def get_point_id_value(self, index):
        row = self.find_elements((By.XPATH, "//tbody"))
        for i in range(len(row)):
            text = self.find_element((By.XPATH, "//tbody[%d]/tr[2]/td[1]" % (i + 1))).text
            if text == index:
                value = self.find_element((By.XPATH, "//tbody[%d]/tr[2]/td[3]" % (i + 1))).text
                func.log(u'数据端点ID为：'+value)
                return value

    def delete_data_point(self, value_list):
        row = self.find_elements((By.XPATH, "//tbody"))
        for i in range(len(row)):
            text = self.find_element((By.XPATH, "//tbody[%d]/tr[2]/td[1]" % (i + 1))).text
            if text == value_list[0]:
                self.find_element((By.XPATH, "//tbody[%d]/tr[2]/td[9]/a[2]" % (i + 1))).click()
                func.log(u'点击删除数据端点')
                self.wait_dialog_visible()
                sleep(1)
                if value_list[12] == u'是':
                    self.find_element((By.XPATH, "html/body/div[3]/div/div/div/div[3]/div/button[1]")).click()
                    func.log(u'点击确定')
                elif value_list[12] == u'否':
                    self.find_element((By.XPATH, "html/body/div[3]/div/div/div/div[3]/div/button[2]")).click()
                    func.log(u'点击取消')
                break

    def get_unit_value(self):
        value = self.find_element(self.data_unit_value).text
        func.log(u'数据端点单位为：' + value)
        return value

    def wait_mod_page_displayed(self):
        func.log(u'等待' + CreateProduct.mod_page_title + u'元素可见')
        msg = self.wait_class_visible(self.mod_page_title)
        if msg == 'Y':
            func.log(u'元素已可见')
            return True
        else:
            func.log(u'【异常】60秒后元素仍不可见')
            return False

    def save_as_custom_mod(self, value_list):
        global mod_data_point_count
        row = self.find_elements((By.CLASS_NAME,"category-menu-item__title"))
        for i in row:
            if i.text == value_list[0]:
                i.click()
                func.log(u'点击 '+value_list[0])
                sleep(1)
                break
        row1 = self.find_elements((By.CLASS_NAME, "category-menu-item__title"))
        for i in row1:
            if i.text == value_list[1]:
                i.click()
                func.log(u'点击 '+value_list[1])
                sleep(2)
                row2 = self.find_elements((By.XPATH, "//table/tr"))
                CreateProduct.mod_data_point_count = len(row2) - 1
                func.log(value_list[1] + u'的模板数据端点个数为：' + str(CreateProduct.mod_data_point_count))
                break
        if value_list[3] != '':
            self.click_button(u'存为自定义模板')
            self.wait_dialog_visible()
            sleep(1)
            self.find_element((By.XPATH, "//form/div/div/div[1]/input")).send_keys(value_list[2])
            func.log(u'模板名称输入：' + value_list[2])
            if value_list[3] == u'是':
                self.find_element((By.XPATH, "//form/button[1]")).click()
                func.log(u'点击确定')
            elif value_list[3] == u'否':
                self.find_element((By.XPATH, "//form/button[2]")).click()
                func.log(u'点击取消')
        if value_list[4] != '' and value_list[4] == u'是':
            self.click_button(u'应用模板')
            sleep(3)

    def accept_mod(self, value_list):
        global mod_data_point_count
        row = self.find_elements((By.CLASS_NAME, "category-menu-item__title"))
        for i in row:
            if i.text == value_list[0]:
                i.click()
                func.log(u'点击 ' + value_list[0])
                sleep(1)
                break
        row1 = self.find_elements((By.CLASS_NAME, "category-menu-item__title"))
        for i in row1:
            if i.text == value_list[1]:
                i.click()
                func.log(u'点击 ' + value_list[1])
                sleep(1)
                row2 = self.find_elements((By.XPATH, "//table/tr"))
                CreateProduct.mod_data_point_count = len(row2) - 1
                func.log(value_list[1] + u'的模板数据端点个数为：' + str(CreateProduct.mod_data_point_count))
                break
        if value_list[4] != '' and value_list[4] != u'不可用':
            self.click_button(u'应用')
            self.wait_dialog_visible()
            sleep(1)
            if value_list[4] == u'是':
                self.find_element((By.XPATH, "html/body/div[3]/div/div/div/div[3]/div/button[1]")).click()
                func.log(u'点击确定')
            elif value_list[4] == u'否':
                self.find_element((By.XPATH, "html/body/div[3]/div/div/div/div[3]/div/button[2]")).click()
                func.log(u'点击取消')

    def check_new_custom_mod_point_num(self, value_list):
        row3 = self.find_elements((By.XPATH, "//table/tr"))
        func.log(u'数据端点个数为 ' + str(len(row3) - 1))
        return len(row3) - 1


    def get_mod_count(self):
        row = self.find_elements((By.CLASS_NAME, "category-menu-item__title"))
        for i in row:
            if i.text == u'自定义模板':
                i.click()
                func.log(u'点击 自定义模板')
                break
        row1 = self.find_elements((By.CLASS_NAME, "category-menu-item__title"))
        func.log(u'模板总数为：' + str(len(row1)))
        return len(row1)

    def get_button_attribute(self, text, key):
        buttons = self.find_elements((By.TAG_NAME,'button'))
        for i in range(len(buttons)):
            if buttons[i].text == text:
                return buttons[i].get_attribute(key)

    def add_custom_mod(self, value_list):
        row = self.find_elements((By.CLASS_NAME, "category-menu-item__title"))
        for i in row:
            if i.text == u'创建模板':
                i.click()
                func.log(u'点击 创建模板')
                sleep(1)
                break
        self.wait_dialog_visible()
        sleep(1)
        self.find_element((By.XPATH, "//form/div/div/div[1]/input")).send_keys(value_list[2])
        func.log(u'模板名称输入：' + value_list[2])
        if value_list[3] == u'是':
            self.find_element((By.XPATH, "//form/button[1]")).click()
            func.log(u'点击确定')
        elif value_list[3] == u'否':
            self.find_element((By.XPATH, "//form/button[2]")).click()
            func.log(u'点击取消')

    def delete_custom_mod(self, value_list):
        row = self.find_elements((By.CLASS_NAME, "category-menu-item__title"))
        for i in row:
            if i.text.find(value_list[2]) >= 0:
                self.mouse_move_to(i)
                func.log(u'鼠标悬停至 '+value_list[2])
                sleep(1)
                i.find_element_by_css_selector(".del-icon.iconfont.icon-trash").click()
                func.log(u'点击删除模板按钮')
                break
        self.wait_dialog_visible()
        sleep(1)
        if value_list[5] == u'是':
            self.find_element((By.XPATH, "html/body/div[3]/div/div/div/div[3]/div/button[1]")).click()
            func.log(u'点击确定')
        elif value_list[5] == u'否':
            self.find_element((By.XPATH, "html/body/div[3]/div/div/div/div[3]/div/button[2]")).click()
            func.log(u'点击取消')

    def edit_custom_mod_name(self, value_list):
        row = self.find_elements((By.CLASS_NAME, "category-menu-item__title"))
        for i in row:
            if i.text == value_list[2]:
                i.click()
                func.log(u'点击 '+value_list[2])
                self.find_element((By.CSS_SELECTOR, ".iconfont.icon-edit")).click()
                break
        self.wait_dialog_visible()
        sleep(1)
        self.find_element((By.XPATH, "//form/div/div/div/input")).send_keys("edited")
        func.log(u'输入edited')
        if value_list[6] == u'是':
            self.find_element((By.XPATH, "//form/button[1]")).click()
            func.log(u'点击确定')
        elif value_list[6] == u'否':
            self.find_element((By.XPATH, "//form/button[2]")).click()
            func.log(u'点击取消')

    def check_mod_name_edit(self, value_list):
        row = self.find_elements((By.CLASS_NAME, "category-menu-item__title"))
        for i in row:
            if i.text == value_list[2] + "edited":
                return True
        else:
            return False

    def mod_library_add_data_point(self, value_list, case_name):
        global mod_data_point_count
        radio_loc = (By.CSS_SELECTOR, '.x-radio-wrapper.x-radio-group-item')
        row = self.find_elements((By.CLASS_NAME, "category-menu-item__title"))
        for i in row:
            if i.text == value_list[0]:
                i.click()
                sleep(1)
                func.log(u'点击 ' + value_list[0])
                row2 = self.find_elements((By.XPATH, "//table/tr"))
                CreateProduct.mod_data_point_count = len(row2) - 1
                func.log(u'模板原始数据端点数量为： ' + str(len(row2) - 1))
                break
        if value_list[14] != u'是':
            self.find_element((By.XPATH, '//header/div[1]/div/button')).click()
            sleep(2)
        else:
            self.mod_library_edit_data_point(value_list)
            sleep(2)
        self.input_text(u'索引', value_list[1])
        self.click_obj(radio_loc, value_list[2])
        if value_list[2] == u'系统':
            CreateProduct.sys_point_id_loc = (By.XPATH, "//form/div[3]/div/div/div[1]")
            CreateProduct.sys_point_id_item_loc = (By.XPATH, "//form/div[3]/div/div/div[2]/div/div[1]/ul[2]/li")
            self.sys_point_id_select(u'系统端点ID', value_list[3], case_name)
            sleep(1)
        if value_list[2] != u'系统':
            self.input_text(u'字段名称', value_list[3])
        self.click_obj(radio_loc, value_list[5])
        self.input_text(u'端点名称', value_list[4])
        sleep(1)
        if value_list[5] == u'公式计算':
            self.input_text(u'计算公式', value_list[6])
            CreateProduct.data_type_loc = (By.XPATH, "//form/div[7]/div/div/div[1]")
            CreateProduct.data_type_item_loc = (By.XPATH, "//form/div[7]/div/div/div[2]/div/div[1]/ul[2]/li")
            min_loc = (By.XPATH, "//form/div[8]/div/div/div[1]/div/div/div/div[1]/input")
            max_loc = (By.XPATH, "//form/div[8]/div/div/div[3]/div/div/div/div[1]/input")
        else:
            CreateProduct.data_type_loc = (By.XPATH, "//form/div[6]/div/div/div[1]")
            CreateProduct.data_type_item_loc = (By.XPATH, "//form/div[6]/div/div/div[2]/div/div[1]/ul[2]/li")
            min_loc = (By.XPATH, "//form/div[7]/div/div/div[1]/div/div/div/div[1]/input")
            max_loc = (By.XPATH, "//form/div[7]/div/div/div[3]/div/div/div/div[1]/input")
        self.data_type_select(u'数据类型', value_list[7], case_name)
        sleep(1)
        if value_list[8] != '':
            min_input = self.find_element(min_loc)
            min_input.clear()
            min_input.send_keys(value_list[8])
            func.log(u'输入最小值：' + value_list[8])
        if value_list[9] != '':
            max_input = self.find_element(max_loc)
            max_input.clear()
            max_input.send_keys(value_list[9])
            func.log(u'输入最大值：' + value_list[9])
        self.input_text(u'单位符号', value_list[10])
        self.click_obj(radio_loc, value_list[11])
        if value_list[12] != '':
            self.input_textarea(u'描述', value_list[12])
            func.log(u'输入描述：' + value_list[12])
        if value_list[15] != '':
            self.find_element((By.CLASS_NAME, "x-checkbox-input")).click()
            func.log(u'勾选删除数据端点')
            self.click_button(u'提交')
            self.wait_dialog_visible()
            sleep(1)
            if value_list[15] == u'是':
                self.find_element((By.XPATH, "html/body/div[3]/div/div/div/div[3]/div/button[1]")).click()
                func.log(u'点击确定')
            elif value_list[15] == u'否':
                self.find_element((By.XPATH, "html/body/div[3]/div/div/div/div[3]/div/button[2]")).click()
                func.log(u'点击取消')
        else:
            self.click_button(u'提交')

    def mod_library_edit_data_point(self, value_list):
        row = self.find_elements((By.XPATH, "//table/tr"))
        CreateProduct.mod_data_point_count = len(row) - 1
        for i in range(len(row)):
            text = self.find_element((By.XPATH, "//table/tr[%d]/td[1]" % (i + 1))).text
            if text == value_list[1]:
                CreateProduct.data_point_id_value = (By.XPATH, "//table/tr[%d]/td[2]" % (i + 1))
                CreateProduct.data_point_name_value = (By.XPATH, "//table/tr[%d]/td[3]" % (i + 1))
                CreateProduct.data_type_value = (By.XPATH, "//table/tr[%d]/td[4]" % (i + 1))
                CreateProduct.data_unit_value = (By.XPATH, "//table/tr[%d]/td[5]" % (i + 1))
                CreateProduct.data_discript_value = (By.XPATH, "//table/tr[%d]/td[6]" % (i + 1))
                CreateProduct.data_read_value = (By.XPATH, "//table/tr[%d]/td[7]" % (i + 1))
                self.find_element((By.XPATH, "//table/tr[%d]/td[8]/div/span" % (i + 1))).click()
                func.log(u'点击编辑按钮')
                break

    def get_mod_library_point_id_value(self):
        value = self.find_element(self.data_point_id_value).text
        func.log(u'字段名称为：' + value)
        return value













