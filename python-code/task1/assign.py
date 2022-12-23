# -*- coding: utf-8 -*-            
# @Time : 2022/12/23 15:21
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
import numpy as np


class Assign:
    def __init__(self, data):
        """

        :param data: 读入的原始数据
        :param n: 数据的行数
        """
        self.data = data
        self.n = data.shape[0]

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


class Order(Assign):
    def __init__(self, data):
        """

        :param data:
        :param data['assign_status']: 订单是否被分配的状态（绝对量）
        :param data['available']: 订单某时间是否能被分配的状态（相对量）
        """
        super(Order, self).__init__(data)
        self.data['assign_status'] = 0
        self.data['available'] = 0

    def get_order(self, timestamp):
        """

        :param timestamp:
        :return:
        """
        if timestamp == 0:
            return self.data[self.data['serviceFirstTime'] == timestamp]
        else:
            idx = [self.data['assign_status'] == 0 and self.data['available'] == 1]
            return self.data[idx]

    def updata_available_status(self, timestamp):
        """
        随时间更新可供分配订单状态
        每次循环应该在get_order之前被调用
        :param timestamp: 当前时间节点
        :return:
        """
        available = []
        for i in range(self.n):
            if self.data['serviceFirstTime'].iloc[i] <= timestamp and self.data['assign_status'].iloc[i] == 0:
                available.append(1)
            else:
                available.append(0)
        self.data['available'] = available


class Aunt(Assign):
    def __init__(self, data):
        super(Aunt, self).__init__(data)
        self.data['avail_time'] = 0

    def updata_aunt_status(self):
        pass

    def calculate_time(self):
        pass

# data_order = pd.read_excel('../../data/order2.xlsx')
# order = Order(data_order)
# print(order.data['assign_status'])
# print(order.data['available'])
# order.updata_available_status(0)
