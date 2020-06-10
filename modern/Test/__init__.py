#coding=utf-8

import os, sys
sys.path.append(os.getcwd())

from selenium import webdriver
from util.Handle_ini import Handle_ini
import time

wd = webdriver.Chrome()
wd.get("http://tools.jb51.net/tools/jisuanqi/jsq_base.htm")
# 3+2
'''
hi = Handle_ini(ini_file=r'../config/element.ini')

method1, n3 = hi.get_value('simple', 'num_3').split(':')
method2, calc_add = hi.get_value('simple', 'op_add').split(':')
method3, n2 = hi.get_value('simple', 'num_2').split(':')
'''
wd.find_element_by_xpath("//tr[3]//td[3]//input[1]").click()
wd.find_element_by_xpath("//tr[4]//td[4]//input[1]").click()
wd.find_element_by_xpath("//tr[3]//td[2]//input[1]").click()
wd.find_element_by_xpath("//tr[3]//td[5]//input[1]").click()

res_elem = wd.find_element_by_id("jsqResult")
actual_res = res_elem.get_attribute("value")
print(actual_res)

time.sleep(5)
wd.close()
wd.quit()