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

start = datetime.datetime.now()
df_aunt = pd.read_excel('../../data/aunt.xlsx')
df_order = pd.read_excel('../../data/order.xlsx')
aunt = Aunt(df_aunt)
order = Order(df_order)
assign = Assign(aunt, order, (2, 2))
assign.use_high_quality = True
obj_final, n_final = assign.time_solve()
print(obj_final / n_final)
end = datetime.datetime.now()
print('Running time: %s Seconds' % (end - start))

#  high_quality_aunt    1                   0               time
#      (16,15) 0.20301235811603816 0.21321570090918196
#      (16,12) 0.20930552563197327 0.21321570090918196
#      (10,10) 0.21509575652426950 0.22437297677430199
#      (5 ,5 ) 0.23697440288046290 0.24944538647827816
#      (3 ,3 ) ******************* 0.25980304087495270  0:01:48.794033 Seconds
#      (1 ,1 ) ******************* 0.25980304087495270
#      (2 ,2 ) ******************* 0.25980304087495270  0:02:04.361812 Seconds

# def main():
#     pass
# if __name__ == '__main__':
#     main()
