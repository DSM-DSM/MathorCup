# -*- coding: utf-8 -*-            
# @Time : 2022/12/24 12:52
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
import numpy as np


class Aunt:
    def __init__(self, data):
        self.data = data
        self.n = self.data.shape[0]
        self.data['avail_time'] = 0
        self.data['assign_status'] = 0
        self.data['order'] = [[] for _ in range(self.n)]
        self.data['when_get_order'] = [[] for _ in range(self.n)]
        self.data['first'] = 1
        self.velocity = 15

    def updata_aunt_info(self, aunt_assign_index, timestamp):
        """
        aunt_assign_index需要事先转换为DataFrame类型
        :param timestamp:
        :param aunt_assign_index:
        :return:
        """
        for index in range(len(aunt_assign_index)):
            order_id = aunt_assign_index.iloc[index, 1]
            aunt_id = aunt_assign_index.iloc[index, 0]
            self.data.loc[aunt_id, :].order.append(order_id)
            self.data.loc[aunt_id, :].when_get_order.append(timestamp)
            self.data.loc[aunt_id, 'first'] = 0
            self.data.loc[aunt_id, 'assign_status'] = 1

    def updata_aunt_assign_status(self, timestamp):
        idx = self.data['avail_time'] <= timestamp
        self.data.loc[idx, 'assign_status'] = 0

    def get_aunt(self, timestamp, solver_mode):
        """

        :param solver_mode:
        :param timestamp:
        :return:
        """
        id_1 = self.data['assign_status'] == 0
        if solver_mode['mode'] == 'off-line':
            id_2 = self.data['avail_time'] <= timestamp
            index = id_1 & id_2
            return self.data[index]
        else:
            id_2 = self.data['avail_time'] <= timestamp + solver_mode['future_aunt']
            index = id_1 & id_2
            return self.data[index]


