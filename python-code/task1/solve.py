# -*- coding: utf-8 -*-            
# @Time : 2022/12/24 18:43
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import cvxpy as cp
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix


def generate_constrain_matrix(aunt, order):
    n_order = order.shape[0]
    n_aunt = aunt.shape[0]
    dist = distance_matrix(order.loc[:, ['x', 'y']],
                           aunt.loc[:, ['x', 'y']])
    constrain_matrix = np.zeros((n_order, n_aunt), dtype=int)
    for i in range(n_order):
        time_i = order.iloc[0, :].serviceLastTime
        for j in range(n_aunt):
            if dist[i, j] > time_i * 15:
                constrain_matrix[i, j] = 0
            else:
                constrain_matrix[i, j] = 1
    return constrain_matrix


def solver(aunt, order, timestamp, *args):
    if args:
        high_quality_aunt_id = args[0]
    else:
        high_quality_aunt_id = aunt.index
    n_order = order.shape[0]
    n_aunt = aunt.shape[0]
    dist = distance_matrix(order.loc[:, ['x', 'y']],
                           aunt.loc[:, ['x', 'y']])
    # 1.定义变量
    x = cp.Variable((n_order, n_aunt), boolean=True)
    alpha = cp.Parameter(nonneg=True, value=0.78)
    beta = cp.Parameter(nonneg=True, value=0.025)
    gamma = cp.Parameter(nonneg=True, value=0.195)

    # 2.创建需要的矩阵和表达式
    # A代表服务分,B代表通行距离,C代表阿姨的服务间隔时间
    A = x @ aunt['serviceScore'].values
    B = cp.multiply(dist, x)
    time_step = aunt['first'].to_numpy()
    avail_time = aunt['avail_time'].to_numpy()
    if_high_quality = np.zeros((n_aunt,), dtype=int)
    for i in range(n_aunt):
        if time_step[i] == 1:
            # 第i个阿姨是第一次分配到订单
            time_step[i] = 0.5
        if time_step[i] == 0:
            time_step[i] = timestamp - avail_time[i]
        if aunt.iloc[i, :].name in high_quality_aunt_id:
            if_high_quality[i] = 1
    C = cp.sum(x, axis=0) @ time_step

    # 3.设置目标函数和约束
    obj = (cp.sum(A) * alpha - beta * cp.sum(B) - C * gamma) / n_order
    objective = cp.Maximize(obj)
    constrain_matrix = generate_constrain_matrix(aunt, order)
    # axis = 1 / 0 <==> 按行/列求和
    constrains = [cp.sum(x, axis=0) <= if_high_quality,
                  x <= constrain_matrix,
                  cp.sum(x, axis=0) <= 1]
    for i in range(n_order):
        if np.sum(constrain_matrix) >= 1:
            constrains += [cp.sum(x, axis=1)[i] == 1]

    # 4.求解问题
    prob = cp.Problem(objective, constrains)
    prob.solve(solver=cp.GLPK_MI)
    df = pd.DataFrame(x.value)
    return prob, df
