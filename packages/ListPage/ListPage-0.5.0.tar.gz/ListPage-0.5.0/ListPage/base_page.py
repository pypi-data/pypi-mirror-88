# -*- coding:utf-8 -*-
# @Author    : g1879
# @date      : 2020-11-17
# @email     : g1879@qq.com
# @File      : base_page.py

import re
from abc import abstractmethod
from typing import Union, List

from DrissionPage import MixPage, Drission
from DrissionPage.common import DrissionElement

from .common import format_loc
from .targets import Targets
from .paths import Paths


class BasePage(MixPage):

    def __init__(self,
                 paths: Union[Paths, dict],
                 index_url: str = None,
                 mode: str = 's',
                 timeout: float = 10,
                 drission: Drission = None):
        """列表页面类的基类
        :param paths: 页面元素管理对象
        :param index_url: 列表第一页url
        :param mode: 's' 或 'd'，MixPage模式
        :param timeout: 超时时间
        :param drission: Drission对象
        """
        super().__init__(drission, mode, timeout)
        self._set_paths(paths)
        self.index_url = index_url
        self._current_page_num = 1

        if index_url:
            self.to_first_page()

    @property
    def paths(self) -> Paths:
        """返回页面路径管理对象"""
        return self._paths

    def _set_paths(self, paths_or_dict) -> None:
        """设置路径对象
        :param paths_or_dict: Paths对象或dict
        :return: None
        """
        if isinstance(paths_or_dict, Paths):
            self._paths = paths_or_dict

        elif isinstance(paths_or_dict, dict):
            self._paths = Paths().from_dict(paths_or_dict)

        else:
            raise ValueError('paths格式错误')

    def to_first_page(self) -> None:
        """跳转到首页"""
        if self.index_url:
            self.get(self.index_url, go_anyway=True, show_errmsg=True, retry=6, interval=10)
            self._current_page_num = 1
        else:
            raise ValueError('首页url未设置')

    def get_current_rows(self) -> List[DrissionElement]:
        """返回当前页行对象"""
        return self.eles(f'{self.paths.type}:{self.paths.rows}')

    def get_current_list(self,
                         targets: Targets,
                         show_msg: bool = True) -> List[List[str]]:
        """返回当前页结果列表
        :param targets: Targets对象
        :param show_msg: 是否显示获取到的内容
        :return: 结果列表
        """
        rows = self.get_current_rows()
        return self._get_list(rows, targets, show_msg)

    @abstractmethod
    def get_list(self,
                 targets: Targets,
                 show_msg: bool = True,
                 wait: float = 0) -> List[List[str]]:
        """返回指定范围的结果列表，由子类实现
        :param targets: Targets对象
        :param show_msg: 是否实时显示获取到的内容
        :param wait: 每页之间等待时间
        :return: 结果列表
        """
        pass

    @abstractmethod
    def to_next_page(self, wait: float = None) -> bool:
        """跳转到下一页"
        :param wait: 跳转前的等待时间
        :return: 是否跳转成功
        """
        pass

    def _get_list(self,
                  rows: list,
                  targets: Targets,
                  show_msg: bool = True) -> List[List[str]]:
        """从行对象列表中获取须要的属性值
        :param rows: 行对象组成的列表
        :param targets: Targets对象
        :param show_msg: 是否实时显示获取到的信息
        :return: 结果列表
        """
        results_list = []
        start, stop = targets.start_stop_row

        for row in rows[start: stop]:
            row_result = [self._get_value(row, target) for target in targets.targets]

            if show_msg:
                print(row_result)

            results_list.append(row_result)

        return results_list

    def _get_value(self,
                   ele_or_page: Union[MixPage, DrissionElement],
                   loc: Union[str, list, tuple]) -> Union[str, None]:
        """根据定位从元素中获取值
        :param ele_or_page: 获取值的目标对象
        :param loc: 定位符：(xpath或css路径, [属性名, 正则])
        :return: 获取到的属性值
        """

        xpath_str, attr_str, re_str = format_loc(loc)

        try:
            data = ele_or_page.ele(f'{self.paths.type}:{xpath_str}').attr(attr_str)
            r = re.search(re_str, data, flags=re.DOTALL)
            return r.group(1)

        except AttributeError:
            return None
