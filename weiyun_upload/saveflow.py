#coding=utf-8

'''
Microsoft Windows：
0. 打开IE浏览器的代理，清空cookies等。
1. 启动 cmd/ powershell/ cmder（推荐），执行 mitmdump -s path/to/thisscript.py
'''

import os
import json
from datetime import datetime
from mitmproxy.http import HTTPFlow


'''
定义你要匹配的地址和方法，确保唯一性。
'''
#match_url = 'http://www.httpbin.org/get'
match_url = 'https://upload.weiyun.com/ftnup_v2/weiyun?cmd=247120'
match_method = "POST"

'''
设置记录json信息文件路径，这里我设置到了C盘根目录。
'''
log_dir = r'C:\'
req_json = os.path.join(log_dir, 'req_upload.json')
resp_json = os.path.join(log_dir, 'resp_upload.json')

'''
避免覆盖文件。
注意ctrl-c暂停mitmdump后重启才会生成新文件，否则覆盖当前的文件。
'''
current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
if os.path.isfile(req_json) and os.path.getsize(req_json):
    req_json = os.path.join(log_dir, 'req_upload_{}.json'.format(current_time))
    
if os.path.isfile(resp_json) and os.path.getsize(resp_json):
    resp_json = os.path.join(log_dir, 'resp_upload_{}.json'.format(current_time))

'''
新建字典分别放置数据。
'''
req_all = dict()
resp_all = dict()


class autosave:
    def request(self, flow: HTTPFlow):
        pass
    
    def response(self, flow: HTTPFlow):

        flow_req = flow.request
        flow_resp = flow.response

        if flow_req.method == match_method and flow_req.url == match_url:
            """
            根据不同的 'content-type' 进行操作
            """
            if 'content-type' in flow_req.headers.keys():
                if 'json' in flow_req.headers['content-type']:
                    req_all['b_json'] = json.loads(flow_req.get_text())
                elif 'x-www-form-urlencoded' in flow_req.headers['content-type']:
                    req_all['b_urlencoded_form'] = dict(flow_req.urlencoded_form)
                elif 'multipart/form-data' in flow_req.headers['content-type']:
                    tmp = dict(flow_req.multipart_form)
                    print(tmp)
                    req_all['b_multipart_form'] = dict()
                    
                    '''
                    因为 键和值都是 bytearray, 需要解码。
                    Windows文件编码这里列出了常见的 utf-8, gbk。
                    '''
                    for x,y in tmp.items():
                        try:
                            req_all['b_multipart_form'][x.decode()] = y.decode()
                        except UnicodeDecodeError:
                            req_all['b_multipart_form'][x.decode(encoding='gbk')] = y.decode(encoding='gbk')
                    del tmp
                    '''
                    保存 'multipart/form-data' 的 body部分。
                    '''
                    req_all['req_body'] = flow_req.get_text()
                
            # dict-like
            for x in ['headers', 'cookies']:
                req_all[x] = dict(getattr(flow_req, x))
            #if '?' in flow_req.url
            if '?' in match_url:
                req_all['query'] = dict(flow_req.query)
            # save property
            for y in ['host', 'path', 'url','path_components']:
                req_all[y] = getattr(flow_req, y)
            
           # print(req_all)
                    
            with open(req_json, 'w', encoding='utf-8') as f:
                json.dump(req_all, f)
            
            '''
            Response data
            '''
            # dict-like
            for x in ['headers', 'cookies']:
                resp_all[x] = dict(getattr(flow_resp, x))
            # save property
            for y in ['status_code', 'reason']:
                resp_all[y] = getattr(flow_resp, y)
                
            
            if 'content-type' in flow_resp.headers.keys():
                if 'json' in flow_resp.headers['content-type']:
                    resp_all['b_json'] = json.loads(flow_resp.get_text())
                else：
                    resp_all['body_text'] = flow_resp.get_text()
            
            
            with open(resp_json, 'w', encoding='utf-8') as f:
                json.dump(resp_all, f)

addons = [
    autosave() 
]
