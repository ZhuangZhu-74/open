#coding=utf-8

import os, sys
import json
from util.handle_json import handle_json
base_path = os.getcwd()
prj_path = os.path.dirname(base_path)
sys.path.append(base_path)

from deepdiff import DeepDiff


class handle_result:
    def __init__(self):
        pass
    
    def get_msg(self, uri, code):
        # 获取模拟的msg
        mock_msg = handle_json(prj_path + "/Config/mock_msg.json")
        data = mock_msg.get_value(uri)
        if data != None:
            for i in data:
                msg = i.get(str(code))
                if msg:
                    return msg
        return None
    
    def get_json(self, uri, status):
        # 获取模拟的json
        mock_json = handle_json(prj_path + "/Config/mock_json.json")
        data = mock_json.get_value(uri)
        if data != None:
            for i in data:
                msg = i.get(status)
                if msg:
                    return msg
        return None
        
    
    def compare_json(self, dict1, dict2):
        if isinstance(dict1, dict) and isinstance(dict2, dict):
            cmp_result = DeepDiff(dict1, dict2, ignore_order=True).to_dict()
            if cmp_result.get('dictionary_item_added'):
                return False
                #return cmp_result
            else:
                return True
        return False
        
        
    
if __name__ == '__main__':
    hr = handle_result()
   # print(hr.get_msg("/get_json", "10002"))
   # print(hr.get_msg("/post_json", "10011"))
    print(hr.get_json("/get_json", "Success"))
    