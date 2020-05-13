## 腾讯微云上传文件抓包及api测试

首先通过Fiddler或浏览器的开发者工具获取接口地址和请求方法。

[mitmproxy保存请求和响应信息](weiyun_upload/saveflow.py)

[抓取的请求信息](weiyun_upload/req_upload.json)

[抓取的响应信息](weiyun_upload/resp_upload.json)

当我使用这些数据编写执行接口测试时，卡在了 `content-type` 中的 `boundary` 信息与request body部分的 `boundary` 不匹配的问题上；
即使我调用了 `flow.request.set_text` 修改request body，但是Fiddler抓取到的信息仍然是未改变的。

解决方案：

1. pip 安装 requests_toolbelt。
2. `from requests_toolbelt import MultipartEncoder`。
3. 创建 `MultipartEncoder` 对象，内容是字典形式的上传内容。
4. 将 `header` 中 `content-type` 的值指向  `MultipartEncoder` 对象的 `content-type` 属性。
5. 发送POST请求。
