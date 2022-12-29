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
#      (16,15) 0.20301235811603816 0.21321570090918196
#      (16,12) 0.20930552563197327 0.21321570090918196
#      (10,10) 0.21509575652426950 0.22437297677430199
#      (5 ,5 ) 0.23697440288046290 0.24944538647827816
#      (3 ,3 ) ******************* 0.25980304087495270  0:01:48.794033 Seconds
#      (1 ,1 ) ******************* 0.36587687623354250  0:35:41.640175 Seconds
#      (2 ,2 ) ******************* 0.43747829740941097  0:01:01.876266 Seconds

def main():
    start = datetime.datetime.now()
    df_aunt = pd.read_excel('../../data/aunt.xlsx')
    df_order = pd.read_excel('../../data/order.xlsx')
    aunt = Aunt(df_aunt)
    order = Order(df_order)
    assign = Assign(aunt, order, (2, 2))
    assign.use_high_quality = False
    obj_final, n_final = assign.time_solve()
    print(obj_final / n_final)
    end = datetime.datetime.now()
    print('Running time: %s Seconds' % (end - start))
    df_aunt.to_excel('../../data/1.1aunt.xlsx')
    df_order.to_excel('../../data/1.1order.xlsx')


if __name__ == '__main__':
    main()
