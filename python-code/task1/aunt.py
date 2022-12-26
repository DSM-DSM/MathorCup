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
        self.data['status'] = 0
        self.data['order'] = [[] for _ in range(self.n)]
        self.data['first'] = 0
        self.velocity = 15

    def updata_aunt_info(self, aunt_assign_index):
        """
        aunt_assign_index需要事先转换为DataFrame类型
        :param aunt_assign_index:
        :return:
        """
        aunt_assign_index = self.transform_aunt_assign_index(aunt_assign_index)
        for index in range(len(aunt_assign_index)):
            order_id = aunt_assign_index.iloc[index, 1]
            aunt_id = aunt_assign_index.iloc[index, 0]
            self.data.loc[aunt_id, :].order.append(order_id)
            self.data.loc[aunt_id, 'first'] = 1
            self.data.loc[aunt_id, 'status'] = 1
            time = self.calculate_time()
            self.data.loc[aunt_id, 'avail_time'] = time
            self.updata_aunt_xy(aunt_id, order_id)

    def get_aunt(self, timestamp):
        """

        :param timestamp:
        :return:
        """
        if timestamp == 0:
            id_1 = self.data['status'] == 0
            id_2 = self.data['avail_time'] <= timestamp
            index = id_1
            return self.data[index]
        else:
            id_1 = self.data['status'] == 0
            id_2 = self.data['avail_time'] <= timestamp
            index = id_1 & id_2
            return self.data[index]

    def calculate_time(self):
        return 0

    def updata_aunt_xy(self, aunt_id, order_id):
        pass

    def extract_info_x(self, x, aunt, order):
        order_info = np.where(x == 1)[0]
        aunt_info = np.where(x == 1)[1]
        info = [[aunt.iloc[aunt_info[i]].id, order.iloc[order_info[i]].id] for i in range(len(order_info))]
        return info

    def transform_aunt_assign_index(self, aunt_assign_index):
        aunt = []
        order = []
        for i in range(len(aunt_assign_index)):
            for j in range(len(aunt_assign_index[i])):
                aunt.append(int(aunt_assign_index[i][j][0]))
                order.append(int(aunt_assign_index[i][j][1]))
        df = pd.DataFrame(columns=['aunt_id', 'order_id'])
        df['aunt_id'] = aunt
        df['order_id'] = order
        return df

# data_aunt = pd.read_excel('../../data/aunt.xlsx')
# aunt = Aunt(data_aunt)
