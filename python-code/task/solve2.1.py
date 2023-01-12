# -*- coding: utf-8 -*-            
# @Time : 2022/12/30 21:42
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import datetime
import pandas as pd
import numpy as np
from assign import Assign
from aunt import Aunt
from order import Order
import matplotlib as mpl
import matplotlib.pyplot as plt


def main():
    start = datetime.datetime.now()
    path1 = '../../data/'
    df_aunt = pd.read_excel(path1 + 'aunt.xlsx', index_col='id')
    df_order = pd.read_excel(path1 + 'order.xlsx', index_col='id')
    df_aunt = df_aunt.sort_index()
    df_order = df_order.sort_index()
    aunt = Aunt(df_aunt)
    order = Order(df_order)
    shape = (1, 1)
    assign = Assign(aunt, order, shape)
    assign.use_high_quality = False
    assign.pressing_order = 4
    assign.future_aunt = 3
    assign.enlarge_time_axis = 3
    obj_final, n_final, result = assign.time_solve()
    print(obj_final / n_final)
    end = datetime.datetime.now()
    print('Running time: %s Seconds' % (end - start))
    df_aunt.to_excel(path1 + f'2.1/aunt433{shape}.xlsx')
    df_order.to_excel(path1 + f'2.1/order433{shape}.xlsx')
    result.to_excel(path1 + f'2.1/{shape}过程433.xlsx')


if __name__ == '__main__':
    main()
