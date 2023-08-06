#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


class Settings:

    __SPECIFIED__ = False

    _root = os.path.abspath(os.path.dirname(__file__))
    _base = os.path.abspath(os.path.dirname(_root))

    # 日志文件存放的目录
    LOG_DIR = os.path.join(_base, "logs")
    # 报告文件存放的目录
    REPORT_DIR = os.path.join(_base, "reports")
    # 需要执行测试用例（python文件）的目录地址或python文件地址
    TEST_SUITE_PATH = os.path.join(_root, 'demo', 'testsuite')
    # 需要执行测试用例（excel文件）的地址
    TEST_EXCEL_PATH = os.path.join(_root, "excel_testset", "TestCases.xlsx")
    # 工程根目录路径
    PROJECT_ROOT = os.path.dirname(TEST_SUITE_PATH)

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
    LOG_REPORT_SWITCH = False

    # 测试用例执行次数（>=1 则失败后会重新执行）
    CASE_FAIL_RERUN = 1
    # 测试用例集形式，"CODE", "EXCEL", "API"
    TEST_SET_FORM = "CODE"
    # 执行包含如下Tags的测试用例，忽略大小写
    RUN_TAGS = ["ALL"]

    # 测试类和测试方法的前缀，忽略大小写
    TEST_PREFIX = 'test'
    # 需要跳过执行的目录和文件的前缀，忽略大小写
    SKIP_PREFIX = 'puskip'