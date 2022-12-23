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
# plt.scatter(aunt_loc[:, 0], aunt_loc[:, 1], marker='o', linewidths=0.1)
# plt.title('阿姨分布图')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.savefig('../../pic/aunt.png')
# plt.show()

order['serviceUnitTime'] = order['serviceUnitTime'] / 60
order['serviceLastTime'] = (order['serviceLastTime'] - order['serviceFirstTime']) / 3600
order['serviceFirstTime'] = (order['serviceFirstTime'] - min(order['serviceFirstTime'])) / 3600

marker = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']
order_num = []

for i in range(13):
    order_num.append(order[order['serviceFirstTime'] == i].shape[0])
    plt.scatter(order[order['serviceFirstTime'] == i].iloc[:, 5], order[order['serviceFirstTime'] == i].iloc[:, 6],
                c='red', marker=marker[i], linewidths=0.1)
    plt.title(f'订单分布图,订单Starttime={i}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(np.min(order['x']), np.max(order['x']))
    plt.ylim(np.min(order['y']), np.max(order['y']))
    plt.savefig(f'../../pic/order_starttime分布图{i}.png')
    plt.show()

plt.plot(range(13), order_num)
plt.title('order_starttime数量折线图')
plt.savefig(f'../../pic/order_starttime数量折线图.png')
plt.show()
