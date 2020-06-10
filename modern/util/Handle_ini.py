#coding=utf-8

import os, sys
sys.path.append(os.getcwd())

from configparser import ConfigParser, ExtendedInterpolation
import chardet

class Handle_ini:
    """
    Used for ini file
    """
    def __init__(self, ini_file=None, var_sub=False):
        '''
        var_sub allow you use reference variable.
        
        https://docs.python.org/3.7/library/configparser.html#configparser.ExtendedInterpolation
        '''
        if ini_file == None:
            self.ini_file = r"C:\Users\ylliu\Desktop\poproject\lesson\config\element.ini"
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
        

    def get_value(self, option, section=None):
        '''
        如果 ini 只有一个section， 那么可以不传。
        '''
        if section == None:
            if len(self.cc.sections()) == 1:
                section = self.cc.sections()[0]
            else:
                print("Can't find section {}".format(section))
                return None
        else:
            if not self.cc.has_section(section):
                print("Can't find section {}".format(section))
                return None
            else:
                if not self.cc.has_option(section, option):
                    print("Can't find option: {} from section:{}".format(option, section))
                    return None
        
        
        return self.cc.get(section, option)
        
    @staticmethod
    def get_encoding(target_file, length=10):
        '''
        length: file first length char
        return file encoding
        '''
        with open(target_file, mode='rb') as f:
            return chardet.detect(f.read())['encoding']
        
if __name__ == '__main__':
    hd = Handle_ini(ini_file=r'../config/element.ini')
    print(hd.get_value('num_2'))
        
