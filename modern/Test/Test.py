#coding=utf-8

import os, sys
import ddt
sys.path.append(os.getcwd())

import unittest
from Page.Page import CalcPage
from selenium import webdriver
from util.Handle_log import log_handler
import HTMLTestRunner_cn
import time

@ddt.ddt
class test_calc(unittest.TestCase):
    
    def setUp(self):
        self.cp.bp.click_clear()
        time.sleep(1)
    
    def tearDown(self):
        time.sleep(1)
    
    @classmethod
    def setUpClass(cls):
        #op = webdriver.ChromeOptions()
        #op.headless = True
        #cls.driver = webdriver.Chrome(options=op)
        cls.driver = webdriver.Chrome()
        cls.log = log_handler()
        cls.logger = cls.log.get_logger()
        cls.cp = CalcPage(cls.driver)
    
    @classmethod
    def tearDownClass(cls):
        cls.log.close_log()
        cls.driver.close()
        cls.driver.quit()
    

    @ddt.data([3, 5, 0.6], [11, 22, 0.5])
    @ddt.unpack
    def test_div_common(self, a, b, c):
        ret = self.cp.run_div(a, b)
        self.assertEqual(ret, c)
    
    @ddt.data([3, 0])
    @ddt.unpack
    def test_div_ZeroDiv(self, a, b):
        self.assertEqual(self.cp.run_div(a, b), "Infinity")
        
    
if __name__ == '__main__':
    top_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    file_path = os.path.join(top_dir, "report", "basic_calc.html")

    suite = unittest.TestLoader().loadTestsFromTestCase(test_calc)
    with open(file_path, 'wb') as f:
        runner = HTMLTestRunner_cn.HTMLTestRunner(stream=f,title="This is first report",description=u"测试报告",verbosity=2)
        runner.run(suite)
    
    
    
    