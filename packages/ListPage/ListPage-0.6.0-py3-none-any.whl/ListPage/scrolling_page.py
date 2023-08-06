# -*- coding:utf-8 -*-
# @Author    : g1879
# @date      : 2020-08-18
# @email     : g1879@qq.com
# @File      : scrolling_page.py
# 依赖：DrissionPage >= v1.1.3
"""
ScrollingPage类是滚动加载式列表页基类，继承自DrissionPage的MixPage类。
专门用于处理滚动加载式列表页面。如新闻列表页。
它抽取了滚动加载列表共有的特征，即栏目名、列表容器、数据行、列，
封装了对页面的基本读取和操作方法，只能在MixPage的driver模式下工作。

它封装了以下方法：
- 获取当前数据列表
- 获取当前行元素对象
- 获取新加载的数据列表
- 获取新加载的元素对象
- 滚动一页

返回列表格式：
    [
        ['参数1结果', '参数2结果', ...],
        ['参数1结果', '参数2结果', ...],
        ...
    ]
"""

from time import sleep
from typing import Union

from DrissionPage import Drission

from .recorder import Recorder
from .targets import Targets
from .base_page import BasePage
from .paths import Paths


class ScrollingPage(BasePage):
    """列表页基类
    列表页基类提取了列表页面共有的特征，即栏目名、数据行容器、数据行、列，
    封装了对页面的基本读取和操作方法
    """

    def __init__(self,
                 paths: Union[Paths, dict],
                 index_url: str = None,
                 timeout: float = 10,
                 drission: Drission = None):
        """初始化函数                      \n
        :param drission: 驱动器对象
        :param index_url: 首页url
        :param paths: 页面元素定位语句
        """
        super().__init__(paths, index_url, 'd', timeout, drission)
        self.index_url = index_url

        self.container = self.ele(f'{self.paths.type}:{self.paths.container}')
        self._last_row = None

    def get_list(self,
                 targets: Targets,
                 scroll_times: int = 0,
                 wait: float = 0,
                 show_msg: bool = True,
                 recorder: Recorder = None,
                 return_data: bool = True) -> list:
        """获取若干次滚动后的数据列表            \n
        :param targets: 要爬取的内容
        :param scroll_times: 滚动次数
        :param wait: 滚动后等待几秒
        :param show_msg: 是否显示爬取信息
        :param recorder: 记录器对象
        :param return_data: 是否返回数据
        :return: 结果列表
        """
        if show_msg:
            print('第1页')

        data_list = []
        first_list = self.get_current_list(targets, show_msg)

        if return_data:
            data_list = first_list

        if recorder:
            recorder.add_data(data_list)

        for i in range(scroll_times):
            self.to_next_page(wait)

            if show_msg:
                print(f'\n第{i + 2}页')

            new_list = self.get_new_list(targets, show_msg)

            if not new_list:
                self.click_more_btn(wait=wait)
                new_list = self.get_new_list(targets, show_msg)

            if not new_list:
                break

            if return_data:
                data_list.extend(new_list)

            if recorder:
                recorder.add_data(new_list)

        if recorder:
            recorder.record()

        return data_list

    def get_current_rows(self) -> list:
        """返回当前页行对象"""
        rows = super().get_current_rows()
        self._last_row = rows[-1]
        return rows

    def get_new_list(self, targets: Targets, show_msg: bool = True) -> list:
        """获取新加载的数据列表                      \n
        :param targets: 待爬取的内容
        :param show_msg: 是否显示爬取到的内容
        :return: 数据列表
        """
        rows = self.get_new_rows()
        return self._get_list(rows, targets, show_msg)

    def get_new_rows(self) -> list:
        """获取新加载的行对象"""
        if self._last_row is None:
            return self.get_current_rows()

        rows = []

        # TODO: 修改
        if self.paths.type == 'xpath':
            pass
        else:
            pass

        # 行是容器直接子元素
        if self.paths.rows[0] == '/' and self.paths.rows[1] != '/':
            xpath_str = f'xpath:/following-sibling::{self.paths.rows[1:]}'
            rows = self._last_row.eles(xpath_str, timeout=2)

        # 在整个容器下级查找行
        else:
            xpath_str = f'xpath:/following::{self.paths.rows.lstrip("/")}'
            js = 'return arguments[1].contains(arguments[0])'

            for i in self._last_row.eles(xpath_str, timeout=2):
                if not i.run_script(js, self.container.inner_ele):
                    break

                rows.append(i)

        if rows:
            self._last_row = rows[-1]

        return rows

    def click_more_btn(self, wait: float = 1) -> None:
        """点击加载更多按钮                      \n
        :param wait: 点击按钮后等待秒数
        :return: None
        """
        if self.paths.more_btn:
            more_btn = self.ele(f'{self.paths.type}:{self.paths.more_btn}')

            if more_btn and more_btn.is_displayed():
                more_btn.click(by_js=True)
                sleep(wait)

    def to_next_page(self, wait: float = 1) -> None:
        """滚动一页                      \n
        :param wait: 滚动后等待秒数
        :return: None
        """
        self.scroll_to('bottom')
        sleep(wait)
