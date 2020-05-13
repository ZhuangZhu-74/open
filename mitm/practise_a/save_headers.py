#coding=utf-8

'''
1 pip安装mitmproxy。
2 浏览器打开mitm.it，安装证书（这里我用的是PC端的windows，当然也适用于linux）。
3 打开ie浏览器的代理；清空历史记录和cookies。
4 打开cmd/powershell，执行mitmdump -s path/to/thisscript.py
5 访问搜狗以及百度主页。
'''

import json
from datetime import datetime
import mitmproxy.http
from mitmproxy import flow

# 检测请求头HOST字段
host_urls = ['www.sogou.com', 'www.baidu.com']
# 记录Headers的文件位置
log_file = r'C:\test.log'

class autosave:
    def request(self, flow):
        pass
    
    def response(self, flow):
        """
        Request headers
        """
        req_data = flow.request
        req_hd = req_data.headers
        """
        Response headers
        """
        resp_data = flow.response
        resp_hd = resp_data.headers
        
        with open(log_file, mode='a+', encoding='utf-8') as f:
            if req_hd.get('HOST') in host_urls and resp_hd.get('Content-Type') == 'text/html':
                # 时间戳
                current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
                f.write(current_time)
                f.write(' >>>\n')
                f.write('Request_header:\n')
                json.dump(dict(req_hd), f)
                f.write('\n')
                f.write('Response_header:\n')
                json.dump(dict(resp_hd), f)
                f.write('\n\n')

addons = [
    autosave() 
]
