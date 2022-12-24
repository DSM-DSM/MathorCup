# -*- coding: utf-8 -*-            
# @Time : 2022/12/23 15:21
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
import numpy as np
from order import Order
from aunt import Aunt


def calculate_dist(x1, x2, y1, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class Assign(Aunt, Order):
    def __init__(self, aunt, order):
        """

        :param data: 读入的原始数据
        :param n: 数据的行数
        """
        self.aunt = aunt
        self.order = order
        self.n_aunt = aunt.data.shape[0]
        self.n_order = order.data.shape[0]

    def grid(self, data_to_grid, n_row, gridshape):
        """
        将数据点按照网格划分
        :param n_row:
        :param data_to_grid:
        :param gridshape: 元组表示几行几列
        :return:
        """
        # 1.获取数据的基本信息
        eps = 10
        try:
            x_min, x_max = np.min(data_to_grid['x']), np.max(data_to_grid['x'])
            y_min, y_max = np.min(data_to_grid['y']), np.max(data_to_grid['y'])
        except KeyError:
            raise 'data中不存在列x或y'

        # 2.循环给数据附加标签1
        district = []
        x_range = np.linspace(x_min, x_max, gridshape[0] + 1)
        y_range = np.linspace(y_min, y_max, gridshape[1] + 1)
        x_range[0], x_range[-1] = x_range[0] - eps, x_range[-1] + eps
        y_range[0], y_range[-1] = y_range[0] - eps, y_range[-1] + eps
        # print(x_range)
        # print(y_range)
        for i in range(n_row):
            dis = list()
            for j in range(gridshape[0]):
                if x_range[j] <= data_to_grid['x'].iloc[i] < x_range[j + 1]:
                    dis.append(j)
            for k in range(gridshape[1]):
                if y_range[k] <= data_to_grid['y'].iloc[i] < y_range[k + 1]:
                    dis.append(k)
            # print(dis)
            # loc = dis[0] * dis[1]
            if len(dis) != 2:
                raise "位置列表维数错误！"
            district.append(dis)
        data_to_grid['district'] = district

    def grid_iter(self, gridshape):
        return self.grid(self.aunt.data, self.n_aunt, gridshape), \
               self.grid(self.order.data, self.n_order, gridshape)

    def test(self):
        print(self.aunt.data.head(5))
        print(self.order.data.head(5))

    def solve(self):
        pass
