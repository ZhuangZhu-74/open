#coding=utf-8

import os, sys
sys.path.append(os.getcwd())

from BasePage.BasePage import BP
from util.Handle_log import log_handler
import time

from selenium import webdriver

class CalcPage:
    def __init__(self, driver):
        self.driver = driver
        self.bp = BP(self.driver)
        self.log = log_handler()
        self.logger = self.log.get_logger()
        self.driver.maximize_window()
        self.driver.get("http://tools.jb51.net/tools/jisuanqi/jsq_base.htm")
        
    def run_add(self, num1, num2):
        self.bp.click_nums_and_dots(num1)
        self.bp.click_add_operator()
        self.bp.click_nums_and_dots(num2)
        self.bp.click_equal()
        #print(self.bp.get_info)
        print(type(self.bp.get_result))
        return self.bp.get_result
    
    def run_div(self, num1, num2):
        #time.sleep(5)
        if self.bp.click_nums_and_dots(num1) != "error":
            #time.sleep(5)
            self.bp.click_div_operator()
            # time.sleep(5)
            if self.bp.click_nums_and_dots(num2) != "error":
                self.bp.click_equal()
            else:
                print("see log for error 1")
                return "error"
        else:
            print("see log for error 2")
            return "error"
            
        # self.bp.get_result is str
        
        # for int
        result = self.bp.get_result
        if result.isnumeric():
            # print('1', result, type(result))
            return int(result)
        # for Infinity (3/0) dividedbyzero
        elif result == 'Infinity':
            self.logger.error(self.bp.get_info)
            self.logger.error("divided by zero")
            return result
        # for float
        elif isinstance(float(result), float):
            # print('2', result, type(result))
            return float(result)
        else:
            self.logger.error(self.bp.get_info)
            self.logger.error(result)
            return None
    
    
if __name__ == '__main__':
    op = webdriver.ChromeOptions()
    op.headless = True
    wd = webdriver.Chrome(options=op)
    
    cp = CalcPage(wd)
    try:
        a = cp.run_div(3, 0)
        print(a)
    finally:
        cp.driver.close()
        cp.driver.quit()
            
    