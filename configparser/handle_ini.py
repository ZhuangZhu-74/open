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
        
        # alias
        self.get_value = self.cc.get
        
    @staticmethod
    def get_encoding(target_file, length=10):
        '''
        length: file first length char
        return file encoding
        '''
        with open(target_file, mode='rb') as f:
            return chardet.detect(f.read(10))['encoding']
        

if __name__ == '__main__':
    test = r'fortune.ini'
    cc = Handle_ini(test, var_sub=True)
    print(cc.get_value('s3', 'begin'))
    print(cc.get_value('s3', 'end'))
    
