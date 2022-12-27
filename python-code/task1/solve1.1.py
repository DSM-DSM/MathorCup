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

df_aunt = pd.read_excel('../../data/aunt.xlsx')
df_order = pd.read_excel('../../data/order.xlsx')
aunt = Aunt(df_aunt)
order = Order(df_order)
assign = Assign(aunt, order, (15, 17))
obj_final, n_final = assign.grid_iter_solve()
# def main():
#     pass
#
#
# if __name__ == '__main__':
#     main()
# 0.2927433967011257 <==> (14, 15) --> 210
# 0.2743800584178908 <==> (40, 10) --> 400
# 0.2821612307628567 <==> (30, 10) --> 300
# 0.2820914161613672 <==> (25, 10) --> 250
# 0.2910592585490601 <==> (10, 25) --> 250
# 0.2916803866195784 <==> (10, 30) --> 300
# 0.2927832507497483 <==> (15, 15) --> 225
# 0.2933496207388876 <==> (15, 17) --> 255  *********
# 0.2900483282140392 <==> (15, 18) --> 270
# 0.2274083719782299 <==> (50, 50) --> 2500
# 0.1981679986273807 <==> (100, 100) --> 10000
