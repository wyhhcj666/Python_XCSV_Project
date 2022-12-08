#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from xcsv.csv_util import CSVUtil

if __name__ == '__main__':
    csv_util = CSVUtil()
    csv_util.open(filename="xcsv/assets/2017_m_c.csv")
    csv_header = csv_util.read_header()
    # row_1 = csv_util.read()
    # row_2 = csv_util.read()
    # row_3 = csv_util.read()

    print(csv_header.parse())

    # all_content = csv_util.read_all()

    # print(row_1)
    # print(row_2)
    # print(row_3)

    # count = 10
    for row in csv_util.row_generator(8):
        print(row)
        # count -= count - 1
        # if count < 0:
        #     break

    csv_util.close()

