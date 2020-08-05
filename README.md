## [测试工程师参考手册](https://github.com/ZhuangZhu-74/QA_references)

## 自动化脚本

- [configparser（封装对ini文件的方法）](configparser)
- [mitmproxy（常规使用、HTTP录制）](mitm)
- [openpyxl（检查excel文件所有sheet的空行及空列；封装对xlsx文件的方法）](openpyxl)
- [微云文件上传的API测试](weiyun_upload)
- [关于 Selenium 的 Python 绑定的元素截取图片实现](Selenium_python_elem_shot)
- [解析并转换 har 文件](handle_har)
  - 将 `har` 文件的全部请求和响应导出到 excel 文件，可用于接口测试。
  - 在指定目录下，将全部请求的 `cookies`、 `headers` 的共有信息保存为公共文件，私有信息保存到私有文件；它们可以导入到 `JMeter` 的 `HTTP Cookie Manager`、`HTTP Header Manager` 。

## 项目

- [基于 PageObject 模型与 ddt 对在线计算器执行 UI 测试](modern)
- [基于 requests 和 ddt 的接口测试(API testing)](ApiPractice)

### 计划中的技术升级
- 日志： `logging（内建）` -> `loguru`

- 测试框架： `unittest（内建）` -> `pytest`
  - [从 unittest 迁移到 pytest](pytest)

- 测试用例参数化：`ddt（用于unittest）` -> `@pytest.mark.parametrize()`

- 测试报告： `HTMLTestRunner（第三方）` -> `pytest-html`（静态单一html）、`pytest-allure`（动态页面）

- Debug： `print() 函数` -> `PySnooper`

- `JSON` 信息处理： 内建 `json` 库 -> 增加 `JMESPath` 库
  - [选择处理 JSON 信息的库](JMESPath)

## 探索

- [chrome://  file:/// 究竟是什么？](URI)

