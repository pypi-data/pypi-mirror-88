#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .settings import Settings
from .utils.parse_excel import ExcelParser
from .utils.logger import logger
from importlib import import_module
import unittest
import re
import os
import platform


class TestSet:
    def __init__(self, test_prefix, skip_prefix):
        self.test_set = []
        self.case_prefix = test_prefix.lower()
        self.skip_prefix = skip_prefix.lower()
        self.test_suite = unittest.TestSuite()

    @staticmethod
    def convert_to_pydata(string):
        """将测试用例中的字符串转换成python数据结构"""
        if string is None:
            return None
        elif isinstance(string, bool):
            return [string]
        else:
            param_list = string.split('\n')
            try:
                param_list = [eval(x.strip()) for x in param_list]
            except NameError:
                param_list = [x.strip() for x in param_list]
            return param_list

    @staticmethod
    def convert_params(params):
        """将测试用例中的ParamsData由字符串转换成python数据结构"""
        return TestSet.convert_to_pydata(params)

    @staticmethod
    def convert_asserts(asserts):
        """将测试用例中的AssertResult由字符串转换成python数据结构"""
        return TestSet.convert_to_pydata(asserts)

    @staticmethod
    def convert_tags(tags):
        """将测试用例中的Tag解析成列表"""
        # 将字符串移除换行符，并利用逗号分隔
        tag_list = ['all']
        if tags is not None:
            tags = [t.strip() for t in tags.replace('\n', '').split(',')]
            if len(tags) > 0:
                # 全部替换为小写
                tags = [tag.lower() for tag in tags]
                tag_list.extend(tags)
        return tag_list

    def filter_test_case(self, **titles):
        """
        根据表格中的title过滤测试用例
        :param titles: 关键字参数，每个参数名对应表格中的title
        :return: 测试用例组成的列表
        """
        if titles:
            for title, value in titles.items():
                self.test_set = list(filter(lambda d: title in d.keys(), self.test_set))
                self.test_set = list(filter(lambda d: d[title] == value, self.test_set))
        return self.test_set

    @staticmethod
    def import_package_by_path(path):
        """
        根据文件/目录的绝对路径加载其中的所有python文件
        :param path:
        :return: 可被import_module识别的字符串
        """
        root, file = os.path.split(path)
        if os.path.splitext(file)[-1] == '.py' and file != '__init__.py':
            root_dir_name = os.path.split(Settings.PROJECT_ROOT)[-1]
            if platform.system() == 'Windows':
                path_list = root.split('\\')
            else:
                path_list = root.split('/')
            path_list = path_list[path_list.index(root_dir_name) + 1:]
            path_list.append(os.path.splitext(file)[0])
            import_list = '.'.join(path_list)
            return import_list
        else:
            return None

    def load_test_set(self):
        raise NotImplementedError

    def convert_test_suite(self):
        raise NotImplementedError


class CodeTestSet(TestSet):
    """从本地代码处获取测试集"""
    def __init__(self, test_prefix, skip_prefix):
        super(CodeTestSet, self).__init__(test_prefix, skip_prefix)
        self.test_set = None

    def _load_test_case(self, package):
        """
        加载一个python package中的所有测试用例
        :param package: package
        :return:
        """
        for cls_name in package.__dict__:
            if cls_name.lower().startswith(self.case_prefix):
                cls = getattr(package, cls_name)
                for name, func in list(cls.__dict__.items()):
                    _name = re.sub(r'_#[\d]*', '', name)
                    _name = re.sub(self.case_prefix + r'_\d{5}', self.case_prefix, _name)
                    if _name.startswith(self.case_prefix):
                        case = cls(name)
                        self.test_suite.addTest(case)

    def load_test_set(self):
        pass

    def convert_test_suite(self):
        """
        遍历测试用例目录下的所有文件，类和方法，加载符合条件的测试方法（测试用例）;
        如果是文件，则直接加载
        :param: skip_prefix 目录和文件跳过的前缀
        :return: unittest.TestSuite 对象
        """
        if os.path.isdir(Settings.TEST_SUITE_PATH):
            for root, dir_, files in os.walk(Settings.TEST_SUITE_PATH):
                for file in files:
                    if not file.lower().startswith(self.skip_prefix) and file.split('.')[-1] == 'py':
                        abs_path = os.path.join(root, file)
                        import_list = self.import_package_by_path(abs_path)
                        if import_list is not None:
                            _import_list = import_list.split('.')
                            for sub_path in _import_list:
                                if sub_path.lower().startswith(self.skip_prefix):
                                    break
                            else:
                                package = import_module(import_list)
                                self._load_test_case(package)
        else:
            import_list = self.import_package_by_path(Settings.TEST_SUITE_PATH)
            if import_list is not None:
                for sub_path in import_list.split('.'):
                    if sub_path.lower().startswith(self.skip_prefix):
                        break
                else:
                    package = import_module(import_list)
                    self._load_test_case(package)
        return self.test_suite


