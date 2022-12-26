# -*- coding: utf-8 -*-            
# @Time : 2022/12/23 15:21
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
import numpy as np
from order import Order
from aunt import Aunt
from solve import solver


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
        self.grid_iter()

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

    def get_grid(self, obj, region_x, region_y):
        id_x = obj['district_x'] == region_x
        id_y = obj['district_y'] == region_y
        id = id_x & id_y
        return obj[id]

    def time_solve(self):
        timestamp = 0
        result1, result2, obj = self.grid_solve(solver=solver, timestamp=timestamp)
        return result1, result2, obj

    def grid_solve(self, solver, timestamp):
        aunt = self.aunt.get_aunt(timestamp)
        order = self.order.get_order(timestamp)
        result1, result2 = [], []
        assign_order = []
        for i in range(self.gridshape[0]):
            for j in range(self.gridshape[1]):
                cur_aunt = self.get_grid(aunt, i, j)
                cur_order = self.get_grid(order, i, j)
                print('位置坐标(%d,%d)' % (i, j))
                print('Order的个数：%d,Aunt的个数：%d' % (cur_order.shape[0], cur_aunt.shape[0]))
                if cur_aunt.shape[0] > 0 and cur_order.shape[0] > 0:
                    if cur_aunt.shape[0] >= cur_order.shape[0]:
                        prob, x = solver(cur_aunt, cur_order)
                        assign_order.append(cur_order.id.values)
                        result1.append(prob)
                        result2.append(self.aunt.extract_info_x(x, cur_aunt, cur_order))
                        print('\n')
                    else:
                        print("Order不能被全部分配！\n")
                else:
                    print('\n')
        self.order.update_order_assign_status(assign_order)
        self.aunt.updata_aunt_info(result2)
        obj = sum([res.value for res in result1])
        return result1, result2, obj

    def enlarge_gridsize(self):
        pass
