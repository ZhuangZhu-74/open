## 将headers信息另存到文件

如果你在用`python`的`requests`库构建接口测试的`GET`、`POST`等请求，那么构造参数的headers和cookies的字典就要预备对应的数据文件；如果你通过`Fiddler`
去实现抓包，那么还要手动保存`Inspectors`->`Raw`中的信息，再读取它们构建字典。

这真是一个令人疲乏的操作。

使用`mitmproxy`模块编写脚本就可以使得上述流程完全自动化，节省您的宝贵时间。

[查看脚本文件](mitm/practise_a/save_headers.py) （**修改脚本不需要暂停mitmdump，程序会自动重新加载**）。

[输出结果](mitm/practise_a/saved_headers.log)

## 把GET请求的url分解为请求路径和请求参数字典

[查看脚本文件](mitm/practise_b/url_extractor.py)

当然，`mitmproxy` 的 `flow.request.query`（将url问号之后的query string整理为字典）和`flow.request.path_components`（分解url中host之后到问号之前的路径到元组）也能完成。


## HTTP录制器

- 设计目的
  - 将请求和相应数据转化为json，便于导入 `python requests`。
  - TODO：由于 `badboy` 不再更新，尝试录制并输出`jmx`。
  
- 当前实现功能
  - 从ini文件中读取要监视的url和请求方法，分别保存请求和响应到json文件之中。
  - 生成用于 `JMeter` 配置元件 `HTTP Header Manager` 的导入文件。

[源文件，请注意功能尚不完全，请谨慎使用](record/saveinfo.py)

[待补充完全的excel表格，用于说明 `flow.request` 和 `flow.response` 的方法和属性](record/mitm_flow.xlsx)

### 另一种思路（20200416）

随着我进一步的扩充知识面，`har`文件可能会更适合的拿来做数据文件，原因如下：

- [w3c标准](https://w3c.github.io/web-performance/specs/HAR/Overview.html)。
- 本质是 `json` ，易于解析。
- 包含了全部HTTP会话。
- 相当多的浏览器(`Chrome`，`Edge`等)、抓包工具（`Fiddler`，`Charles`）、也包括我关注的mitmproxy支持[导出har文件](https://github.com/mitmproxy/mitmproxy/blob/master/examples/complex/har_dump.py)。
- `har` 文件也可以通过[Blazemeter提供的在线转换器](https://converter.blazemeter.com/)转为 `JMeter` 支持的 `jmx` 格式。

**TODO** 那么我只需要封装用于解析`har`文件的脚本就可以方便的在接口自动化脚本中调用了。
