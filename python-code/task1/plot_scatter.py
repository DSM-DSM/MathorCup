# -*- coding: utf-8 -*-            
# @Time : 2022/12/21 15:40
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

aunt = pd.read_excel('../../data/aunt.xlsx')
order = pd.read_excel('../../data/order.xlsx')
aunt_loc = aunt.iloc[:, 2:5] / 1000
order_loc = order.iloc[:, 5:7] / 1000

aunt_loc = aunt_loc.values
order_loc = order_loc.values

plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.scatter(aunt_loc[:, 0], aunt_loc[:, 1], marker='o', linewidths=0.1)
plt.title('阿姨分布图')
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('../../pic/aunt.png')
plt.show()

plt.scatter(order_loc[:, 0], order_loc[:, 1], c='red', marker='^', linewidths=0.1)
plt.title('订单分布图')
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('../../pic/order.png')
plt.show()
