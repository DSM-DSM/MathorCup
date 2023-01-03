# -*- coding: utf-8 -*-            
# @Time : 2022/12/30 21:42
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
from assign import Assign
from aunt import Aunt
from order import Order
import datetime


#  high_quality_aunt    1                   0               time
#      (5 ,5 ) ******************* *******************  ----------------------
#      (3 ,3 ) ******************* *******************  ----------------------
#      (1 ,1 ) ******************* 0.61079308096349900  0:36:11.617671 Seconds
#      (2 ,2 ) ******************* 0.59394942729087370  0:02:55.411861 Seconds


def main():
    start = datetime.datetime.now()
    df_aunt = pd.read_excel('../../data/aunt.xlsx', index_col='id')
    df_order = pd.read_excel('../../data/order.xlsx', index_col='id')
    df_aunt = df_aunt.sort_index()
    df_order = df_order.sort_index()
    aunt = Aunt(df_aunt)
    order = Order(df_order)
    shape = (2, 2)
    assign = Assign(aunt, order, shape)
    assign.use_high_quality = False
    assign.pressing_order = 2
    assign.enlarge_time_axis = 3
    obj_final, n_final = assign.time_solve()
    print(obj_final / n_final)
    end = datetime.datetime.now()
    print('Running time: %s Seconds' % (end - start))
    df_aunt.to_excel(f'../../data/2.1/aunt{shape}.xlsx')
    df_order.to_excel(f'../../data/2.1/order{shape}.xlsx')


if __name__ == '__main__':
    main()
