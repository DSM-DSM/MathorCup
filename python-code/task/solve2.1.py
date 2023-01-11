# -*- coding: utf-8 -*-            
# @Time : 2022/12/30 21:42
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import datetime
import pandas as pd
import numpy as np
from assign import Assign
from aunt import Aunt
from order import Order
import matplotlib as mpl
import matplotlib.pyplot as plt


def plot_score_linechart(data, shape, path):
    mpl.rcParams['font.sans-serif'] = ['simhei']
    mpl.rcParams['axes.unicode_minus'] = False
    rag = max(data[:, 3]) - min(data[:, 3])
    date_series = pd.date_range(start='2023-1-1 0:00:00', end='2023-1-1 ' + str(rag) + ':00:00', freq="30min")
    df = pd.DataFrame(data[:, 0:3], index=date_series, columns=['obj', 'n_exist', 'n_assign'])

    ax = df.plot(secondary_y=['n_exist', 'n_assign'], x_compat=True, grid=True)
    ax.set_title(f"目标函数值-订单数,gridshape:{shape}")
    ax.set_ylabel('目标函数值')
    ax.grid(linestyle="--", alpha=0.3)

    ax.right_ax.set_ylabel('订单数')
    plt.savefig(path + f'双轴折线图/双轴折线图，{shape}.png')
    plt.show()


def main():
    start = datetime.datetime.now()
    path1 = '../../data/'
    path2 = '../../pic/'
    df_aunt = pd.read_excel(path1 + 'aunt.xlsx', index_col='id')
    df_order = pd.read_excel(path1 + 'order.xlsx', index_col='id')
    df_aunt = df_aunt.sort_index()
    df_order = df_order.sort_index()
    aunt = Aunt(df_aunt)
    order = Order(df_order)
    shape = (1, 1)
    assign = Assign(aunt, order, shape)
    assign.use_high_quality = False
    assign.pressing_order = 2
    assign.enlarge_time_axis = 3
    assign.future_aunt = 2
    obj_final, n_final, result, plot_data = assign.time_solve()
    print(obj_final / n_final)
    end = datetime.datetime.now()
    print('Running time: %s Seconds' % (end - start))
    plot_score_linechart(plot_data, shape, path2)
    df_aunt.to_excel(path1 + f'test/aunt{shape}.xlsx')
    df_order.to_excel(path1 + f'test/order{shape}.xlsx')
    result.to_excel(path1 + f'test/{shape}过程.xlsx')


if __name__ == '__main__':
    main()
