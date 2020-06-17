#coding=utf-8

import os, sys
base_path = os.getcwd()
prj_path = os.path.dirname(base_path)
sys.path.append(base_path)

import json

'''
cookie.json
'''
class handle_cookie:
    
    def __init__(self, json_file=None):
        
        if json_file == None:
            json_file = prj_path + "/Config/cookie.json"
        self.json_file = json_file
        
        with open(self.json_file) as f:
            self.jc = json.load(f)
        
     
    def get_value(self, key):
        
        try:
            data =  self.jc[key]
        except:
            print("{} has not such key -> {}".format(self.json_file, key))
            return None
        else: 
            return data
    
    def update(self, cookie_key, data):
        cookie_data = self.jc
        if cookie_key in cookie_data.keys():
            cookie_data[cookie_key] = data
            with open(self.json_file, 'w') as f:
                f.write(json.dumps(cookie_data))
        else:
            return None
        

if __name__ == '__main__':
    hc = handle_cookie()
    hc.update("server", {"sda":1111})