class ExcelTestSet(TestSet):
    """从Excel中读取测试集"""
    def __init__(self, test_prefix, skip_prefix):
        super(ExcelTestSet, self).__init__(test_prefix, skip_prefix)
        try:
            self._excel = ExcelParser(Settings.TEST_EXCEL_PATH, 'TestCases')
        except FileNotFoundError:
            raise FileNotFoundError("Cannot found testcase file: {}".format(Settings.TEST_EXCEL_PATH))
        self.test_set = self.load_test_set()

    def load_test_set(self):
        """
        一次性读取所有测试用例
        :return: [dict(case), dict(case)...]
        """
        test_set = list()
        titles = [x for x in self._excel.get_row_values(1)]
        for row in range(2, self._excel.max_row + 1):
            test_case = dict()
            row_hidden = self._excel.worksheet.row_dimensions[row].hidden   # 获取该行是否被隐藏
            # 过滤被隐藏的行
            if row_hidden is False:
                values = [x for x in self._excel.get_row_values(row)]
                # 将行数据按照表头个数补齐None
                if len(values) < len(titles):
                    for i in range(len(titles) - len(values)):
                        values.append(None)
                for title, value in zip(titles, values):
                    if title == 'ParamsData':
                        params = self.convert_params(value)
                        test_case[title] = params
                    elif title == 'AssertResult':
                        asserts = self.convert_asserts(value)
                        test_case[title] = asserts
                    elif title == 'Tags':
                        tags = self.convert_tags(value)
                        test_case[title] = tags
                    else:
                        test_case[title] = value
                test_set.append(test_case)
        return test_set

    def convert_test_suite(self):
        """
        将excel表格中读取的测试用例生成 PUnittest 能识别的 TestSuite 对象，或者获取本地的所有测试文件
        :return: unittest.TestSuite 对象
        """
        if len(self.test_set) > 0:
            for test_case in self.test_set:
                _dir_name = test_case['TestDir'] if 'TestDir' in test_case else None
                _file_name = test_case['TestFile'] if 'TestFile' in test_case else None
                _cls_name = test_case['TestClass'] if 'TestClass' in test_case else None
                _case_name = test_case['TestCase'] if 'TestCase' in test_case else None
                try:
                    if not _file_name.lower().startswith(self.skip_prefix) \
                            or not _cls_name.lower().startswith(self.skip_prefix):
                        package = import_module('{0}.{1}'.format(_dir_name, _file_name))
                        cls = getattr(package, _cls_name)
                        for name, func in list(cls.__dict__.items()):
                            # 将装饰过的测试用例尾部序号移除
                            _name = re.sub(r'_#[\d]*', '', name)
                            # 将装饰过的测试用例首部还原
                            _name = re.sub(self.case_prefix + r'_\d{5}', self.case_prefix, _name)
                            if _name == _case_name:
                                case = cls(name)
                                self.test_suite.addTest(case)
                except Exception as e:
                    logger.error('Fail to load test case <{0}><{1}>: {2}'.format(_cls_name, _case_name, e))
        else:
            logger.error('Fail to load any test case, please check')
            raise RuntimeError('Fail to load any test case, please check')
        return self.test_suite


class ApiTestSet(TestSet):
    """从Http接口获取测试集"""
    def __init__(self, data, test_prefix, skip_prefix):
        super(ApiTestSet, self).__init__(test_prefix, skip_prefix)
        self.api_data = data
        self.test_set = self.load_test_set()

    def load_test_set(self):
        test_set = list()
        for item in self.api_data:
            test_case = dict()
            for k, v in item.items():
                if k == 'ParamsData':
                    params = self.convert_params(v)
                    test_case[k] = params
                elif k == 'AssertResult':
                    asserts = self.convert_asserts(v)
                    test_case[k] = asserts
                elif k == 'Tags':
                    tags = self.convert_tags(v)
                    test_case[k] = tags
                else:
                    test_case[k] = v
            test_set.append(test_case)
        return test_set

    def convert_test_suite(self):
        raise NotImplementedError("Not implemented yet...")
