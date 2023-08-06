#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .settings import Settings as SETTINGS
from .utils.logger import logger
from .testrunner import TestRunner
from .testresult import TestResult
from importlib import reload, import_module


def RELOAD_SETTINGS():
    SETTINGS.__SPECIFIED__ = True

    from . import settings
    settings.Settings = SETTINGS
    from .utils.logger import Logger
    global logger
    logger = Logger(
        logger_dir=SETTINGS.LOG_DIR,
        console_level=SETTINGS.LOG_CONSOLE_LEVEL,
        file_level=SETTINGS.LOG_FILE_LEVEL,
        report_level=SETTINGS.LOG_REPORT_LEVEL
    ).get_new_logger(
        console_switch=SETTINGS.LOG_CONSOLE_SWITCH,
        file_switch=SETTINGS.LOG_FILE_SWITCH,
        report_switch=SETTINGS.LOG_REPORT_SWITCH
    )

    from .testcase import TestCaseHandler
    TestCaseHandler.total_case_num = 0
    TestCaseHandler.actual_case_num = 0

    import punittest
    reload(punittest)
    from punittest import PUnittest

    # 通过递归的方式重载所有PUnittest的子类所在的文件（也就是测例文件），
    # 这样做的目的是可以在运行过程中想要修改测例的配置，比如tag
    def get_all_subclasses(cls):
        subclasses = cls.__subclasses__()
        for subclass in subclasses:
            module = import_module(subclass.__module__)
            reload(module)
            get_all_subclasses(subclass)

    get_all_subclasses(PUnittest)


__all__ = ['SETTINGS', 'RELOAD_SETTINGS', 'TestRunner', 'TestResult', 'logger']


if SETTINGS.__SPECIFIED__ is True:
    from .punittest import PUnittest
    __all__.append('PUnittest')
