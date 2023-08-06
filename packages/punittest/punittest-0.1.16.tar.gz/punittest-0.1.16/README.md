---
typora-root-url: pic
---


# 简介
punittest 是基于 unittest 的第三方扩展 utx 的修改版本。使用起来非常方便，和 unittest 类似。

除了满足 unittest 的常用功能之外，还提供日志、html 报告、excel 组织用例、用例失败重新执行、利用 tag 加载用例等功能。



# 安装

**依赖库**
- openpyxl - 解析 xlsx 文件

如果是离线安装，请访问 PyPi 下载 tar.gz 压缩包后使用 pip 安装
```shell
pip install punittest-0.1.1.tar.gz
```
如果是联网环境，直接使用 pip 工具下载安装即可
```shell
pip3 install punittest
```



# 使用 Demo

demo 的测试用例都在 demo 目录的 testsuite 目录下：

运行 demo 目录下的 main.py：
```python
import os
from punittest import SETTINGS, RELOAD_SETTINGS
from punittest import logger, TestRunner

demo = os.path.abspath(os.path.dirname(__file__))
root = os.path.abspath(os.path.dirname(demo))
# 先修改punittest的设置然后重载
SETTINGS.PROJECT_ROOT = os.path.abspath(os.path.dirname(root))
SETTINGS.RUN_TAGS = ["ALL"]
SETTINGS.CASE_FAIL_RERUN = 2

# 如果是TEST_SET_FORM是CODE则需要指定TEST_SUITE_DIR
# SETTINGS.TEST_SUITE_DIR = os.path.join(demo, 'testsuite', 'chat')
SETTINGS.TEST_SET_FORM = "EXCEL"
SETTINGS.TEST_EXCEL_PATH = os.path.join(root, 'excel_testset', 'TestCases.xlsx')

SETTINGS.LOG_CONSOLE_SWITCH = True
SETTINGS.LOG_FILE_SWITCH = False
SETTINGS.LOG_REPORT_SWITCH = True
SETTINGS.LOG_CONSOLE_LEVEL = "DEBUG"
SETTINGS.LOG_FILE_LEVEL = "DEBUG"
SETTINGS.LOG_REPORT_LEVEL = "INFO"

SETTINGS.LOG_DIR = r"D:\Temp\Logs"
SETTINGS.REPORT_DIR = r"D:\Temp\Reports"

SETTINGS.CAP_FUNC = lambda _dir, name, **kwargs: logger\
    .info(r"创建截图{}\{}，参数{}".format(_dir, name, kwargs))
SETTINGS.CAP_DIR = r"D:\Temp\screenshots"
SETTINGS.CAP_KWARGS = {"arg1": "val1", "arg2": "val2"}

RELOAD_SETTINGS()

# 运行测试
logger.info("开始")
runner = TestRunner("demo接口测试用例")
results = runner.run()
logger.info("结束")
```
输出结果包含三部分：

- 控制台日志

- 日志文件

![punittest_logfile](pic/punittest_logfile.png)
    
- html 报告

![punittest_report01](pic/punittest_report01.png)

![punittest_report02](pic/punittest_report02.png)



# 使用说明

