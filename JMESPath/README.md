### 选择处理 `JSON` 信息的库

#### 常用处理 `JSON` 信息的库的介绍：

- `Python` 内建的 `json` 库适用于内容简单的情况。

- `JMESPath` 和 `jsonpath-rw` 适合于处理复杂的 JSON 格式，但是 `jsonpath-rw` 只适用于 `Python`。

- `JMESPath` 在 `JMeter` 中的应用：
  - 断言： `JSON JMESPath Assertion`
  - 后置处理器： `JSON JMESPath Extractor`

**综上所述，我选择 `JMESPath` 处理复杂情况，`Python` 内建的 `json` 库处理简单情况。**

#### `JMESPath` 的相关资料：
- 主页：
https://jmespath.org/

- github 主页：
https://github.com/jmespath

- 常见编程语言的 `JMESPath` 库：
https://jmespath.org/libraries.html

- 安装 `Python` 版本的 `JMESPath` 库：
  - `pip install jmespath`

- tutorial：
https://jmespath.org/tutorial.html

- example：
https://jmespath.org/examples.html

- 规范（语法）
https://jmespath.org/specification.html

