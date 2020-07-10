## har 文件的解析与转换

处理并转换har文件。

### 已实现功能

1 将 `har` 文件的全部请求和响应导出到 excel 文件。

```python3
# 使用方法
from handle_har import handle_har

hh = handle_har(r"www.soso.com.har")
hh.export_to_xls(r'testcase.xlsx')
```

2 在指定目录下，将全部请求的 `cookies`、 `headers` 的共有信息保存为公共文件，私有信息保存到私有文件；它们可以导入到 `JMeter` 的 `HTTP Cookie Manager`、`HTTP Header Manager` 。

```python3
# 使用方法
from handle_har import handle_har

hh = handle_har(r"www.soso.com.har")
hh.export_req_headers_to_JMeter("./output/headers_mgr")
hh.export_req_cookies_to_JMeter("./output/cookies_mgr")
```


### 获取 har 文件

- 浏览器开发者工具
- Fiddler 等

我在附件中提供的 `www.soso.com.har` 是通过以下步骤获取的：

1 打开浏览器，打开开发者工具。

2 访问 `www.soso.com`。

3 从开发者工具中右键菜单保存为 `har`。

### 参考信息
[我之前提到 har 的文章](https://github.com/ZhuangZhu-74/open/tree/master/mitm#%E5%8F%A6%E4%B8%80%E7%A7%8D%E6%80%9D%E8%B7%AF20200416)

