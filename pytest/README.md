## 从 unittest 迁移到 pytest

### 为什么我要迁移？

- 可以在命令行运行单条用例，不用打开文件再去改。
- 通过用例名或标记的方式对测试用例分组、执行。
- `HTMLTestRunner` 的报告不够酷。
- `pytest` 插件丰富，更新频繁。
- `@pytest.fixture()` 相比与 `setUp*` 和 `tearDown*` 更灵活。
- `pytest` 可以正常运行 `unittest` 用例。

### 生成测试报告

#### 使用 `pytest-html` 生成单一的 html 报告：

1. `pip install pytest-html`
2. 在命令行终端执行 pytest 命令时增加 `--html=输出路径/报告文件.html`。

#### 使用 `pytest-allure` 和 `allure2` 的命令行工具生成更漂亮的动态网页：

1 `pip install allure-pytest`

2 进入 `GitHub allure2` [版本发布页面](https://github.com/allure-framework/allure2/releases)，
在最新版本处点击 download 链接下载命令行工具压缩包。

3 解压命令行工具压缩包，记住 allure.bat 的路径。

4 在命令行终端执行 pytest 命令时增加 `--alluredir=测试结果信息文件夹`

5 在命令行终端执行 `allure.bat完整路径 generate -o 测试报告文件夹 测试结果信息文件夹`

6 由于浏览器（webkit内核）默认不支持ajax，所以你不能直接打开`index.html`，可以考虑以下方法：
  - 命令行终端执行 `python -m http.server 端口号 -d 测试报告文件夹`，使用浏览器访问
  - 编辑 `nginx` 的配置文件并启动 `nginx`，使用浏览器访问。

