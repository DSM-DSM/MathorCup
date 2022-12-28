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

# (22,22) 0.4100297947763798
# (20,20) 0.4273022412762358
# (19,19) 0.4322149866416236
# (18,18) 0.4448636581594178
# (17,17) 0.4325583198025164
# (16,16) 0.4606468364142121
# (16,15) 0.4690932707752045

# def main():
#     pass
# if __name__ == '__main__':
#     main()
