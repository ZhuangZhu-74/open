#coding=utf-8

import os, sys
sys.path.append(os.getcwd())

from util.Handle_ini import Handle_ini
from util.Handle_log import log_handler

class BP:
    def __init__(self, driver):
        self.ini = Handle_ini(ini_file=r'../config/element.ini')
        self.driver = driver
        self.log = log_handler()
        self.logger = self.log.get_logger()
        
    def find_element(self, info):
        '''
        param info: ini file options
        '''
        val = self.ini.get_value(info)
        if val:
            # only split one time.
            method, name = val.split(":", 1)
            try:
                if method == 'id':
                    return self.driver.find_element_by_id(name)
                if method == 'name':
                    return self.driver.find_element_by_name(name)
                if method == 'classname':
                    return self.driver.find_element_by_class_name(name)
                if method == 'part_link':
                    return self.driver.find_element_by_partial_link_text(name)
                if method == 'xpath':
                    return self.driver.find_element_by_xpath(name)
                if method == 'link':
                    return self.driver.find_element_by_link_text(name)
                if method == 'css':
                    return self.driver.find_element_by_name(name)
                if method == 'tag':
                    return self.driver.find_element_by_tag_name(name)
            except:
                self.logger.error("No such method {}".format(method))
                return None
        else:
            self.logger.error("No such {} in {}".format(info, self.ini.ini_file))
            return None
        
    def click_nums_and_dots(self, num):
        conv_dict = {
        '0':'num_0', '1':'num_1', '2':'num_2', '3':'num_3', '4':'num_4',
        '5':'num_5', '6':'num_6', '7':'num_7', '8':'num_8', '9':'num_9',
        '.':'dot'
        }
        
        '''
        '''
        if not isinstance(num, (int, float)):
            self.logger.error("argument {} is not int or float".format(num))
            print("argument {} is not int or float".format(num))
            return "error"
        else:
            for x in list(str(num)):
                self.find_element(conv_dict[x]).click()

    
    def click_add_operator(self):
        return self.find_element('op_add').click()
        
    def click_sub_operator(self):
        return self.find_element('op_sub').click()
    
    def click_mul_operator(self):
        return self.find_element('op_mul').click()
    
    def click_div_operator(self):
        return self.find_element('op_div').click()
    
    def click_equal(self):
        return self.find_element('exec').click()
    
    def click_clear(self):
        return self.find_element('clear').click()
    
    @property
    def get_info(self):
        return self.find_element("info_tip").text
    
    @property
    def get_result(self):
        return self.find_element("result_elem").get_attribute("value")
    
    '''
    # comment because htmltestrunner_cn has same function
    
    def make_screenshot(self):
        top_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        datefmt = datetime.today().strftime("%Y%m%d_%H%M%S")
        shot_file = os.path.join(top_dir, "shot", "{}.png".format(datefmt))
        return self.driver.save_screenshot(shot_file)
    '''
        
        
    
        
        