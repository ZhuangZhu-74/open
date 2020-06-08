#coding=utf-8
import sys, os
base_path = os.getcwd()
sys.path.append(base_path)

from configparser import ConfigParser, ExtendedInterpolation
import chardet

class Handle_ini:
    """
    Used for ini file
    """
    def __init__(self, ini_file, var_sub=False):
        '''
        var_sub allow you use reference variable.
        
        https://docs.python.org/3.7/library/configparser.html#configparser.ExtendedInterpolation
        '''
        self.ini = ini_file
        if var_sub:
            self.cc = ConfigParser(interpolation=ExtendedInterpolation())
        else:
            self.cc = ConfigParser()
        try:
            os.path.isfile(ini_file)
            with open(self.ini, encoding=self.get_encoding(self.ini)) as f:
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
    test = r'fortune.ini'
    cc = Handle_ini(test, var_sub=True)
    print(cc.get_value('s3', 'begin'))
    print(cc.get_value('s3', 'end'))
    
