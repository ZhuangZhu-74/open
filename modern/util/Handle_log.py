#coding=utf-8

import os, sys
sys.path.append(os.getcwd())

import logging
import datetime


class log_handler:
    def __init__(self):
        
        self.logger = logging.getLogger()
        
        datefmt = datetime.datetime.now().strftime("%Y-%m-%d")
        top_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_file = os.path.join(top_dir, "log", "{}.log".format(datefmt))

        self.fh = logging.FileHandler(filename=log_file)
        
        fmt_str = '%(asctime)s %(filename)s --> %(funcName)s %(lineno)s: %(levelname)s ----->%(message)s'
        loggerfmt = logging.Formatter(fmt_str)
        
        self.logger.setLevel(logging.DEBUG)
        
        self.fh.setFormatter(loggerfmt)
        self.logger.addHandler(self.fh)
        
    def get_logger(self):
        return self.logger
        
    def close_log(self):
        self.fh.close()
        self.logger.removeHandler(self.fh)


        