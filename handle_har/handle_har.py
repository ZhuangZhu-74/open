#coding=utf-8

import os, sys, json
from collections import Counter
from handle_excel import handle_excel

base_path = os.getcwd()
sys.path.append(base_path)


class handle_har:
    def __init__(self, har_file):
        self.har_file = har_file
        self.content = self.load_har()
        self.entries = self.content['log']['entries']
    
    def load_har(self):
        with open(self.har_file, encoding='utf-8-sig') as f:
            tmp = f.readlines()
            content = json.loads(''.join(tmp).replace('\n', ''))
        return content

    @property
    def howmany_entries(self):
        # 一共有多少组 请求/响应
        return len(self.entries)
    
    def get_all_req(self):
        return [ i['request'] for i in self.entries ]
    
    def get_all_resp(self):
        return [ i['response'] for i in self.entries ]
    
    def get_all_req_headers(self):
        return [ i['request']['headers'] for i in self.entries ]

    def get_all_req_cookies(self):
        return [ i['request']['cookies'] for i in self.entries ]
    
    def merge_to_dict(self, list_of_dicts):
        '''
        转换
        Convert list [ {"name": "Host", "value": "www.soso.com"}, 
        {"name": "Connection", "value": "keep-alive"} ]
        
        To { "Host": "www.soso.com", "Connection": "keep-alive" }
        '''
        entry_list = []
        for p in list_of_dicts:
            k, v = p['name'], p['value']
            entry_list.append((k, v))
        return dict(entry_list)

    def convertor(self, field):
        '''
        field is one of all 'req/resp -> headers/cookies' combine set:
        
        we will let a list contain all of entries by list,
        all of dict in entry will export to tuple.
        So result will perform like:
        
        list    -> list  -> tuple
        entries -> entry -> record (key, value tuple)
        '''
        if field == ('req', 'headers'):
            info = self.get_all_req_headers()
        elif field == ('req', 'cookies'):
            info = self.get_all_req_cookies()
        elif field == ('resp', 'headers'):
            info = self.get_all_resp_headers()
        elif field == ('resp', 'cookies'):
            info = self.get_all_resp_cookies()
        else:
            raise ValueError("Argument tuple is invalid")
        
        entries_list = []
        for i in info:
            entries_list.append(list(self.merge_to_dict(i).items()))
        return entries_list

    def convertor2(self, list_of_lists):
        """
        用于将 har 的请求/响应 headers/cookies 转换成JMeter 的外层和内层作用域的信息
        也就是公共和各个请求私有的信息。
        req_field: 请求字段，限定为 headers/cookies
        """
        
        '''
        展平全部tuple
        '''
        item_all = []
        for x in list_of_lists:
            for y in x:
                item_all.append(y)
        
        public_all = []
        private_all = []
        
        #pprint("counter -> {}".format(Counter(item_all).items()))
        for x, y in Counter(item_all).items():
            if y == self.howmany_entries:
                '''
                generate public
                '''
                public_all.append(x)
            else:
                '''
                if no public, it will be next
                '''
                continue
                
        for x in list_of_lists:
            private_one = x
            if public_all:
                for y in public_all:
                    private_one.remove(y)
                private_all.append(private_one)
            else:
                '''
                if no public, public return None
                '''
                public_all = None
                private_all = list_of_lists
                
        return public_all, private_all
    
    def export_to_xls(self, xlsfile):
        '''
         将全部的请求和响应保存到表格的对应列中。
        save all requests and all response to xls.
        '''
        if not (os.path.isfile(xlsfile) and xlsfile.endswith('xlsx')):
            raise ValueError("Argument error")
            
        xlsx_handle = handle_excel(xlsfile)
        xlsx_handle.sheet_by_index(0)
        
        for recordid in range(self.howmany_entries):
            entity = self.get_all_req()[recordid]
            # case_col 用于追加信息，最后按行写入
            case_col = []
            
            #print("会话编号: {}".format(recordid + 1))
            case_col.append(recordid+1)
            
            #print("请求方法: {}".format(entity["method"]))
            case_col.append(entity["method"])
            
            #print("请求地址: {}".format(entity["url"]))
            case_col.append(entity["url"])
            
            req_headers = self.merge_to_dict(entity["headers"])
            #print("请求headers: {}".format(req_headers))
            case_col.append(json.dumps(req_headers))
            
            #print("请求headers大小: {}".format(entity["headersSize"]))
            case_col.append(entity["headersSize"])
            
            req_cookies = self.merge_to_dict(entity["cookies"])
            #print("请求cookies: {}".format(req_cookies))
            if dict(req_cookies) != dict():
                case_col.append(json.dumps(dict(req_cookies)))
            else:
                case_col.append('')
            
            #print("请求字符串: {}".format(entity["queryString"]))
            if entity["queryString"] != [] :
                req_qrstr = self.merge_to_dict(entity["queryString"])
                case_col.append(json.dumps(req_qrstr))
            else:
                case_col.append('')
            
            if "postData" in entity.keys():
                pd = entity["postData"]
            else:
                pd = None
            #print("请求body: {}".format(pd))
            case_col.append(json.dumps(pd))
            
            #print("请求body大小: {}".format(entity["bodySize"]))
            case_col.append(entity["bodySize"])
            
            entity = self.get_all_resp()[recordid]
            
            #print("响应状态码: {}".format(entity["status"]))
            case_col.append(entity["status"])
            
            #print("响应描述: {}".format(entity["statusText"]))
            case_col.append(entity["statusText"])
            
            resp_headers = self.merge_to_dict(entity["headers"])
            #print("响应headers: {}".format(resp_headers))
            case_col.append(json.dumps(resp_headers))
            
            #print("响应headers大小: {}".format(entity["headersSize"]))
            case_col.append(entity["headersSize"])
            
            resp_cookies = self.merge_to_dict(entity["cookies"])
            #print("响应cookies: {}".format(resp_cookies))
            if resp_cookies != dict():
                case_col.append(json.dumps(resp_cookies))
            else:
                case_col.append('')
            
            #print("响应body: {}".format(entity["content"]))
            case_col.append(json.dumps(entity["content"]))
            
            #print("响应body大小: {}".format(entity["bodySize"]))
            case_col.append(entity["bodySize"])
            
            #print("重定向地址: {}".format(entity["redirectURL"]))
            if not entity["redirectURL"]:
                case_col.append(entity["redirectURL"])
            else:
                case_col.append('')
            
            # 用于 debug
            print("##>> {}".format(case_col))
            xlsx_handle.write_row_values(case_col, recordid+2, 1)
        
        xlsx_handle.save_wb()

    
    def export_req_headers_to_JMeter(self, logdir):
        '''
        将请求头部的共有信息保存为公共文件，私有信息保存到私有文件放到指定目录下。
        for HTTP Header Manager
        源代码文件：源代码包中的 HeaderManager.java
        '''
        
        public_all, private_all = self.convertor2(self.convertor(('req', 'headers')))
        
        if public_all:
            logfile = os.path.join(logdir, 'req_headers_pub.txt')
            req_hd = []
            req_hd.append("# Generate for JMeter by  https://github.com/ZhuangZhu-74")
            req_hd.append("# Fields: name, value")
            req_hd.append("# Separator: tab\n")
            
            for i in public_all:
                req_hd.append("{}\t{}".format(i[0], i[1]))
            with open(logfile, 'w') as f:
                f.write('\n'.join(req_hd))
        
        for index, priv in enumerate(private_all, start=1):
            logfile = os.path.join(logdir, 'req_headers_priv_{}.txt'.format(index))
            req_hd = []
            req_hd.append("# Generate for JMeter by  https://github.com/ZhuangZhu-74")
            req_hd.append("# Fields: name, value")
            req_hd.append("# Separator: tab\n")
            
            for z in priv:
                req_hd.append("{}\t{}".format(z[0], z[1]))
            with open(logfile, 'w') as f:
                f.write('\n'.join(req_hd))
    
    
    def export_req_cookies_to_JMeter(self, logdir):
        '''
        将全部请求 cookies 的共有信息保存为公共文件，私有信息保存到私有文件，放到指定目录下。
        for HTTP Cookie Manager
        源代码文件：源代码包中的 CookieManager.java
        '''
        
        public_all, private_all = self.convertor2(self.convertor(('req', 'cookies')))
        
        if public_all:
            logfile = os.path.join(logdir, 'req_cookies_pub.txt')
            req_ck = []
            req_ck.append("# Generate for JMeter by  https://github.com/ZhuangZhu-74")
            req_ck.append("# Fields: domain, [忽略位，始终为 TRUE], path, secure, [忽略位，始终为 0] , name, value")
            req_ck.append("# Separator: tab\n")
            
            for i in public_all:
                line = "{}\t{}\t{}\t{}\t{}\t{}\t{}".format('', "TRUE", '', "FALSE", 0, i[0], i[1])
                req_ck.append(line)
            with open(logfile, 'w') as f:
                f.write('\n'.join(req_ck))
        
        for index, priv in enumerate(private_all, start=1):
            logfile = os.path.join(logdir, 'req_cookies_priv_{}.txt'.format(index))
            req_ck = []
            req_ck.append("# Generate for JMeter by  https://github.com/ZhuangZhu-74")
            req_ck.append("# Fields: domain, [忽略位，始终为 TRUE], path, secure, [忽略位，始终为 0] , name, value")
            req_ck.append("# Separator: tab\n")
            
            for z in priv:
                line = "{}\t{}\t{}\t{}\t{}\t{}\t{}".format('', "TRUE", '', "FALSE", 0, z[0], z[1])
                req_ck.append(line)
            with open(logfile, 'w') as f:
                f.write('\n'.join(req_ck))

    
if __name__ == '__main__':
    hh = handle_har(r"www.soso.com.har")
    #hh.export_to_xls(r'testcase.xlsx')
    #exit(1)
    
    hh.export_req_headers_to_JMeter("./output/headers_mgr")
    hh.export_req_cookies_to_JMeter("./output/cookies_mgr")


    
