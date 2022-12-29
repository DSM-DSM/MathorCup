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
#      (5 ,5 ) 0.30278788976999920 0.35516730817918870  0:00:34.485767 Seconds
#      (3 ,3 ) 0.37853846578688016 0.41633563956018793  0:00:54.790292 Seconds
#      (1 ,1 ) 0.59081606277804300 0.60022536191526690
#      (2 ,2 ) 0.38556398316595580 0.43747829740941097  0:01:00.053095 Seconds
start = datetime.datetime.now()
df_aunt = pd.read_excel('../../data/aunt.xlsx', index_col='id')
df_order = pd.read_excel('../../data/order.xlsx', index_col='id')
aunt = Aunt(df_aunt)
order = Order(df_order)
assign = Assign(aunt, order, (5, 5))
assign.use_high_quality = False
obj_final, n_final = assign.time_solve()
print(obj_final / n_final)
end = datetime.datetime.now()
print('Running time: %s Seconds' % (end - start))
df_aunt.to_excel('../../data/1.1aunt.xlsx')
df_order.to_excel('../../data/1.1order.xlsx')


# def main():
#     pass
#
#
# if __name__ == '__main__':
#     main()