- 使用 punittest 的日志器 logger
```python
from punittest import logger

logger.debug("xxx")
logger.info("xxx")
logger.warning("xxx")
logger.error("xxx")
```
- 使用 punittest 编写测试用例
```python
from punittest import PUnittest, logger


class TestLogin(PUnittest):
    """测试登录功能"""

    @PUnittest.tag("Smoke", "Regression")
    @PUnittest.data([{'user': 'username', 'pass': 'password'}], [True])
    def test_login_successfully(self, params, asserts):
        """测试登录成功"""
        _user, _passwd = params['user'], params['pass']
        _result = asserts
        logger.info("调用登录接口，用户名/密码: {}/{}， 获取登录结果".format(_user, _passwd))
        result = True
        self.assertTrue(_result, result)

    @PUnittest.tag("Regression")
    @PUnittest.data(
        [{'user': 'username', 'pass': '123'},
         {'user': '123', 'pass': 'password'},
         {'user': '', 'pass': ''}],
        [False, False, False])
    def test_login_failed(self, params, asserts):
        """测试登录失败"""
        _user, _passwd = params['user'], params['pass']
        _result = asserts
        logger.info("调用登录接口，用户名/密码: {}/{}， 获取登录结果".format(_user, _passwd))
        result = False
        self.assertTrue(_result, result)

    @PUnittest.skip("这里跳过不测")
    @PUnittest.tag("Regression")
    @PUnittest.data([{'user': 'username', 'pass': 'password'}], [True])
    def test_relogin_successfully(self, params, asserts):
        """测试重新登录成功"""
        _user, _passwd = params['user'], params['pass']
        _result = asserts
        logger.info("调用登录接口，用户名/密码: {}/{}， 获取登录结果".format(_user, _passwd))
        result = True
        self.assertTrue(_result, result)
        logger.info("调用登录接口，用户名/密码: {}/{}， 获取登录结果".format(_user, _passwd))
        result = True
        self.assertTrue(_result, result)
       
```
- 在入口文件 main.py 中修改 punittest 的 SETTING 后重载
```python
import os
from punittest import SETTINGS, RELOAD_SETTINGS
from punittest import logger, TestRunner

demo = os.path.abspath(os.path.dirname(__file__))
root = os.path.abspath(os.path.dirname(demo))

# 先修改punittest的设置然后重载
SETTINGS.PROJECT_ROOT = os.path.abspath(os.path.dirname(root))
SETTINGS.RUN_TAGS = ["ALL"]
SETTINGS.CASE_FAIL_RERUN = 2

# 如果是TEST_SET_FORM是CODE则需要指定TEST_SUITE_DIR
SETTINGS.TEST_SUITE_DIR = os.path.join(demo, 'testsuite', 'chat')
SETTINGS.TEST_SET_FORM = "EXCEL"
SETTINGS.TEST_EXCEL_PATH = os.path.join(root, 'excel_testset', 'TestCases.xlsx')

SETTINGS.LOG_CONSOLE_SWITCH = True
SETTINGS.LOG_FILE_SWITCH = False
SETTINGS.LOG_REPORT_SWITCH = True
SETTINGS.LOG_CONSOLE_LEVEL = "DEBUG"
SETTINGS.LOG_FILE_LEVEL = "DEBUG"
SETTINGS.LOG_REPORT_LEVEL = "INFO"

SETTINGS.LOG_DIR = r"D:\Temp\Logs"
SETTINGS.REPORT_DIR = r"D:\Temp\Reports"

SETTINGS.CAP_FUNC = lambda _dir, name, **kwargs: logger\
    .info(r"创建截图{}\{}，参数{}".format(_dir, name, kwargs))
SETTINGS.CAP_DIR = r"D:\Temp\screenshots"
SETTINGS.CAP_KWARGS = {"arg1": "val1", "arg2": "val2"}

RELOAD_SETTINGS()
```
- 再在入口文件 Main.py 中导入 TestRunner 并调用其 run() 方法运行测试
```python
from punittest.testrunner import TestRunner
# 调用TestRunner的run()方法运行测试框架
runner = TestRunner("XXX接口功能测试用例")
runner.run()
```



# 功能说明

- 组织测试用例
    - 使用装饰器组织
    - 使用 excel 表格组织
-  加载测试用例
    - 使用 unittest.TestLoader() 加载
    - 使用 excel 表格加载
- 执行测试
    - 断言
    - 异常处理 
    - 失败重新执行
    - 失败自动截图
- 获取测试结果
    - 日志
    - 测试报告
    - 测试结果数据集
- 配置文件



## 使用装饰器组织测试用例

punittest 为测试类中的测试方法提供了4种装饰器：skip, skip_if, data, tag。

测试类继承了 PUnittest 类后，测试方法即可使用这4种装饰器：
- skip - 跳过某一条测试用例（和 unittest 的 skip 用法一致）
```python
@PUnittest.skip("这里书写跳过的原因")
def test_02(self):
    """测试02"""
    logger.debug("jaja")
    self.assertEqual(1, 2)
    self.assertEqual(1, 3)
```
- skip_if - 在某种情况下跳过某一条测试用例（和 unittest 的 skip 用法一致）
```python
@PUnittest.skip_if(counter<10, "这里书写跳过的原因")
def test_02(self):
    """测试02"""
    logger.debug("jaja")
    self.assertEqual(1, 2)
    self.assertEqual(1, 3)
```
- data - 为测试方法传递参数
    data 接收2个参数 params 和 asserts，类型为 list，对应测试参数和断言的参数，两个列表的元素位置需要对应。
    被 data 装饰过的测试方法会根据参数列表中的元素数目将该条测试用例拆分成数个用例，分别使用对应的参数进行测试。
