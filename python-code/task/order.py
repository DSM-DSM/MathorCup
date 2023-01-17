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
        self.data['aunt_id'] = -1
        self.data['serviceStartTime'] = -1
        self.serviceStartTimeRange = int(max(data['serviceFirstTime']) - min(data['serviceFirstTime']))
        self.TimeRange = self.serviceStartTimeRange + int(
            max(data[data['serviceFirstTime'] == max(data['serviceFirstTime'])].serviceLastTime))
        self.data['retainable'] = 1
        self.data['current_time'] = 1662768000

    def get_order(self, timestamp, solver_mode):
        """

        :param solver_mode: 求解器模式
        :param timestamp: 当前时间戳
        :return:
        """
        id_1 = self.data['assign_status'] == 0
        # order['available']根据求解器模式模式定义的
        id_2 = self.data['available'] == 1
        if solver_mode['mode'] == 'on-line':
            id_3 = self.data['createTime'] <= timestamp
            index = id_1 & id_2 & id_3
        else:
            index = id_1 & id_2
        return self.data[index]

    def update_order_assign_status(self, aunt_order_indexer):
        order_id = aunt_order_indexer.order_id.values
        id = self.data.index.values
        index = [i in order_id for i in id]
        self.data.loc[index, 'assign_status'] = 1

    def updata_order_available(self, timestamp, pressing_order):
        """

        :param pressing_order: 压单的时间约束
        :param timestamp:
        :return:
        """
        self.data['available'] = 0
        firstime = self.data.serviceFirstTime.values
        lastime = self.data.serviceLastTime.values + firstime
        index1 = np.array([i <= (timestamp + pressing_order) for i in firstime])
        index2 = np.array([i >= timestamp for i in lastime])
        index = index1 & index2
        self.data.loc[index, 'available'] = 1

    def if_retainable(self, timestamp):
        """

        :param timestamp:
        :return:
        """
        self.data['current_time'] = 1662768000 + 3600 * timestamp
        index = self.data['aunt_id'] != -1
        self.data.loc[index, 'retainable'] = 0
