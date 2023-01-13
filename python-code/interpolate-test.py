# -*- coding: utf-8 -*-            
# @Time : 2023/1/13 19:19
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf  # 引入径向基函数

filename = r'0.txt'  # 数据文件地址，附件1
df = pd.read_csv(filename, sep="\t")  # 读取文件
df1 = df["1"]  # 读取第一列数据
df2 = df['2']  # 读取第二列数据
df3 = df['3']  # 读取第三列数据
odf1 = np.linspace(600, 1900, 50)  # 设置网格经度
odf2 = np.linspace(50, 450, 50)  # 设置网格纬度
odf1, odf2 = np.meshgrid(odf1, odf2)  # 网格化
func = Rbf(odf1, odf2, function='linear')  # 定义插值函数plt.cm.hot
odf3_new = func(odf1, odf2)  # 获得插值后的网格累计降水量
plt.contourf(odf1, odf2, odf3_new,
             levels=np.arange(odf3_new.min(), odf3_new.max(), (odf3_new.max() - odf3_new.min()) / 10), cmap='GnBu',
             extend='both')  # 画图
# 添加等高线
line = plt.contour(odf1, odf2, odf3_new,
                   levels=np.arange(odf3_new.min(), odf3_new.max(), (odf3_new.max() - odf3_new.min()) / 10))
plt.clabel(line, inline=True, fontsize=12)
plt.show()
