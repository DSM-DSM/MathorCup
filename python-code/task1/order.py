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

    def get_order(self, timestamp):
        """

        :param timestamp:
        :return:
        """
        if timestamp == 0:
            id_1 = self.data['assign_status'] == 0
            id_2 = self.data['available'] == 1
            index = id_1 & id_2
            return self.data[index]
        else:
            id_1 = self.data['assign_status'] == 0
            id_2 = self.data['available'] == 1
            index = id_1 & id_2
            return self.data[index]

    def update_order_assign_status(self, idx):
        idx_lst = [i for lst in idx for i in lst]
        id = self.data.id.values
        index = [i in idx_lst for i in id]
        self.data.loc[index, 'assign_status'] = 1

    def updata_order_available(self, timestamp):
        """

        :param timestamp:
        :return:
        """
        self.data['available'] = 0
        firstime = self.data.serviceFirstTime.values
        index = [i <= timestamp for i in firstime]
        self.data.loc[index, 'available'] = 1
