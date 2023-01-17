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


def generate_constrain_matrix(aunt, order, timestamp, solver_mode):
    n_order = order.shape[0]
    n_aunt = aunt.shape[0]
    dist = distance_matrix(order.loc[:, ['x', 'y']],
                           aunt.loc[:, ['x', 'y']])
    constrain_matrix = np.zeros((n_order, n_aunt), dtype=int)
    for i in range(n_order):
        lastime = order.iloc[i, :].serviceLastTime
        firstime = order.iloc[i, :].serviceFirstTime
        for j in range(n_aunt):
            first = aunt.iloc[j, :]['first']
            avail_time = aunt.iloc[j, :]['avail_time']
            if first == 1:
                if solver_mode['mode'] == 'off-line':
                    constrain_matrix[i, j] = 1
                else:
                    if dist[i, j] > (lastime + firstime + solver_mode['start_time_axis'] - timestamp) * 15:
                        constrain_matrix[i, j] = 0
                    else:
                        constrain_matrix[i, j] = 1
            else:
                if lastime + firstime - avail_time <= 0:
                    constrain_matrix[i, j] = 0
                else:
                    if dist[i, j] > (lastime + firstime - avail_time) * 15:
                        constrain_matrix[i, j] = 0
                    else:
                        constrain_matrix[i, j] = 1
    return constrain_matrix


def generate_travel_time_matrix(aunt, order, dist):
    """

    :param order:
    :param aunt:
    :param dist:
    :return: Aunt对应于每一个Order的服务间隔时间矩阵
    """
    first_order = aunt['first'].to_numpy()
    avail_time = aunt['avail_time'].to_numpy()
    firstime = order['serviceFirstTime'].to_numpy()
    time_travel_matrix = np.floor(dist / 7.5) * 0.5 + 0.5
    for i in range(dist.shape[0]):
        for j in range(dist.shape[1]):
            if first_order[j] == 1:
                time_travel_matrix[i, j] = 0.5
            elif avail_time[j] + time_travel_matrix[i, j] <= firstime[i]:
                time_travel_matrix[i, j] = firstime[i] - avail_time[j]
    return time_travel_matrix


def get_a_b_c(aunt, order, x, dist):
    """

    :param order:
    :param aunt:
    :param x:
    :param dist:
    :return:A代表服务分,B代表通行距离,C代表阿姨的服务间隔时间
    """
    A = cp.sum(x @ aunt['serviceScore'].values)
    B = cp.sum(cp.multiply(dist, x))
    travel_time_matrix = generate_travel_time_matrix(aunt, order, dist)
    C = cp.sum(cp.multiply(x, travel_time_matrix))
    return A, B, C


def get_urgent_order(order, timestamp, n, solver_mode):
    urgent = (order.serviceLastTime + order.serviceFirstTime - timestamp)
    urgent_rank = urgent.rank(method='dense')
    if solver_mode['mode'] == 'on-line':
        urgent_rank[urgent <= 2] = 1
        urgent_rank = urgent_rank.rank(method='dense')
    urgent_order_index = urgent_rank[urgent_rank <= n].index
    return urgent_order_index, urgent_rank


def solver(aunt, order, timestamp, solver_mode, n, status, *args):
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
    A, B, C = get_a_b_c(aunt, order, x, dist)

    # 2.定义约束
    if_high_quality = np.zeros((n_aunt,), dtype=int)
    urgent_order, rank = get_urgent_order(order, timestamp, n, solver_mode)
    # 2.1设置优质阿姨
    for i in range(n_aunt):
        if aunt.iloc[i, :].name in high_quality_aunt_id:
            if_high_quality[i] = 1
    # 2.2限制阿姨不能接自己无法及时到达的订单
    constrain_matrix = generate_constrain_matrix(aunt, order, timestamp, solver_mode)
    # axis = 1 / 0 <==> 按行/列求和
    constrains = [cp.sum(x, axis=0) <= if_high_quality,
                  x <= constrain_matrix,
                  cp.sum(x, axis=0) <= 1]
    # 2.3根据求解状态，逐步扩大紧急订单的范围，在所有可行解中寻找目标函数最大的一个作为当前派单方案的解
    if status:
        # 能够满足最基本的紧急订单全部分配时的约束和目标函数
        obj = (A * alpha - beta * B - gamma * C) / len(urgent_order)
        for i in range(n_order):
            if np.sum(constrain_matrix, axis=1)[i] >= 1 and order.iloc[i, :].name in urgent_order:
                constrains += [cp.sum(x, axis=1)[i] == 1]
            else:
                constrains += [cp.sum(x, axis=1)[i] == 0]
    else:
        # 当前时间最基本的紧急订单都不能满足的约束和目标函数
        obj = (A * alpha - beta * B - gamma * C)
        for i in range(n_order):
            if np.sum(constrain_matrix, axis=1)[i] >= 1 and order.iloc[i, :].name in urgent_order:
                constrains += [cp.sum(x, axis=1)[i] <= 1]
            else:
                constrains += [cp.sum(x, axis=1)[i] == 0]

    # 3.求解问题
    objective = cp.Maximize(obj)
    prob = cp.Problem(objective, constrains)
    prob.solve(solver=cp.GLPK_MI, qcp=True)
    df = pd.DataFrame(x.value)
    print(prob.value)
    # 4.递归求解，直至找到当前时间段，当前网格中最优的目标函数值
    if status:
        if prob.status == 'optimal' and n >= 1:
            if n > max(rank):
                return None, 0, 0
            n += 1
            prob_1, df_1, m_1 = solver(aunt, order, timestamp, solver_mode, n, True, high_quality_aunt_id)
            if prob_1 == None:
                return prob, df, np.sum(x.value)
            else:
                if prob_1.value > prob.value:
                    return prob_1, df_1, m_1
                else:
                    return prob, df, np.sum(x.value)
        if prob.status == 'infeasible' and n > 1:
            return None, 0, 0
        if prob.status == 'infeasible' and n == 1:
            warnings.warn('仅考虑当前时间段必须被分配的订单却仍不能找到可行解！！！')
            prob_1, df_1, m_1 = solver(aunt, order, timestamp, solver_mode, n, False, high_quality_aunt_id)
            return prob_1, df_1, m_1
    else:
        return prob, df, np.sum(x.value)
