#coding=utf-8

import os, sys
sys.path.append(os.getcwd())

import requests
import json

class BaseRequest:
    def run_main(self, method, url, data=None, write_cookie=None, **kwargs):
        '''
        method is (get post)
        url
        data get:params post:data
        kwargs should be cookies or headers and so on
        '''
        if method == 'GET':
            resp = requests.get(url, params=data)
            res = resp.text
        elif method == 'POST':
            resp = requests.post(url, data=data)
            res = resp.text
        else:
            print('Error: method {} not allowed'.method())
            return None
        
        try:
            res = json.loads(res)
        except:
            print("Response is a text")
        else:
            print("Response is a json")
        finally:
            return res
        
        
if __name__ == '__main__':
    
    #cd C:\Users\ylliu\Desktop\all\imooc_AutoTest\Chapter7
    #java -jar ./moco-runner-0.11.0-standalone.jar http -p 8705 -c 20200611.json
    
    sc = BaseRequest()
    sg = sc.run_main("GET", "http://127.0.0.1:8705/gettext")
    print(sg)
    sp = sc.run_main("POST", "http://127.0.0.1:8705/post_json")
    print(sp)