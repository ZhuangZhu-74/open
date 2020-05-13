#coding=utf-8

def url_extractor(url):
    """
    处理get请求的url，将它分解为可用于requests的路径和参数字典
    """
    if isinstance(url, str) and '?' in url:
        url_path, params = url.split('?')
        params_dict = dict()
        for i in params.split('&'):
            key, value = i.split('=')
            params_dict[key] = value
            return url_path, params_dict
    else:
        print("'{}' is not a 'GET request url'".format(url))
    

if __name__ == '__main__':
    sogou_query='https://www.sogou.com/web?query=sun+glasses'
    print(url_extractor(sogou_query))

