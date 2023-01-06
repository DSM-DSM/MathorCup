# -*- coding: utf-8 -*-            
# @Time : 2022/12/24 13:02
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
#      (3 ,3 ) ******************* 0.54519125137766770  0:09:51.196651 Seconds
#      (2 ,2 ) ******************* 0.54528576253197900  0:13:21.659300 Seconds
#      (1 ,1 ) ******************* 0.55693158461683940  0:54:47.133616 Seconds


def main():
    start = datetime.datetime.now()
    df_aunt = pd.read_excel('../../data/aunt.xlsx', index_col='id')
    df_order = pd.read_excel('../../data/order.xlsx', index_col='id')
    aunt = Aunt(df_aunt)
    order = Order(df_order)
    shape = (1, 1)
    assign = Assign(aunt, order, shape)
    assign.use_high_quality = False
    obj_final, n_final, result = assign.time_solve()
    print(obj_final / n_final)
    end = datetime.datetime.now()
    print('Running time: %s Seconds' % (end - start))
    # df_aunt.to_excel(f'../../data/1.1/aunt{shape}.xlsx')
    # df_order.to_excel(f'../../data/1.1/order{shape}.xlsx')
    # result.to_excel('../../data/result/result22.xlsx')


if __name__ == '__main__':
    main()
