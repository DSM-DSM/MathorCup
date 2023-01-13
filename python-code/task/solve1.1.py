# -*- coding: utf-8 -*-            
# @Time : 2022/12/24 13:02
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import numpy as np
import pandas as pd
from assign import Assign
from aunt import Aunt
from order import Order
import datetime


def main():
    start = datetime.datetime.now()
    df_aunt = pd.read_excel('../../data/aunt.xlsx', index_col='id')
    df_order = pd.read_excel('../../data/order.xlsx', index_col='id')
    aunt = Aunt(df_aunt)
    order = Order(df_order)
    shape = (2, 2)
    assign = Assign(aunt, order, shape)
    assign.use_high_quality = False
    assign.plot_interpolation()
    # obj_final, n_final, result = assign.time_solve()
    # print(obj_final / n_final)
    # end = datetime.datetime.now()
    # print('Running time: %s Seconds' % (end - start))
    # df_aunt.to_excel(f'../../data/1.1/aunt{shape}.xlsx')
    # df_order.to_excel(f'../../data/1.1/order{shape}.xlsx')
    # result.to_excel(f'../../data/1.1/{shape}过程.xlsx')


if __name__ == '__main__':
    main()
