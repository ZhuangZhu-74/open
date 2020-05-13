#coding=utf-8

'''
使用方法：
url、请求方法可通过 Fiddler、 浏览器开发者工具获取，然后按相应格式填入config.ini，并且
在当前脚本修改keyword。

Microsoft Windows 7：

1. 打开IE代理。
2. 启动 cmd/ powershell/ cmder（推荐）
3. 执行mitmdump -s path/to/thisscript.py
4. 打开浏览器执行操作（执行Selenium webdriver脚本也行），观察输出，
'''

import os
import json
import configparser
from datetime import datetime
from mitmproxy.http import HTTPFlow


'''
目录结构：

httpdata/${keyword}/req_${datetime}.json

获取项目根目录与记录json信息的目录，建议换成适合你实际情况的代码。
keyword对应为ini文件的section。
'''

keyword = 'upload'
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

'''
读取ini
官方参考：https://docs.python.org/3.7/library/configparser.html
*注意，编写ini文件时没必要在声明字符串时环绕单（双）引号，否则要切片。
'''
cc = configparser.ConfigParser()
ini_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')

if not os.path.exists(ini_file):
    print("No such file {}".format(ini_file))
    exit()
    
cc.read(ini_file)

if keyword in cc.sections():
    log_dir = os.path.join(project_dir, 'httpdata', keyword)
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    match_url = cc.get(keyword, 'url')
    match_method = cc.get(keyword, 'method')
else:
    print("No such section {} in {}".format(keyword, ini_file))
    exit()

'''
避免覆盖文件
注意ctrl-c暂停mitmdump后重启才会生成新文件，否则覆盖当前的文件。
'''
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
req_json = os.path.join(log_dir, 'req_{}.json'.format(current_time))
resp_json = os.path.join(log_dir, 'resp_{}.json'.format(current_time))

JMeter_req = os.path.join(log_dir, 'JMeter_req_{}.txt'.format(current_time))

# 转换为moco-runner-<ver>-standalone.jar 支持的json格式
#moco_runner_json = os.path.join(log_dir, 'mcrunner_req_{}.json'.format(current_time))

'''
创建字典收集数据
'''
req_all = dict()
resp_all = dict()

print(req_json)
print(resp_json)

class autosave:
    def request(self, flow: HTTPFlow):
        pass
    
    def response(self, flow: HTTPFlow):

        req = flow.request
        resp = flow.response
        
        if req.method == match_method and req.url == match_url:
            print("Start process...")
            """
            switch for different 'content-type' with 'body'
            for different case like 'Content-Type', 'content-type'
            """
            ct_value = ''
            for i in ('Content-Type', 'content-type'):
                tmp = dict(req.headers).get(i)
                if tmp != None:
                    ct_value = tmp
                    break
            
            # print(ct_value)
            '''
            0327：名称更改
            b_json -> body_json
            b_urlencoded_form  -> body_urlencoded_form
            b_multipart_form -> header_multipart_form
            body -> body_multipart_form
            '''
            if 'json' in ct_value:
                req_all['body_json'] = json.loads(req.get_text())
            elif 'x-www-form-urlencoded' in ct_value:
                req_all['body_urlencoded_form'] = dict(req.urlencoded_form)
            elif 'multipart/form-data' in ct_value:
                tmp = dict(req.multipart_form)

                req_all['header_multipart_form'] = dict()
                '''
                because of both key and value are bytearray, so need decode.
                Windows file encoding: utf-8, gbk
                '''
                for x,y in tmp.items():
                    try:
                        req_all['header_multipart_form'][x.decode()] = y.decode()
                    except UnicodeDecodeError:
                        req_all['header_multipart_form'][x.decode(encoding='gbk')] = y.decode(encoding='gbk')
                del tmp
                
                req_all['body_multipart_form'] = req.get_text()
            #else:
            #    req_all['body'] = req.get_text()
                
            # dict-like
            for x in ['headers', 'cookies']:
                req_all[x] = dict(getattr(req, x))
                
            """
            生成用于JMeter配置元件 ‘HTTP Header Manager’的导入文件。
            """
            with open(JMeter_req, 'w') as f:
                f.write("# Generate by mitmproxy addons\n")
                for i,j in req_all['headers'].items():
                    f.write("{}\t{}\n".format(i, j))
            
            
            # if '?' in req.url
            if '?' in match_url:
                req_all['query'] = dict(req.query)
            # property
            for y in ['host', 'path', 'url','path_components']:
                req_all[y] = getattr(req, y)
            
            # print(req_all)
                    
            with open(req_json, 'w', encoding='utf-8') as f:
                json.dump(req_all, f)
            
            '''
            Response data
            '''
            # dict-like
            '''
            Because sometime like github logout response, mitm not parse
            Cookies in currect format, so use 'Headers -> Set-Cookies' instead
            '''
            resp_all['headers'] = dict(resp.headers)
            
            try:
                tmp = json.dumps(dict(resp.cookies))
            except TypeError:
                for k in ('Set-Cookie', 'set-cookie'):
                    tmp = dict(resp.headers).get(k)
                    if tmp != None:
                        resp_all['cookies'] = tmp
                        break
            else:
                resp_all['cookies'] = dict(resp.cookies)
            finally:
                print(resp_all['cookies'])
                
            # property
            for y in ['status_code', 'reason']:
                resp_all[y] = getattr(resp, y)
            
            '''
           和上面的set-cookie一样，需要判断大小写。
            '''
            ct_value = ''
            for i in ('Content-Type', 'content-type'):
                tmp = dict(resp.headers).get(i)
                if tmp != None:
                    ct_value = tmp
                    break
                    
            if 'json' in ct_value:
                resp_all['b_json'] = json.loads(resp.get_text())
            elif 'x-www-form-urlencoded' in ct_value:
                resp_all['b_urlencoded_form'] = dict(resp.urlencoded_form)
            elif 'multipart/form-data' in ct_value:
                tmp = dict(resp.multipart_form)

                resp_all['b_multipart_form'] = dict()
                '''
                because of both key and value are bytearray, so need decode.
                Windows file encoding: utf-8, gbk
                '''
                for x,y in tmp.items():
                    try:
                        resp_all['b_multipart_form'][x.decode()] = y.decode()
                    except UnicodeDecodeError:
                        resp_all['b_multipart_form'][x.decode(encoding='gbk')] = y.decode(encoding='gbk')
                del tmp
                
                resp_all['body'] = resp.get_text()
            elif 'image' in ct_value:
                resp_image = os.path.join(log_dir, 'resp_{}'.format(req.path_components[-1]))
                with open(resp_image, 'wb') as f:
                    f.write(resp.get_content())
            #else:
            #    resp_all['body'] = resp.get_text()
            
            with open(resp_json, 'w', encoding='utf-8') as f:
                json.dump(resp_all, f)

            #print(resp.get_text())
        else:
            '''
            if req.method != match_method:
                print("ERROR: {} {} {} {} {} {}".format(
                    req.method, type(req.method),len(req.method),
                    match_method,type(match_method),len(match_method)))
            if req.url != match_url:
                print("ERROR: {} {} {} {} {} {}".format(
                    req.url, type(req.url), len(req.url),
                    match_url,type(match_url), len(match_url))
                )
            '''
        
        
addons = [
    autosave() 
]
