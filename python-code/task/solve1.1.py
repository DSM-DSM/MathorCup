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
#      (3 ,3 ) ******************* 0.56965208253859060  0:09:02.922124 Seconds
#      (2 ,2 ) ******************* 0.59242664509726130  0:15:42.151474 Seconds
#      (1 ,1 ) ******************* 0.60996405265091140  1:33:42.307747 Seconds


def main():
    start = datetime.datetime.now()
    df_aunt = pd.read_excel('../../data/aunt.xlsx', index_col='id')
    df_order = pd.read_excel('../../data/order.xlsx', index_col='id')
    aunt = Aunt(df_aunt)
    order = Order(df_order)
    shape = (3, 3)
    assign = Assign(aunt, order, shape)
    assign.use_high_quality = False
    obj_final, n_final = assign.time_solve()
    print(obj_final / n_final)
    end = datetime.datetime.now()
    print('Running time: %s Seconds' % (end - start))
    df_aunt.to_excel(f'../../data/1.1/aunt{shape}.xlsx')
    df_order.to_excel(f'../../data/1.1/order{shape}.xlsx')


if __name__ == '__main__':
    main()
