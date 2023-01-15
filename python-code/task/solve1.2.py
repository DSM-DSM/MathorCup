# -*- coding: utf-8 -*-            
# @Time : 2022/12/30 15:53
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
from assign import Assign
from aunt import Aunt
from order import Order
import datetime


def main():
    start = datetime.datetime.now()
    df_aunt = pd.read_excel('../../data/aunt.xlsx', index_col='id')
    df_order = pd.read_excel('../../data/order.xlsx', index_col='id')
    df_aunt = df_aunt.sort_index().head(20)
    df_order = df_order.sort_index().head(50)
    aunt = Aunt(df_aunt)
    order = Order(df_order)
    shape = (1, 1)
    assign = Assign(aunt, order, shape)
    assign.use_high_quality = False
    obj_final, n_final, result = assign.time_solve()
    # Score(1, 1): 0.40346554305965470
    # Score(2, 2): 0.34678236054821676
    # Score(2, 1): 0.43484661856178436
    print(obj_final / n_final)
    end = datetime.datetime.now()
    print('Running time: %s Seconds' % (end - start))
    assign.plot_order_aunt_route()
    # df_aunt.to_excel(f'../../data/1.2/aunt{shape}.xlsx')
    # df_order.to_excel(f'../../data/1.2/order{shape}.xlsx')
    # result.to_excel(f'../../data/1.2/过程1.2{shape}.xlsx')


if __name__ == '__main__':
    main()
