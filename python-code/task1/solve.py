# -*- coding: utf-8 -*-            
# @Time : 2022/12/24 18:43
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import cvxpy as cp
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix


def solver(aunt, order, timestamp):
    n_order = order.shape[0]
    n_aunt = aunt.shape[0]
    dist = distance_matrix(order.loc[:, ['x', 'y']],
                           aunt.loc[:, ['x', 'y']])
    # 1.定义变量
    x = cp.Variable((n_order, n_aunt), boolean=True)
    # 2.定义约束
    # A代表服务分,B代表通行距离,C代表阿姨的服务间隔时间
    A = x @ aunt['serviceScore'].values
    B = cp.multiply(dist, x)
    time_step = aunt['first'].to_numpy()
    for i in range(n_aunt):
        if time_step[i] == 1:
            # 第i个阿姨是第一次分配到订单
            time_step[i] = 0.5
        else:
            time_step[i] = timestamp - aunt.loc[i, 'when_get_order'][-1]
    C = cp.sum(x, axis=0) @ time_step
    alpha = cp.Parameter(nonneg=True, value=0.78)
    beta = cp.Parameter(nonneg=True, value=0.025)
    gamma = cp.Parameter(nonneg=True, value=0.195)
    obj = (cp.sum(A) * alpha - beta * cp.sum(B) - C * gamma) / n_order
    objective = cp.Maximize(obj)
    constrains = [cp.sum(x, axis=1) == 1,
                  cp.sum(x, axis=0) <= 1]
    # 3.求解问题
    prob = cp.Problem(objective, constrains)
    prob.solve(solver=cp.CPLEX)
    df = pd.DataFrame(x.value)
    return prob, df
