# -*- coding: utf-8 -*-            
# @Time : 2022/12/30 21:42
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import datetime
import warnings
import pandas as pd
import numpy as np
from assign import Assign
from aunt import Aunt
from order import Order


def check_pressing(data):
    data['current_time_1'] = (data['current_time'] - 1662768000) / 3600
    groups = data.groupby('id')
    n = data.index.unique().shape[0]
    arr = np.zeros((n, 1))
    for key, values in groups:
        value = values[values['retainable'] == 0]
        a = min(value['current_time_1'] - value['serviceFirstTime'])
        arr[key] = a
    status = True
    if sum(arr[arr > -2]) > 0:
        status = False
    return status, min(arr)


def main():
    start = datetime.datetime.now()
    path1 = '../../data/'
    df_aunt = pd.read_excel(path1 + 'aunt.xlsx', index_col='id')
    df_order = pd.read_excel(path1 + 'order.xlsx', index_col='id')
    df_aunt = df_aunt.sort_index()
    df_order = df_order.sort_index()
    aunt = Aunt(df_aunt)
    order = Order(df_order)
    shape = (5, 5)
    assign = Assign(aunt, order, shape)
    assign.use_high_quality = False
    assign.pressing_order = 2
    assign.future_aunt = 2
    assign.enlarge_time_axis = 3
    obj_final, n_final, result = assign.time_solve()
    print(obj_final / n_final)
    end = datetime.datetime.now()
    print('Running time: %s Seconds' % (end - start))
    if_pressing, min_pressing = check_pressing(result)
    if if_pressing:
        print(f'\n程序实现了压单，最晚压单时间为：{min_pressing}')
        df_aunt.to_excel(
            path1 + f'2.1/aunt{assign.pressing_order}{assign.future_aunt}{assign.enlarge_time_axis}{shape}.xlsx')
        df_order.to_excel(
            path1 + f'2.1/order{assign.pressing_order}{assign.future_aunt}{assign.enlarge_time_axis}{shape}.xlsx')
    else:
        warnings.warn('程序没有实现压单！')
    result.to_excel(
        path1 + f'2.1/{assign.pressing_order}{assign.future_aunt}{assign.enlarge_time_axis}{shape}过程.xlsx')


if __name__ == '__main__':
    main()
