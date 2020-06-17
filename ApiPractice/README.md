## 关于接口测试的练习（使用 mocorunner 模拟服务端）。

### 如何使用

1. 进入[该页面](https://github.com/dreamhead/moco/releases/tag/v0.12.0)下载 mocorunner， 解压出 jar 文件。
2. 下载本文件夹。
2. 打开命令提示符，执行 `java -jar moco-runner-0.12.0-standalone.jar http -p 8705 -c server.json` 。
3. 进入 `Run` 目录，执行 `ddt_run_main.py` 。

### 使用到的第三方包：

- HTMLTestRunner_cn
    （来自于 https://github.com/GoverSky/HTMLTestRunner_cn 下的 HTMLTestRunner_cn.py ，放在 PATH）
- openpyxl
- requests
- ddt


### 目录结构

- Base：封装HTTP请求。
- Case：测试用例表格文件。
- Config：用于比对的数据，服务器配置，表格与列的映射配置。
- Report：报告目录。
- Run：执行API测试的目录。
- util：封装对 `ini`、 `xlsx`、 `json`等的操作。
- server.json：用于 `mocorunner` 的配置文件。

