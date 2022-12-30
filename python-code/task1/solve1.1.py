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
#      (5 ,5 ) ******************* 0.58774298433294400  0:00:42.580772 Seconds
#      (3 ,3 ) ******************* 0.59602846391035460  0:01:05.857174 Seconds
#      (1 ,1 ) ******************* 0.60982068762292620  0:08:36.454157 Seconds
#      (2 ,2 ) ******************* 0.59868447551536490  0:01:02.419661 Seconds


def main():
    start = datetime.datetime.now()
    df_aunt = pd.read_excel('../../data/aunt.xlsx', index_col='id')[:20]
    df_order = pd.read_excel('../../data/order.xlsx', index_col='id')[:50]
    aunt = Aunt(df_aunt)
    order = Order(df_order)
    shape = (1, 1)
    assign = Assign(aunt, order, shape)
    assign.use_high_quality = False
    obj_final, n_final = assign.time_solve()
    print(obj_final / n_final)
    end = datetime.datetime.now()
    print('Running time: %s Seconds' % (end - start))
    df_aunt.to_excel(f'../../data/aunt1.2{shape}.xlsx')
    df_order.to_excel(f'../../data/order1.2{shape}.xlsx')


if __name__ == '__main__':
    main()
