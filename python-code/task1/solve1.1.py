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
from solve import solve_prob

df_aunt = pd.read_excel('../../data/aunt.xlsx', index_col='id')
df_order = pd.read_excel('../../data/order.xlsx', index_col='id')
aunt = Aunt(df_aunt)
order = Order(df_order)
assign = Assign(aunt, order, (20, 20))

t = 0
assign.grid_iter()
cur_order = order.get_order(timestamp=t)
cur_aunt = aunt.get_aunt(timestamp=t)
prob, x = assign.solve(solve_prob, cur_aunt, cur_order)

# id_x = df_aunt['district_x'] == 0
# id_y = df_aunt['district_y'] == 5
# id = id_x & id_y
# df_aunt[id]
# def main():
#     pass
#
#
# if __name__ == '__main__':
#     main()
