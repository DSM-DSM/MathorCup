# -*- coding: utf-8 -*-            
# @Time : 2023/1/17 10:53
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import numpy as np
import pandas as pd


def check_pressing(data):
    data['current_time_1'] = (data['current_time'] - 1662768000) / 3600
    groups = data.groupby('id')
    n = data['id'].unique().shape[0]
    arr = np.zeros((n, 1))
    for key, values in groups:
        value = values[values['retainable'] == 0]
        a = min(value['current_time_1'] - value['serviceFirstTime'])
        arr[key] = a
    status = True
    if sum(arr[arr > -2]) > 0:
        status = False
    return status, min(arr)


data = pd.read_excel('../../data/2.1/535(5, 5)过程.xlsx')
check_pressing(data)
