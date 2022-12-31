# -*- coding: utf-8 -*-            
# @Time : 2022/12/31 13:21
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import matplotlib.pyplot as plt

plt.xlim(0, 5)
plt.ylim(0, 5)
# 绘制3个坐标点
plt.plot((3, 3, 3), (1, 2, 3), 'o')
# 使用text函数设置文本
plt.text(3, 1, 'text')
# 使用annotate函数必备参数绘制注解
plt.annotate('sdhasd', xy=(2, 2))
# 使用annotate函数绘制注解，添加指示箭头
plt.annotate('annotate', xy=(3, 3), xytext=(4, 3),
             arrowprops=dict(arrowstyle='->', facecolor='black')
             )
plt.show()
