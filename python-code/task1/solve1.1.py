# -*- coding: utf-8 -*-            
# @Time : 2022/12/24 13:02
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
from assign import Assign
from aunt import Aunt
from order import Order

df_aunt = pd.read_excel('../../data/aunt.xlsx')
df_order = pd.read_excel('../../data/order.xlsx')
aunt = Aunt(df_aunt)
order = Order(df_order)
assign = Assign(aunt, order, (16, 15))
obj_final, n_final = assign.time_solve()
print(obj_final / n_final)

# (22,22)
# (20,20)
# (19,19)
# (18,18)
# (17,17) 0.35452089029360845
# (16,16) 0.39912246152969627
# (16,15) 0.40289120972633286
# (40,40) 0.21778516015368363

# def main():
#     pass
# if __name__ == '__main__':
#     main()
