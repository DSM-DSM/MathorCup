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
        self.n = data.shape[0]
        self.data['avail_time'] = 0
        self.data['status'] = 0
        self.data['order'] = [[] for _ in range(self.n)]
        self.data['first'] = 0
        self.velocity = 15

    def updata_aunt_info(self, aunt_assign_index):
        '''
        aunt_assign_index需要事先转换为DataFrame类型
        :param aunt_assign_index: 包括是否被分配以及阿姨被分配的订单信息
        :return:
        '''
        for index, row in self.data.iterrows():
            row['order'].append(aunt_assign_index[index, 1])
            time = self.calculate_time()
            row['avail_time'] = time

    def calculate_time(self):
        return 0


data_aunt = pd.read_excel('../../data/aunt.xlsx')
aunt = Aunt(data_aunt)
