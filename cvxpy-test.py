# -*- coding: utf-8 -*-            
# @Time : 2022/12/24 12:14
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
# Import packages.
import cvxpy as cp
import numpy as np

# Generate data.
m = 20
n = 15
np.random.seed(1)
A = np.random.randn(m, n)
b = np.random.randn(m)

# Define and solve the CVXPY problem.
x = cp.Variable(n, integer=True)
cost = cp.sum_squares(A @ x - b)
prob = cp.Problem(cp.Minimize(cost))
prob.solve(solver=cp.CPLEX)

# Print result.
print("\nThe optimal value is", prob.value)
print("The optimal x is")
print(x.value)
# 残差的2范数
print("The norm of the residual is ", cp.norm(A @ x - b).value)
