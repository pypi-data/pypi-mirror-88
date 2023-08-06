#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from punittest import SETTINGS, RELOAD_SETTINGS
from punittest import logger, TestRunner

demo = os.path.abspath(os.path.dirname(__file__))
root = os.path.abspath(os.path.dirname(demo))
# 先修改punittest的设置然后重载
SETTINGS.PROJECT_ROOT = os.path.abspath(os.path.dirname(root))
SETTINGS.RUN_TAGS = ["ALL"]
SETTINGS.CASE_FAIL_RERUN = 1
SETTINGS.TEST_PREFIX = 'test'
SETTINGS.SKIP_PREFIX = 'skip'

# 如果是TEST_SET_FORM是CODE则需要指定TEST_SUITE_DIR
SETTINGS.TEST_SET_FORM = "CODE"
SETTINGS.TEST_SUITE_PATH = os.path.join(demo, 'testsuite', 'login')
SETTINGS.TEST_EXCEL_PATH = os.path.join(root, 'excel_testset', 'TestCases.xlsx')

SETTINGS.LOG_CONSOLE_SWITCH = True
SETTINGS.LOG_FILE_SWITCH = False
SETTINGS.LOG_REPORT_SWITCH = False
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
