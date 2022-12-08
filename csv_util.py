#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os

from xcsv.csv_not_open_exception import CSVNotOpenException
from xcsv.header import Header
from xcsv.row import Row


class CSVUtil:
    """
    CSV 文件实用程序
    """

    __csv_file = None
    __cached_header = None
    __tmp_filename = None

    def read(self) -> Row:
        """
        读取 CSV 数据并返回为 Python 对象, 每调用一次，就会读取一行新的数据
        :return: Row
        """

        self.__check_csv_open()

        line = self.__csv_file.readline()
        line_object = self.__parse_csv_string_line(line=line)

        return Row(row=line_object)

    def write(self, row: Row) -> None:
        self.__check_csv_open()
        row_str = self.__convert_row_to_csv_str(row=row)

        self.__csv_file.write(row_str + '\n')
        self.__csv_file.flush()

    def write_all(self, rows: list) -> None:
        self.__check_csv_open()

    def open(self, filename: str = None) -> None:
        """
        打开 CSV 文件
        :param filename: 文件位置
        :return: None
        """

        if (filename is None) or (len(filename) <= 0):
            return

        self.__tmp_filename = filename

        if os.path.exists(filename):
            self.__csv_file = open(filename, 'r', encoding="UTF-8")

        self.__check_csv_open()

    def close(self) -> None:
        """
        关闭 CSV 文件
        :return: None
        """
        if not self.__csv_file.closed:
            self.__csv_file.close()

    def read_header(self, cache: bool = True) -> Header:
        """
        读取 CSV 文件头部
        :param cache: 是否利用缓存加速
        :return: CSV 头部
        """

        self.__check_csv_open()

        if cache:
            if self.__cached_header:
                return self.__cached_header

        current_file_pointer_position = self.__csv_file.tell()
        self.__csv_file.seek(0)

        line = self.__csv_file.readline()

        cols = self.__parse_csv_string_line(line=line)

        header = Header()
        header.fill_content(content=cols)

        self.__csv_file.seek(current_file_pointer_position, current_file_pointer_position + 1)

        self.__cached_header = header

        return header

    def read_all(self) -> tuple:
        """
        读取全部的 CSV 数据，并转换成 Row 类型构成的元组
        :return: 全部 CSV 数据
        """
        self.__check_csv_open()


        self.read_header()

        tmp = []

        for line in self.__csv_file.readlines():
            tmp.append(Row(row=self.__parse_csv_string_line(line=line)))

        return tuple(tmp)

    def __parse_csv_string_line(self, line: str) -> tuple:
        """
        将 CSV 字符串解析为 Python 对象
        :param line: CSV 字符串数据
        :return: Python 对象
        """

        if (len(line) <= 0) or (line is None):
            return ()

        tmp = []

        line = line.strip()
        cols = line.split(",")

        for col in cols:
            if (len(col) <= 0) or (col is None):
                tmp.append(None)
            else:
                tmp.append(col.strip())

        return tuple(tmp)

    def row_generator(self, sums=None):
        """
        Row 生成器，每次迭代，可以返回一个 Row 对象
        :return: Row
        """
        self.__csv_file.seek(0)
        # print(self.__csv_file.readline(), end="")
        self.__csv_file.readline()
        tmp = []
        for i in range(sums):
            line = self.__csv_file.readline()
            row = self.__parse_csv_string_line(line=line)
            if len(row) == 0:
                break
            tmp.append(row)
            yield tmp[i]
            
    def __check_csv_open(self):
        if self.__csv_file is None:
            raise CSVNotOpenException("'{}' is not open.".format(self.__tmp_filename))

    def __convert_row_to_csv_str(self, row: Row) -> str:
        """
        将 Row 对象转换为 CSV 字符串
        :param row: Row 对象
        :return: 字符串
        """
        return row.__str__()


if __name__ == '__main__':
    pass
