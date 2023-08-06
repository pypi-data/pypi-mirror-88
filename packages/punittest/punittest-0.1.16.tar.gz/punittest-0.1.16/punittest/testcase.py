#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from .testset import *
from .utils.logger import logger
from functools import wraps
import unittest
import sys
import time

CASE_TAG_FLAG = "__case_tag__"
CASE_DATA_FLAG = "__case_data__"
CASE_ID_FLAG = "__case_id__"
CASE_INFO_FLAG = "__case_info__"
CASE_RUN_INDEX_FlAG = "__case_run_index_flag__"
CASE_SKIP_FLAG = "__unittest_skip__"
CASE_SKIP_REASON_FLAG = "__unittest_skip_why__"


def check_prefix(name, test_prefix=Settings.TEST_PREFIX):
    """
    检查名称的前缀是否符合test_prefix，忽略大小写
    :param name: 名称
    :param test_prefix: 前缀
    :return: bool
    """
    return name.lower().startswith(test_prefix)


def skip(reason):
    def wrap(func):
        return unittest.skip(reason)(func)
    return wrap


def skip_if(condition, reason):
    def wrap(func):
        return unittest.skipIf(condition, reason)(func)
    return wrap


def data(params, asserts):
    """注入测试数据，可以做为测试用例的数据驱动
    :param params: 测试数据组成的list
    :param asserts: 断言数据组成的list
    :return:
    """
    def wrap(func):
        param_data = {'params': params, 'asserts': asserts}
        setattr(func, CASE_DATA_FLAG, param_data)
        return func
    return wrap


def tag(*tag_type):
    """指定测试用例的标签，可以作为测试用例分组使用，用例默认会有Tag.al标签，支持同时设定多个标签，如：
    @tag(Tag.V1_0_0, Tag.SMOKE)
    def test_func(self):
        pass

    :param tag_type:标签类型，在tag.py里边自定义
    :return:
    """
    def wrap(func):
        _tag_type = [_tag.lower() for _tag in tag_type]
        if not hasattr(func, CASE_TAG_FLAG):
            tags = {'all'}
            tags.update(_tag_type)
            setattr(func, CASE_TAG_FLAG, tags)
        else:
            getattr(func, CASE_TAG_FLAG).update(_tag_type)
        return func
    return wrap


