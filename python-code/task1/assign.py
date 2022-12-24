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


class Assign(Order, Aunt):
    def __init__(self, aunt, order):
        """

        :param data: 读入的原始数据
        :param n: 数据的行数
        """
        super(Assign, self).__init__(aunt)
        super(Assign, self).__init__(order)

    def grid(self, gridshape):
        """
        将数据点按照网格划分
        :param gridshape: 元组表示几行几列
        :return:
        """
        # 1.获取数据的基本信息
        eps = 10
        try:
            x_min, x_max = np.min(self.data['x']), np.max(self.data['x'])
            y_min, y_max = np.min(self.data['y']), np.max(self.data['y'])
        except KeyError:
            raise 'data中不存在列x或y'

        # 2.循环给数据附加标签1
        district = []
        x_range = np.linspace(x_min, x_max, gridshape[0] + 1)
        y_range = np.linspace(y_min, y_max, gridshape[1] + 1)
        x_range[0], x_range[-1] = x_range[0] - eps, x_range[-1] + eps
        y_range[0], y_range[-1] = y_range[0] - eps, y_range[-1] + eps
        print(x_range)
        print(y_range)
        for i in range(self.n):
            dis = list()
            for j in range(gridshape[0]):
                if x_range[j] <= self.data['x'].iloc[i] < x_range[j + 1]:
                    dis.append(j)
            for k in range(gridshape[1]):
                if y_range[k] <= self.data['y'].iloc[i] < y_range[k + 1]:
                    dis.append(k)
            # print(dis)
            # loc = dis[0] * dis[1]
            if len(dis) != 2:
                raise "位置列表维数错误！"
            district.append(dis)
        self.data['district'] = district

    def solve(self):
        pass




