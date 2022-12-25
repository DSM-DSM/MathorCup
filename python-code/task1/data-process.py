# -*- coding: utf-8 -*-            
# @Time : 2022/12/20 22:31
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix


def main():
    # 导入数据
    aunt = pd.read_excel('../../data/aunt.xlsx')
    order = pd.read_excel('../../data/order.xlsx')
    score = aunt['serviceScore']

    # 计算距离
    aunt_loc = aunt.iloc[:, 2:5] / 1000
    order_loc = order.iloc[:, 5:7] / 1000
    dist = distance_matrix(aunt_loc, order_loc)

    # 处理时间信息
    # order ['id', 'createTime', 'serviceFirstTime', 'serviceLastTime','serviceUnitTime', 'x', 'y']
    # aunt ['id', 'serviceScore', 'x', 'y']
    order['serviceUnitTime'] = order['serviceUnitTime'] / 60
    order['serviceLastTime'] = (order['serviceLastTime'] - order['serviceFirstTime']) / 3600
    order['serviceFirstTime'] = (order['serviceFirstTime'] - min(order['serviceFirstTime'])) / 3600

    order['x'] = order['x'] / 1000
    order['y'] = order['y'] / 1000
    aunt['x'] = aunt['x'] / 1000
    aunt['y'] = aunt['x'] / 1000
    order.to_excel('../../data/order2.xlsx')
    aunt.to_excel('../../data/aunt.xlsx')


if __name__ == '__main__':
    main()
