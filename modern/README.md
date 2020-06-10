## 我选择了一个简单的在线计算器来说明 PageObject 架构。

### 页面地址：http://tools.jb51.net/tools/jisuanqi/jsq_base.htm

### 使用到的第三方包：

- HTMLTestRunner_cn
    （来自于 https://github.com/GoverSky/HTMLTestRunner_cn 下的 HTMLTestRunner_cn.py ，放在 PATH）
- selenium == 3.141.0
- ddt == 1.4.1


### 目录结构

- asePage：页面基类，基础操作元素等。
- config：ini配置文件，记录元素定位信息。
- log：日志信息。
- Page：业务页面操作。
- report：报告目录。
- Test：测试类。
- util：对于ini文件，日志的操作。