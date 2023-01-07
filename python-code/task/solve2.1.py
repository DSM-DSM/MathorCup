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
#      (3 ,3 ) ******************* 0.55962475119855800  0:13:51.849539 Seconds
#      (2 ,2 ) ******************* 0.56089487169637970  0:23:37.211425 Seconds
#      (1 ,1 ) ******************* 0.56350058788039490  1:53:14.278527 Seconds


def main():
    start = datetime.datetime.now()
    df_aunt = pd.read_excel('../../data/aunt.xlsx', index_col='id')
    df_order = pd.read_excel('../../data/order.xlsx', index_col='id')
    df_aunt = df_aunt.sort_index()
    df_order = df_order.sort_index()
    aunt = Aunt(df_aunt)
    order = Order(df_order)
    shape = (1, 1)
    assign = Assign(aunt, order, shape)
    assign.use_high_quality = False
    assign.pressing_order = 2
    assign.enlarge_time_axis = 3
    obj_final, n_final, result = assign.time_solve()
    print(obj_final / n_final)
    end = datetime.datetime.now()
    print('Running time: %s Seconds' % (end - start))
    df_aunt.to_excel(f'../../data/2.1/aunt{shape}.xlsx')
    df_order.to_excel(f'../../data/2.1/order{shape}.xlsx')
    result.to_excel('../../data/result/result22.xlsx')


if __name__ == '__main__':
    main()
