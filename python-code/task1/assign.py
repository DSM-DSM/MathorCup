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
        self.get_grid_info()

    def get_grid_info(self):
        try:
            self.x_max = max(self.aunt.data['x_od'].max(), self.order.data['x_od'].max())
            self.x_min = min(self.aunt.data['x_od'].min(), self.order.data['x_od'].min())
            self.y_max = max(self.aunt.data['y_od'].max(), self.order.data['y_od'].max())
            self.y_min = min(self.aunt.data['y_od'].min(), self.order.data['y_od'].min())
        except TypeError:
            raise 'data中不存在列x_od或y_od'

    def grid(self, data_to_grid, n_row):
        """
        将数据点按照网格划分
        :param n_row:
        :param data_to_grid:
        :param gridshape: 元组表示几行几列
        :return:
        """
        eps = 10
        x_range = np.linspace(self.x_min, self.x_max, self.gridshape[0] + 1)
        y_range = np.linspace(self.y_min, self.y_max, self.gridshape[1] + 1)
        x_range[0], x_range[-1] = x_range[0] - eps, x_range[-1] + eps
        y_range[0], y_range[-1] = y_range[0] - eps, y_range[-1] + eps
        dis_x, dis_y = [], []
        for i in range(n_row):
            for j in range(self.gridshape[0]):
                if x_range[j] <= data_to_grid['x_od'].iloc[i] < x_range[j + 1]:
                    dis_x.append(j)
            for k in range(self.gridshape[1]):
                if y_range[k] <= data_to_grid['y_od'].iloc[i] < y_range[k + 1]:
                    dis_y.append(k)
        data_to_grid['district_x'] = dis_x
        data_to_grid['district_y'] = dis_y

    def grid_iter(self):
        self.grid(self.order.data, self.n_order)
        self.grid(self.aunt.data, self.n_aunt)

    def get_grid(self, data, region_x, region_y):
        id_x = data['district_x'] == region_x
        id_y = data['district_x'] == region_y
        id = id_x & id_y
        return data[id]

    def solve(self, solve_prob, aunt, order):
        result1, result2 = [], []
        for i in range(self.gridshape[0]):
            for j in range(self.gridshape[1]):
                aunt = self.get_grid(aunt, i, j)
                order = self.get_grid(order, i, j)
                if aunt.shape[0] > 0 and order.shape[0] > 0:
                    prob, x = solve_prob(aunt, order)
                    result1.append(prob)
                    result2.append(x)
        return result1, result2
