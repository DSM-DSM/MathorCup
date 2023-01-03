# -*- coding: utf-8 -*-            
# @Time : 2022/12/24 18:43
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import math
import warnings
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


def generate_travel_time_matrix(aunt, dist, timestamp):
    first_order = aunt['first'].to_numpy()
    avail_time = aunt['avail_time'].to_numpy()
    time_travel_matrix = np.floor(dist / 15) + 0.5
    for i in range(dist.shape[0]):
        for j in range(dist.shape[1]):
            if first_order[j] == 1:
                time_travel_matrix[:, j] = 0.5
                break
            time_travel_matrix[i, j] += (timestamp - avail_time[i])
    return time_travel_matrix


def solver(aunt, order, timestamp, n=1, status=True, *args):
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
    A = cp.sum(x @ aunt['serviceScore'].values)
    B = cp.sum(cp.multiply(dist, x))

    if_high_quality = np.zeros((n_aunt,), dtype=int)
    rank = order.serviceLastTime.rank(method='dense')
    urgent_order = rank[rank <= n].index
    travel_time_matrix = generate_travel_time_matrix(aunt, dist, timestamp)
    for i in range(n_aunt):
        if aunt.iloc[i, :].name in high_quality_aunt_id:
            if_high_quality[i] = 1
    C = cp.sum(cp.multiply(x, travel_time_matrix))

    # 3.设置目标函数和约束
    obj = (A * alpha - beta * B - gamma * C) / cp.sum(x)
    objective = cp.Maximize(obj)
    constrain_matrix = generate_constrain_matrix(aunt, order)
    # axis = 1 / 0 <==> 按行/列求和
    constrains = [cp.sum(x, axis=0) <= if_high_quality,
                  x <= constrain_matrix,
                  cp.sum(x, axis=0) <= 1]

    if status:
        for i in range(n_order):
            if np.sum(constrain_matrix, axis=1)[i] >= 1 and order.iloc[i, :].name in urgent_order:
                constrains += [cp.sum(x, axis=1)[i] == 1]
            else:
                constrains += [cp.sum(x, axis=1)[i] <= 1]
    else:
        constrains += [cp.sum(x, axis=1) <= 1]

    # 4.求解问题
    prob = cp.Problem(objective, constrains)
    prob.solve(solver=cp.GLPK_MI, qcp=True)
    df = pd.DataFrame(x.value)
    if status:
        if prob.status == 'optimal' and n >= 1:
            if n > max(rank):
                return None, 0
            n += 1
            prob_1, df_1 = solver(aunt, order, timestamp, n, True, high_quality_aunt_id)
            if prob_1 == None:
                return prob, df
            else:
                if prob_1.value > prob.value:
                    return prob_1, df_1
                else:
                    return prob, df
        if prob.status == 'infeasible' and n > 1:
            return None, 0
        if prob.status == 'infeasible' and n == 1:
            warnings.warn('仅考虑继续分配的订单仍不能找到可行解。')
            prob_1, df_1 = solver(aunt, order, timestamp, n, False, high_quality_aunt_id)
            return prob_1, df_1
    else:
        return prob, df