def _assertion(cap_func=None, cap_dir=None, **cap_kwargs):
    """用来装饰PUnittest类中所有的AssertXxx方法，提供日志，和失败截图，
        并且当出现断言异常不会立即终止用例，而是等用例结束后抛出所有的断言异常"""
    def wrapper(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            try:
                logger.info('[Assert]: {0}{1}'.format(func.__name__, format(args[1:])))
                return func(*args, **kwargs)
            except AssertionError as e:
                args[0].Exc_Stack.append(e)
                if cap_func is not None and cap_dir is not None:
                    cap_name = "{}_{}.png".format(
                        time.strftime("%Y-%m-%d_%H-%M-%S"), getattr(args[0], '_testMethodName')
                    )
                    cap_func(cap_dir, cap_name, **cap_kwargs)
        return wrap
    return wrapper


def _handler(rerun=Settings.CASE_FAIL_RERUN, cap_func=None, cap_dir=None, **cap_kwargs):
    """处理测试用例，为用例添加格式化的日志。并提供失败重跑机制。"""
    def wrapper(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            _testcase_name = getattr(args[0], '_testMethodName')
            _testcase_doc = getattr(args[0], '_testMethodDoc')
            _testclass_name = args[0].__class__.__name__
            _testclass_doc = args[0].__class__.__doc__
            rerun_time = rerun
            while rerun_time > 0:
                try:
                    logger.info('[TestCase]: {0}.{1} {2}|{3}'.format(
                        _testclass_name, _testcase_name, _testclass_doc, _testcase_doc))
                    logger.info('[TestProgress]: {0}/{1} [RerunTime]: NO.{2}'.format(
                        getattr(func, CASE_RUN_INDEX_FlAG), TestCaseHandler.actual_case_num, rerun - rerun_time + 1))
                    args[0].clear_exc_stack()
                    result = func(*args, **kwargs)
                    # 用例执行完毕抛出所有可能存在的AssertionError异常
                    args[0].raise_exc()
                    logger.info('[TestResult]: Pass!')
                    return result
                except AssertionError as e:
                    rerun_time -= 1
                    if rerun_time <= 0:
                        logger.error('[TestResult]: Fail!')
                        raise e
                except Exception as e:
                    rerun_time -= 1
                    if rerun_time <= 0:
                        _, _, exc_traceback = sys.exc_info()
                        logger.error('[TestResult]: Error!')
                        if cap_func is not None and cap_dir is not None:
                            cap_name = "{}_{}.png".format(
                                time.strftime("%Y-%m-%d_%H-%M-%S"), getattr(args[0], '_testMethodName')
                            )
                            cap_func(cap_dir, cap_name, **cap_kwargs)
                        raise e
        return wrap
    return wrapper


def _feed_data(*args, **kwargs):
    def wrap(func):
        @wraps(func)
        def _wrap(self):
            return func(self, *args, **kwargs)
        return _wrap
    return wrap


class TestCaseHandler:
    actual_case_num = 0
    total_case_num = 0

    @classmethod
    def create_case_id(cls):
        cls.total_case_num += 1
        return cls.total_case_num

    @classmethod
    def create_actual_run_index(cls):
        cls.actual_case_num += 1
        return cls.actual_case_num

    @staticmethod
    def modify_func_name(func, index):
        """修改函数名字，实现排序，并且根据DDT数据的编号在函数名后添加编号 eg test_fight >> test_00001_fight_#1
        :param func:
        :param index:
        :return:
        """
        case_id = TestCaseHandler.create_case_id()
        setattr(func, CASE_ID_FLAG, case_id)
        func_name = func.__name__.replace(
            Settings.TEST_PREFIX, Settings.TEST_PREFIX + "_{:05d}".format(case_id)
        )
        if index is not None:
            func_name += "_#{0}".format(index)
        return func_name

    @staticmethod
    def create_case_with_case_data(func):
        """根据原有测试函数创建新的带参数的测试函数"""
        result = dict()
        test_data = getattr(func, CASE_DATA_FLAG)
        params = test_data['params']
        asserts = test_data['asserts']
        for index, (param, assert_) in enumerate(zip(params, asserts), 1):
            if not hasattr(func, CASE_SKIP_FLAG):
                setattr(func, CASE_RUN_INDEX_FlAG, TestCaseHandler.create_actual_run_index())
            func_name = TestCaseHandler.modify_func_name(func, index)
            result[func_name] = _handler(
                cap_func=Settings.CAP_FUNC,
                cap_dir=Settings.CAP_DIR,
                **Settings.CAP_KWARGS
            )(_feed_data(params=param, asserts=assert_)(func))
        return result

    @staticmethod
    def create_case_without_case_data(func):
        """根据原有测试函数创建新的不带参数的测试函数"""
        result = dict()
        if not hasattr(func, CASE_SKIP_FLAG):
            setattr(func, CASE_RUN_INDEX_FlAG, TestCaseHandler.create_actual_run_index())
        func_name = TestCaseHandler.modify_func_name(func, None)
        result[func_name] = _handler(
            cap_func=Settings.CAP_FUNC,
            cap_dir=Settings.CAP_DIR,
            **Settings.CAP_KWARGS
        )(func)
        return result

    @staticmethod
    def classify_funcs(funcs_dict):
        """将类中的函数进行归类"""
        funcs = dict()
        cases = dict()
        asserts = dict()
        for attr in funcs_dict:
            if check_prefix(attr):
                cases[attr] = funcs_dict[attr]
            elif attr.startswith("assert"):
                if attr not in ["assertMultiLineEqual", "assertIsInstance"]:
                    asserts[attr] = funcs_dict[attr]
                else:
                    funcs[attr] = funcs_dict[attr]
            else:
                funcs[attr] = funcs_dict[attr]
        return funcs, cases, asserts

    @staticmethod
    def filter_cases_by_tags(tags, func):
        """根据func的tags进行过滤"""
        tags = [x.lower() for x in tags]
        name = func.__name__
        if check_prefix(name):
            _tags = getattr(func, CASE_TAG_FLAG, {'all'})
            for _tag in _tags:
                if _tag in tags:
                    break
            else:
                msg = "不包含需要执行的Tag: {}".format(', '.join(tags))
                filtered_func = skip(msg)(func)
                return filtered_func
        return func


def get_test_set(api_data=None):
    """获取测试用例集"""
    if Settings.TEST_SET_FORM == "CODE":
        test_set = CodeTestSet(Settings.TEST_PREFIX, Settings.SKIP_PREFIX).test_set
    elif Settings.TEST_SET_FORM == "EXCEL":
        test_set = ExcelTestSet(Settings.TEST_PREFIX, Settings.SKIP_PREFIX).test_set
    elif Settings.TEST_SET_FORM == "API":
        test_set = ApiTestSet(api_data, Settings.TEST_PREFIX, Settings.SKIP_PREFIX).test_set
    else:
        test_set = CodeTestSet(Settings.TEST_PREFIX, Settings.SKIP_PREFIX).test_set
    return test_set


def handle_asserts(funcs, asserts):
    """
    装饰测试类中的每个断言函数，将其放入funcs
    :param funcs:
    :param asserts:
    :return:
    """
    for name, assert_ in asserts.items():
        # 将装饰过的assert方法加入类
        funcs.update(
            {name: _assertion(
                cap_func=Settings.CAP_FUNC,
                cap_dir=Settings.CAP_DIR,
                **Settings.CAP_KWARGS)(assert_)}
        )
    return funcs


def handle_case_by_code(funcs, cases, tags):
    """
    直接处理代码中测试类中的每个函数，将每个测试函数处理为测试用例
    :param funcs: 测试类中的普通函数，和装饰后的assert函数
    :param cases: 测试类中以prefix开头的测试函数（测试用例）
    :param tags: 需要运行的测试用例的tag
    :return: funcs更新装饰后的测试函数
    """
    for test_func in cases.values():
        # 根据tag进行过滤
        test_func = TestCaseHandler.filter_cases_by_tags(tags, test_func)
        # 注入用例信息
        case_info = "{}.{}".format(test_func.__module__, test_func.__name__)
        setattr(test_func, CASE_INFO_FLAG, case_info)
        # 注入测试数据
        if hasattr(test_func, CASE_DATA_FLAG):
            funcs.update(TestCaseHandler.create_case_with_case_data(test_func))
        else:
            funcs.update(TestCaseHandler.create_case_without_case_data(test_func))
    return funcs


def handle_case_by_test_set(funcs, cases, tags, cls_name, test_set):
    """
    根据外在测试集处理测试类中的每个函数，将每个测试函数处理为测试用例
    :param funcs: 测试类中的普通函数，和装饰后的assert函数
    :param cases: 测试类中以prefix开头的测试函数（测试用例）
    :param tags: 需要运行的测试用例的tag
    :param cls_name: 类名称
    :param test_set: 测试集
    :return: funcs更新装饰后的测试函数
    """
    for test_case in test_set:
        _cls_name = test_case['TestClass'] if 'TestClass' in test_case else None
        _case_name = test_case['TestCase'] if 'TestCase' in test_case else None
        _case_desc = test_case['CaseDescription'] if 'CaseDescription' in test_case else None
        _tags = test_case['Tags'] if 'Tags' in test_case else None
        _skip = test_case['Skip'] if 'Skip' in test_case else None
        _params = test_case['ParamsData'] if 'ParamsData' in test_case else None
        _asserts = test_case['AssertResult'] if 'AssertResult' in test_case else None
        if cls_name == _cls_name:
            for test_func in cases.values():
                if test_func.__name__ == _case_name:
                    # 为测试函数绑定tag装饰器
                    test_func = tag(*_tags)(test_func)
                    # 根据tag进行过滤
                    test_func = TestCaseHandler.filter_cases_by_tags(tags, test_func)
                    # 为测试函数绑定skip装饰器，只认定excel中的skip标识，忽略编码中的skip标识
                    if _skip is not None:
                        test_func = skip(_skip)(test_func)
                    # 修改测试函数的文档注释
                    if _case_desc:
                        setattr(test_func, '__doc__', _case_desc)
                    # 为测试函数绑定data装饰器
                    if _asserts is not None and _params is not None:
                        test_func = data(_params, _asserts)(test_func)
                        funcs.update(TestCaseHandler.create_case_with_case_data(test_func))
                    else:
                        funcs.update(TestCaseHandler.create_case_without_case_data(test_func))
    return funcs


def filter_skipped_class(cls, funcs):
    """
    如果一个testclass中的所有testfunc都跳过不执行，则该testclass也被标记为跳过，
    setupClass和teardownClass也不执行
    :param cls: 测试类
    :param funcs: 包括所有需要执行的函数
    :return: 更新后的测试类
    """
    if_skip = True
    for func_name, func_obj in funcs.items():
        if check_prefix(func_name):
            if not hasattr(func_obj, CASE_SKIP_FLAG):
                if_skip = False
                break
    if check_prefix(cls.__name__):
        setattr(cls, CASE_SKIP_FLAG, if_skip)
    return cls


class Meta(type):
    def __new__(mcs, cls_name, supers, cls_dict):
        test_set = get_test_set()
        tags = Settings.RUN_TAGS
        funcs, cases, asserts = TestCaseHandler.classify_funcs(cls_dict)
        funcs = handle_asserts(funcs, asserts)
        if test_set is None:
            funcs = handle_case_by_code(funcs, cases, tags)
        else:
            funcs = handle_case_by_test_set(funcs, cases, tags, cls_name, test_set)
        cls = super(Meta, mcs).__new__(mcs, cls_name, supers, funcs)
        cls = filter_skipped_class(cls, funcs)
        return cls