```python
@PUnittest.data([[1, 2], [-1, 1]], [3, 0])
def test_04(self, params, asserts):
    """测试04"""
    logger.info("hehe")
    result = params[0] + params[1]
    self.assertEqual(result, asserts)
```
```python
@PUnittest.data([{'user': 'user1', 'pass': 1}, {'user': 'user2', 'pass': 2}], [1, 2])
def test_07(self, params, asserts):
    """测试07"""
    result = params['pass']
    self.assertEqual(result, asserts)
```
- tag - 为测试用例添加 tag，在加载用例的时候可以加载指定 tag 的用例，不填写 tag 参数的则默认 tag 为 All 
```python
@PUnittest.tag("Smoke", "Regression")
def test_02(self):
    """测试02"""
    logger.debug("jaja")
    self.assertEqual(1, 2)
    self.assertEqual(1, 3)
```


## 使用 excel 表格组织测试用例

**当指定SETTINGS中的TEST_SET_FORM为EXCEL，并指定TEST_EXCEL_PATH，就可以加载excel的测试用例并执行。**

excel_testset 目录中的 TestCases.xlsx 文件记录了需要测试的用例，格式如下：
![](pic/punittest_testcase.png)

- Priority - 测试用例优先级，和编码无关的属性，可以删除
- Tags - 测试用例标签，对应 tag 装饰器中的标签
- Skip - 是否跳过，如果需要跳过，则填写跳过内容，无内容则认为不跳过
- TestDir - 测试目录名称，测试文件所在的目录，多级菜单之间用 . 连接，如 TestSuite.TestSubSuite
- TestFile - 测试文件名称
- TestClass - 测试类名称
- TestCase - 测试用例名称
- CaseDescription - 测试用例描述
- ParamsData - 测试用例的测试参数，多个测试数据之间用换行符隔开，对应于 data 装饰器第一个参数列表中的元素
- AssertResult - 测试用例的断言参数，多个断言数据之间用换行符隔开，对应于 data 装饰器第二个参数列表中的元素

**可以对 excel 的标题进行过滤，punittest 只会运行过滤后依然显示的测试用例。**



## 使用 HttpApi 传递测试用例

也可以使用 http_api 来传递需要执行的用例，用例的格式和excel读取的保持一致。**当指定SETTINGS中的TEST_SET_FORM为API，就可以加载api传递的测试用例。**



## 使用 python 文件组织测试用例

**当指定SETTINGS中的TEST_SET_FORM为CODE，并指定TEST_SUITE_DIR，就可以指定加载该目录下的.py文件，并加载符合TEST_PREFIX的类和方法为测试用例**。



## 断言
punittest.py 中的 PUnittest 类继承了 unittest.TestCase 类，但也进行了扩展：
- 针对断言行为添加了日志
- 为断言失败添加了异常队列，在同一条用例中出现断言失败，不再会终止用例，而是继续执行，直到结束后再抛出所有的断言异常

如果需要让断言方法添加以上 2 种扩展功能，则需要在 PUnittest 类中显式地重定义一次相应的断言方法即可：
```python
class PUnittest(unittest.TestCase, metaclass=Meta):
    
    def assertEqual(self, first, second, msg=None):
        super(PUnittest, self).assertEqual(first, second, msg=msg)

    def assertAlmostEqual(self, first, second, places=None, msg=None, delta=None):
        super(PUnittest, self).assertAlmostEqual(first, second, places=places, msg=msg, delta=delta)

    def assertDictEqual(self, d1, d2, msg=None):
        super(PUnittest, self).assertDictEqual(d1=d1, d2=d2, msg=msg)
```



## 异常处理 

测试用例执行过程中一旦发现异常，则会终止该用例的测试，抛出异常，和 unittest 保持一致。不像改写过的断言过程会有异常列表。



## 失败自动截图

