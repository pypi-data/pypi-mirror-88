# -*- coding:utf-8 -*-
# @Author    : g1879
# @date      : 2020-11-17
# @email     : g1879@qq.com
# @File      : paths.py

from typing import Union


class Paths(object):
    """路径管理对象                        \n
    用于管理列表页面中关键元素的路径信息"""
    __attrs__ = ['rows', 'cols', 'page_count', 'next_btn', 'more_btn', 'container']

    def __init__(self, paths: dict = None):
        """初始化
        :param paths: 包含路径信息的字典
        """
        self._type = None

        self._rows = None
        self._cols = {}
        self._next_btn = None
        self._pages_count = None
        self._more_btn = None
        self._container = None

        if paths:
            self.from_dict(paths)

    def __call__(self) -> dict:
        """调用时把路径信息以字典格式返回"""
        return self.as_dict()

    @property
    def type(self) -> str:
        """返回路径的类型，css或xpath"""
        return self._type

    @property
    def rows(self) -> str:
        """返回行元素的路径"""
        return self._rows

    @rows.setter
    def rows(self, path: str) -> None:
        """设置行元素的路径         \n
        :param path: 行元素的路径
        :return: None
        """
        self._rows = path

    @property
    def next_btn(self) -> str:
        """返回下一页按钮的路径"""
        return self._next_btn

    @next_btn.setter
    def next_btn(self, path: str) -> None:
        """设置下一页按钮的路径         \n
        :param path: 下一页按钮的路径
        :return: None
        """
        self._next_btn = path

    @property
    def pages_count(self) -> Union[str, list, tuple]:
        """返回总页数元素的定位符列表"""
        return self._pages_count

    @pages_count.setter
    def pages_count(self, path_or_loc: Union[str, list, tuple]) -> None:
        """设置总页数元素的定位符                  \n
        :param path_or_loc: 总页数元素的定位符
        :return: None
        """
        if isinstance(path_or_loc, (list, tuple)) and not 0 < len(path_or_loc) < 4:
            raise ValueError

        self._pages_count = path_or_loc

    @property
    def more_btn(self) -> str:
        """返回加载更多按钮元素的路径"""
        return self._more_btn

    @more_btn.setter
    def more_btn(self, path: str) -> None:
        """设置加载更多按钮元素的路径              \n
        :param path:加载更多按钮元素的路径
        :return: None
        """
        self._more_btn = path

    @property
    def container(self) -> str:
        """返回滚动列表页的容器路径"""
        return self._container

    @container.setter
    def container(self, path: str) -> None:
        """设置滚动列表页的容器路径    \n
        :param path: 容器的路径
        :return: None
        """
        self._container = path

    @property
    def cols(self) -> dict:
        """返回保存的列路径"""
        return self._cols

    def get_col(self, col_name: str) -> str:
        """返回某列元素的路径
        :param col_name: 列名
        :return: 列的路径
        """
        return self._cols[col_name] if col_name in self._cols else None

    def set_cols(self, cols_data: Union[dict, list, tuple]) -> None:
        """批量设置列路径                               \n
        :param cols_data: list或tuple格式保存的列信息
        :return: None
        """
        if isinstance(cols_data, dict):
            self._cols = cols_data

        elif isinstance(cols_data, (list, tuple)):
            # 一维数组，即 (key, paths_or_dict)
            if len(cols_data) == 2 and isinstance(cols_data[0], str) and isinstance(cols_data[1], str):
                self.set_col(cols_data[0], cols_data[1])

            # 二维数组，即 ((key, paths_or_dict), (key, paths_or_dict), ...)
            else:
                for i in cols_data:
                    if (not isinstance(i, (list, tuple)) or len(i) != 2
                            or not isinstance(i[0], str) or not isinstance(i[1], str)):
                        raise TypeError

                    self.set_col(i[0], i[1])

        else:
            raise TypeError('参数cols类型错误。')

    def set_col(self, col_name: str, path: str) -> None:
        """设置一列的路径                  \n
        :param col_name: 列名
        :param path: 列的路径
        :return: None
        """
        self._cols[col_name] = path

    def as_dict(self) -> dict:
        """把路径信息以字典格式返回"""
        return {key: getattr(self, key) for key in self.__attrs__}

    def from_dict(self, cols_data: dict):
        """从字典中读取并设置路径信息                  \n
        :param cols_data: 以字典形式保存的列信息
        :return: 返回自己
        """
        for argument in cols_data:
            if argument in self.__attrs__:
                if argument == 'cols':
                    self.set_cols(cols_data['cols'])
                else:
                    setattr(self, argument, cols_data[argument])

        return self


class Xpaths(Paths):
    def __init__(self):
        """类型为xpath的路径类"""
        super().__init__()
        self._type = 'xpath'


class CssPaths(Paths):
    def __init__(self):
        """类型为css selector的路径类"""
        super().__init__()
        self._type = 'css'
