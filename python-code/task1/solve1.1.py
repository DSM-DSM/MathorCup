# -*- coding: utf-8 -*-            
# @Time : 2022/12/24 13:02
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
import numpy as np
import cvxpy as cp
from assign import Assign
from aunt import Aunt
from order import Order


def main():
    df_aunt = pd.read_excel('../../data/aunt.xlsx')
    df_order = pd.read_excel('../../data/order.xlsx')
    aunt = Aunt(df_aunt)
    order = Order(df_order)
    assign = Assign(aunt, order, (20, 20))
    obj_final, n_final = assign.time_solve()
    print(obj_final / n_final)
    # (22,22) 0.41002979477637985


if __name__ == '__main__':
    main()