Settings.py 中提供了关于失败自动截图的接口：
```python
SETTINGS.CAP_FUNC = lambda _dir, name, **kwargs: logger\
    .info(r"创建截图{}\{}，参数{}".format(_dir, name, kwargs))
SETTINGS.CAP_DIR = r"D:\Temp\screenshots"
SETTINGS.CAP_KWARGS = {"arg1": "val1", "arg2": "val2"}
```
由于不同的工程可能使用完全不同的截图方式，所以 punittest 只提供了接收截图函数的接口，而没有具体实现。上例中用 lambda 表达式编写了一个打印文本的函数实例，实际运行效果如下：
```
[2019-07-29 17:19:39,174][INFO]: ********************************************** Start ***********************************************
[2019-07-29 17:19:39,175][INFO]: 登录角色
[2019-07-29 17:19:39,175][INFO]: 修改角色货币
[2019-07-29 17:19:39,175][INFO]: [TestCase]: TestLottery.test_00010_lottery_not_enough_gold 测试游戏内抽奖功能|测试抽奖货币不足
[2019-07-29 17:19:39,175][INFO]: [TestProgress]: 9/13 [RerunTime]: NO.1
[2019-07-29 17:19:39,175][INFO]: 将角色货币归0
[2019-07-29 17:19:39,175][INFO]: 调用抽奖接口，获取抽奖结果
[2019-07-29 17:19:39,175][INFO]: [Assert]: assertIn('抽奖道具列表', '货币不足')
[2019-07-29 17:19:39,175][INFO]: 创建截图D:\Temp\screenshots\2019-07-29_17-19-39_test_00010_lottery_not_enough_gold.png，参数{'arg1': 'val1', 'arg2': 'val2'}
[2019-07-29 17:19:39,175][ERROR]: [TestResult]: Fail!
[2019-07-29 17:19:39,175][INFO]: 角色登出
[2019-07-29 17:19:39,175][INFO]: *********************************************** End ************************************************
[2019-07-29 17:19:39,176][INFO]: 
[2019-07-29 17:19:39,176][ERROR]: TestCase Failed:
[2019-07-29 17:19:39,176][ERROR]: Traceback (most recent call last):
  File "E:\Workspace\Packages\punittest\punittest\testcase.py", line 110, in wrap
    raise e
  File "E:\Workspace\Packages\punittest\punittest\testcase.py", line 103, in wrap
    args[0]._raise_exc()
  File "E:\Workspace\Packages\punittest\punittest\punittest.py", line 32, in _raise_exc
    raise AssertionError(exc_text)
AssertionError: '抽奖道具列表' not found in '货币不足'
```
在实际使用中，只需要编写截图函数，并配置相应的截图选项即可。



## 失败重新执行

settings.py   进行设置，数字设置为1，则失败后不会重新执行，>1 则会重新执行。
```
CASE_FAIL_RERUN = 1
```

**请注意重新执行的用例不会再重新执行 setUp 和 tearDown 过程。**



## 日志

PUnittest 提供 3 种类型的日志，分别是控制台，日志文件和测试报告日志，都有开关控制是否开启，3 种日志能分别设置日志级别。这些可以在 settings.py 中进行设置。
```
# 日志文件存放的目录
LOG_DIR = os.path.join(_base, "logs")

# 过滤日志的级别
LOG_CONSOLE_LEVEL = "DEBUG"
LOG_FILE_LEVEL = "DEBUG"
LOG_REPORT_LEVEL = "DEBUG"

# 是否开启日志的开关
LOG_CONSOLE_SWITCH = True
LOG_FILE_SWITCH = False
LOG_REPORT_SWITCH = True
```



## 测试报告

PUnittest 会自动生成一份 html 形式的测试报告，供测试者查阅。相关设置如下：
```
# 报告文件存放的目录
REPORT_DIR = os.path.join(_base, "reports")
```



## 测试结果数据集

