#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from xcsv.row import Row


class Header(Row):
    """
    代表一个 CSV 文件的表头
    """

    __content = ()

    def fill_content(self, content: tuple):
        self.__content = content

    def parse(self) -> tuple:
        return self.__content


if __name__ == '__main__':
    pass
