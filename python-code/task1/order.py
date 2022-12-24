# -*- coding: utf-8 -*-            
# @Time : 2022/12/24 12:52
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
import numpy as np


class Order:
    def __init__(self, data):
        """

        :param data:
        :param data['assign_status']: 订单是否被分配的状态（绝对量）
        :param data['available']: 订单某时间是否能被分配的状态（相对量）
        """
        self.data = data
        self.n = data.shape[0]
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


# data_order = pd.read_excel('../../data/order2.xlsx')
#
# order = Order(data_order)
# print(order.order['assign_status'])
# print(order.order['available'])
# order.updata_available_status(0)
