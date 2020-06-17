#coding=utf-8

import os, sys
base_path = os.getcwd()
prj_path = os.path.dirname(base_path)
sys.path.append(base_path)

import json

class handle_json:
    
    def __init__(self, json_file=None):
        
        if json_file == None:
            json_file = prj_path + "/Config/user_data.json"
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
    


if __name__ == '__main__':
    hj = handle_json()
    print(hj.get_value('/post_json'))
