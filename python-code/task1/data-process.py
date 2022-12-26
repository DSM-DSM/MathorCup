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
    aunt = pd.read_excel('../../data/附件2：阿姨数据.xlsx')
    order = pd.read_excel('../../data/附件1：订单数据.xlsx')
    score = aunt['serviceScore']

    # 计算距离
    aunt_loc = aunt.iloc[:, 2:5] / 1000
    order_loc = order.iloc[:, 5:7] / 1000

    # 处理时间信息
    # order ['id', 'createTime', 'serviceFirstTime', 'serviceLastTime','serviceUnitTime', 'x', 'y']
    # aunt ['id', 'serviceScore', 'x', 'y']
    order['serviceUnitTime'] = order['serviceUnitTime'] / 60
    order['serviceLastTime'] = (order['serviceLastTime'] - order['serviceFirstTime']) / 3600
    order['serviceFirstTime'] = (order['serviceFirstTime'] - min(order['serviceFirstTime'])) / 3600

    order['x1'] = order['x'] / 1000
    order['y1'] = order['y'] / 1000
    aunt['x1'] = aunt['x'] / 1000
    aunt['y1'] = aunt['x'] / 1000

    order.to_excel('../../data/order.xlsx')
    aunt.to_excel('../../data/aunt.xlsx')


if __name__ == '__main__':
    main()