调用 TestRunner 类的 run() 方法后会返回测试结果数据集。
```python
# 运行测试
logger.info("开始")
runner = TestRunner("demo接口测试用例")
results = runner.run()
logger.info("结束")
```
本身是个 dict，多个字段提供了测试结果的详情，这本身也为测试报告提供了接口：
```python
{   
	'beginTime': '2019-07-29 17:08:48.660638',
    'finishTime': '2019-07-29 17:08:48.756378',
    'reportName': 'demo接口测试用例',
    'testAll': 14,
    'testError': 1,
    'testFail': 3,
    'testPass': 9,
    'testResult': [
		{ 
			'className': 'punittest.demo.testsuite.login.test_login.TestLogin',
	        'description': '测试登录功能',
	        'endTime': '2019-07-29 17:08:48.735436',
	        'log': '[2019-07-29 17:08:48,734][INFO]: [TestCase]: '
	               'TestLogin.test_00001_login_successfully_#1 '
	               '测试登录功能|测试登录功能\n'
	               '[2019-07-29 17:08:48,734][INFO]: '
	               '[TestProgress]: 1/13 [RerunTime]: NO.1\n'
	               '[2019-07-29 17:08:48,734][INFO]: '
	               '调用登录接口，用户名/密码: username/password， 获取登录结果\n'
	               '[2019-07-29 17:08:48,735][INFO]: [Assert]: '
	               'assertTrue(True, True)\n'
	               '[2019-07-29 17:08:48,735][INFO]: '
	               '[TestResult]: Pass!\n',
	        'methodName': 'test_00001_login_successfully_#1',
	        'spendTime': '0:00:00.001995',
	        'startTime': '2019-07-29 17:08:48.733441',
	        'status': '成功'
        },
        {
        	...
        },
	],
    'testSkip': 1,
    'totalTime': '0:00:00.095740'
}
```



## 配置文件

配置文件是 settings.py，可以编写 python 代码
```python
class Settings:

    _root = os.path.abspath(os.path.dirname(__file__))
    _base = os.path.abspath(os.path.dirname(_root))

    # 日志文件存放的目录
    LOG_DIR = os.path.join(_base, "logs")
    # 报告文件存放的目录
    REPORT_DIR = os.path.join(_base, "reports")
    # 需要执行测试用例（python文件）的目录地址
    TEST_SUITE_DIR = ""
    # 需要执行测试用例（excel文件）的地址
    TEST_EXCEL_PATH = os.path.join(_root, "excel_testset", "TestCases.xlsx")

	# 测试用例失败截图函数
    CAP_FUNC = None
    # 测试用例失败截图存放目录
    CAP_DIR = os.path.join(_base, "screenshots")
    # 测试用例失败截图函数参数
    CAP_KWARGS = {}
    
    # 过滤日志的级别
    LOG_CONSOLE_LEVEL = "DEBUG"
    LOG_FILE_LEVEL = "DEBUG"
    LOG_REPORT_LEVEL = "DEBUG"

    # 是否开启日志的开关
    LOG_CONSOLE_SWITCH = True
    LOG_FILE_SWITCH = False
    LOG_REPORT_SWITCH = True

    # 测试用例执行次数（>=1 则失败后会重新执行）
    CASE_FAIL_RERUN = 1
    # 是否从Excel表格中读取测试用例
    EXCEL_TEST_SET = True
    # 执行包含如下Tags的测试用例
    RUN_TAGS = "Regression, Smoke"
```
使用配置文件时不需要修改源码，而是在入口文件中先导入 punittest.SETTINGS，修改 SETTINGS 项后调用 RELOAD_SETTINGS 即可，比如：
```python
from punittest import SETTINGS, RELOAD_SETTINGS

SETTINGS.EXCEL_TEST_SET = True
SETTINGS.RUN_TAGS = ["All"]
SETTINGS.LOG_DIR = "D:\Temp\Logs"
SETTINGS.REPORT_DIR = "D:\Temp\Reports"
RELOAD_SETTINGS()


from punittest import TestRunner

runner = TestRunner("demo接口测试用例")
runner.run()
```



# 文件说明

- excel_testset - 存放 excel 用例文件的目录
- report - 存放 html 报告模板的目录
- static - 存放 html 报告模板所需 css 和 js 的目录
- utils - 工具目录，提供日志格式和 excel 解析方法
- punittest - PUnittest 供测试类继承，以便调用相应的装饰器
- testcase - 提供测试方法的装饰器，并且会在加载过程中动态修改名称和添加测试参数
- testresult - 处理测试用例的测试结果
- testrunner - 执行 run() 方法执行测试，产生 html 测试报告
- testset - make_test_suite() 方法加载测试集
- settings - 配置文件
