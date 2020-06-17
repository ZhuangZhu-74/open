#coding=utf-8

import os, sys
sys.path.append(os.getcwd())

from configparser import ConfigParser, ExtendedInterpolation
import chardet

class handle_ini:
    """
    Used for ini file
    """
    def __init__(self, ini_file=None, var_sub=False):
        '''
        var_sub allow you use reference variable.
        
        https://docs.python.org/3.7/library/configparser.html#configparser.ExtendedInterpolation
        '''
        if ini_file == None:
            self.ini_file = r'../Config/server.ini'
        else:
            self.ini_file = ini_file
            
        if var_sub:
            self.cc = ConfigParser(interpolation=ExtendedInterpolation())
        else:
            self.cc = ConfigParser()
        try:
            os.path.isfile(self.ini_file)
            #with open(self.ini_file, encoding='utf-8-sig') as f:
            with open(self.ini_file, encoding=self.get_encoding(self.ini_file)) as f:
                self.cc.read_file(f)
        except Exception as e:
            print(e)
            exit(2)
        

    def get_value(self, section, option):
        # print(self.ini_file)
        return self.cc.get(section, option)
    
    @property
    def caseid_col(self):
        if self.ini_file == r'../Config/excel_col.ini':
            return self.cc.getint("reflect", "caseid")
    
    @property
    def isrun_col(self):
        if self.ini_file == r'../Config/excel_col.ini':
            return self.cc.getint("reflect", "is_run")
    
    @property
    def uri_col(self):
        if self.ini_file == r'../Config/excel_col.ini':
            return self.cc.getint("reflect", "uri")
    
    @property
    def httpmethod_col(self):
        if self.ini_file == r'../Config/excel_col.ini':
            return self.cc.getint("reflect", "httpmethod")
    
    @property
    def data_col(self):
        if self.ini_file == r'../Config/excel_col.ini':
            return self.cc.getint("reflect", "data")
        
    @property
    def exp_method_col(self):
        if self.ini_file == r'../Config/excel_col.ini':
            return self.cc.getint("reflect", "expectmethod")
        
    @property
    def exp_data_col(self):
        if self.ini_file == r'../Config/excel_col.ini':
            return self.cc.getint("reflect", "expectdata")
        
    
    @property
    def run_result_col(self):
        if self.ini_file == r'../Config/excel_col.ini':
            return self.cc.getint("reflect", "runresult")
        
    @property
    def error_data_col(self):
        if self.ini_file == r'../Config/excel_col.ini':
            return self.cc.getint("reflect", "errordata")
    
    
    @staticmethod
    def get_encoding(target_file):
        '''
        length: file first length char
        return file encoding
        '''
        with open(target_file, mode='rb') as f:
            return chardet.detect(f.read())['encoding']
        
if __name__ == '__main__':
    hd = handle_ini(ini_file=r'../Config/server.ini')
    print(hd.get_value('project', 'host'))
        
