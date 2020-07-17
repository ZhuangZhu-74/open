## 从 unittest 迁移到 pytest

### 为什么我要迁移？

- 可以在命令行运行单条用例，不用打开文件再去改。
- 通过用例名或标记的方式对测试用例分组、执行。
- `HTMLTestRunner` 的报告不够酷。
- `pytest` 插件丰富，更新频繁。
- `@pytest.fixture()` 相比与 `setUp*` 和 `tearDown*` 更灵活。
- `pytest` 可以正常运行 `unittest` 用例。
