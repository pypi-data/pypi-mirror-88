# -*- coding:utf-8 -*-
# @Author    : g1879
# @date      : 2020-11-17
# @email     : g1879@qq.com
# @File      : targets.py

from typing import Union

from .common import format_loc
from .paths import Paths


class Targets(object):
    """此类用于管理待爬取目标                                           \n
    待爬目标由一个3位的元组表示：(列名, [属性名, 正则表达式])              \n
    如：('作者', 'text', '(.*)')
    其中后两位可省略，当省略时默认获取元素text值
    即传入'作者' 与传入 ('作者', 'text', '(.*)')是等价的
    示例：
        - '作者'
        - '链接', 'href'
        - '页数', 'text', '(\\d+)'
    """

    def __init__(self,
                 paths: Union[Paths, dict],
                 targets: Union[list, tuple] = None):
        """初始化                              \n
        :param paths: Paths对象
        :param targets: 要爬取的内容集合
        """
        if isinstance(paths, Paths):
            self._paths = paths

        elif isinstance(paths, dict):
            self._paths = Paths(paths_dict=paths)

        else:
            raise TypeError('paths参数只能是Paths或dict类型。')

        self._targets = []
        self._start_stop_row = (None, None)

        if targets:
            self.set_targets(targets)

    @property
    def paths(self) -> Paths:
        """返回页面路径管理对象"""
        return self._paths

    @property
    def start_stop_row(self) -> tuple:
        """返回起止行号"""
        return self._start_stop_row

    @start_stop_row.setter
    def start_stop_row(self, start_stop: Union[list, tuple]):
        """设置起止行号"""
        if not isinstance(start_stop, (list, tuple)) or not 0 < len(start_stop) < 3:
            raise ValueError

        self._start_stop_row = (start_stop[0], None) if len(start_stop) == 1 else start_stop

    @property
    def targets(self) -> list:
        """返回所有目标"""
        return self._targets

    @targets.setter
    def targets(self, targets: Union[list, tuple]) -> None:
        """批量设置目标                            \n
        :param targets: 列表或元组格式的目标信息
        :return: None
        """
        self.set_targets(targets)

    def set_targets(self, targets: Union[list, tuple]) -> None:
        """批量设置目标                            \n
        :param targets: 列表或元组格式的目标信息
        :return: None
        """
        if not isinstance(targets, (tuple, list)):
            raise TypeError(f'请传入tuple或list，不是{type(targets)}')

        # 当第一个元素是范围设置时
        if isinstance(targets[0], (tuple, list)) and isinstance(targets[0][0], (int, type(None))):
            if not 0 < len(targets) < 3:
                raise ValueError

            start = 1
            self._start_stop_row = (targets[0][0], None) if len(targets[0]) == 1 else targets[0]

        else:
            start = 0
            self._start_stop_row = (None, None)

        for i in targets[start:]:
            xpath_str, attr_str, re_str = format_loc(i)
            self.add_target(xpath_str, attr_str, re_str)

    def add_target(self, col: str, attr: str = None, re_str: str = None) -> None:
        """添加待爬目标                                     \n
        :param col: 对象的路径，xpath 或 css selector
        :param attr: 要抓取的熟悉
        :param re_str: 提取属性内容的正则表达式
        :return: None
        """
        path_str = self.paths.cols[col]
        attr = attr or 'text'
        re_str = re_str or '(.*)'

        self._targets.append((path_str, attr, re_str))
