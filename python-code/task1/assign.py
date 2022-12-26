# -*- coding: utf-8 -*-            
# @Time : 2022/12/23 15:21
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
import numpy as np
from order import Order
from aunt import Aunt
import cvxpy as cp


def calculate_dist(x1, x2, y1, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class Assign(Aunt, Order):
    def __init__(self, aunt, order, gridshape):
        """

        :param data: 读入的原始数据
        :param n: 数据的行数
        """
        self.aunt = aunt
        self.order = order
        self.n_aunt = aunt.data.shape[0]
        self.n_order = order.data.shape[0]
        self.gridshape = gridshape

    def grid(self, data_to_grid, n_row):
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
        x_range = np.linspace(x_min, x_max, self.gridshape[0] + 1)
        y_range = np.linspace(y_min, y_max, self.gridshape[1] + 1)
        x_range[0], x_range[-1] = x_range[0] - eps, x_range[-1] + eps
        y_range[0], y_range[-1] = y_range[0] - eps, y_range[-1] + eps
        dis_x = list()
        dis_y = list()
        for i in range(n_row):
            for j in range(self.gridshape[0]):
                if x_range[j] <= data_to_grid['x'].iloc[i] < x_range[j + 1]:
                    dis_x.append(j)
            for k in range(self.gridshape[1]):
                if y_range[k] <= data_to_grid['y'].iloc[i] < y_range[k + 1]:
                    dis_y.append(k)
        data_to_grid['district_x'] = dis_x
        data_to_grid['district_y'] = dis_y

    def grid_iter(self):
        return self.grid(self.aunt.data, self.n_aunt), \
               self.grid(self.order.data, self.n_order)

    def get_grid(self, data, region_x, region_y):
        id_x = data['district_x'] == region_x
        id_y = data['district_x'] == region_y
        id = id_x & id_y
        return data[id]

    def solve(self, solve_prob, aunt, order):
        # for i in self.gridshape[0]:
        #     for j in self.gridshape[1]:
        #         aunt = self.get_grid(self.aunt.data, i, j)
        #         order = self.get_grid(self.order.data, i, j)
        #         result = solve(aunt, order)
        i, j = 0, 0
        aunt = self.get_grid(aunt, i, j)
        order = self.get_grid(order, i, j)
        result = solve_prob(aunt, order)
        return result
