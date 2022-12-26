# -*- coding: utf-8 -*-            
# @Time : 2022/12/24 18:43
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import cvxpy as cp
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix


def solve_prob(aunt, order):
    n1 = order.shape[0]
    n2 = aunt.shape[0]
    print(n1, n2)
    dist = distance_matrix(order.loc[:, ['x', 'y']],
                           aunt.loc[:, ['x', 'y']])
    # 1.定义变量
    x = cp.Variable((n1, n2), boolean=True)
    # 2.定义约束
    # A代表服务分,B代表通行距离,阿姨的服务间隔时间
    A = x @ aunt['serviceScore'].values
    B = cp.multiply(dist, x)
    C = n1 / 2

    alpha = cp.Parameter(nonneg=True, value=0.78)
    beta = cp.Parameter(nonneg=True, value=0.025)
    gamma = cp.Parameter(nonneg=True, value=0.195)
    obj = cp.sum(A) * alpha - beta * cp.sum(B) - C * gamma
    objective = cp.Maximize(obj)
    constrains = [cp.sum(x, axis=1) == 1,
                  cp.sum(x, axis=0) <= 1]
    # 3.求解问题
    prob = cp.Problem(objective, constrains)
    prob.solve(solver=cp.CPLEX, verbose=True)
    df = pd.DataFrame(x.value)
    return prob, df
