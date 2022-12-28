# -*- coding: utf-8 -*-            
# @Time : 2022/12/23 15:21
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import math
import numpy as np
from order import Order
from aunt import Aunt
from solve import solver
from scipy.spatial import distance_matrix


class Assign(Aunt, Order):
    def __init__(self, aunt, order, gridshape):
        """

        :param data: 读入的原始数据
        :param n: 数据的行数
        """
        self.aunt = aunt
        self.order = order
        self.n_aunt = aunt.data.shape[0]
        self.n_order = order.data.shape[0]
        self.gridshape = gridshape
        self.cur_order_all_assign = False
        self.get_grid_info()
        self.grid_iter(self.gridshape)
        self.all_to_program = False
        self.var_limit = 1000
        self.force_to_next_time = False
        self.use_high_quality = False

    def get_grid_info(self):
        try:
            self.x_max = max(self.aunt.data['x_od'].max(), self.order.data['x_od'].max())
            self.x_min = min(self.aunt.data['x_od'].min(), self.order.data['x_od'].min())
            self.y_max = max(self.aunt.data['y_od'].max(), self.order.data['y_od'].max())
            self.y_min = min(self.aunt.data['y_od'].min(), self.order.data['y_od'].min())
        except TypeError:
            raise 'data中不存在列x_od或y_od'

    def grid(self, data_to_grid, gridshape, n_row):
        """
        将数据点按照网格划分
        :param n_row:
        :param data_to_grid:
        :param gridshape: 元组表示几行几列
        :return:
        """
        eps = 10
        x_range = np.linspace(self.x_min, self.x_max, gridshape[0] + 1)
        y_range = np.linspace(self.y_min, self.y_max, gridshape[1] + 1)
        x_range[0], x_range[-1] = x_range[0] - eps, x_range[-1] + eps
        y_range[0], y_range[-1] = y_range[0] - eps, y_range[-1] + eps
        dis_x, dis_y = [], []
        for i in range(n_row):
            for j in range(gridshape[0]):
                if x_range[j] <= data_to_grid['x_od'].iloc[i] < x_range[j + 1]:
                    dis_x.append(j)
            for k in range(gridshape[1]):
                if y_range[k] <= data_to_grid['y_od'].iloc[i] < y_range[k + 1]:
                    dis_y.append(k)
        data_to_grid['district_x'] = dis_x
        data_to_grid['district_y'] = dis_y

    def grid_iter(self, gridshape):
        self.grid(self.order.data, gridshape, self.n_order)
        self.grid(self.aunt.data, gridshape, self.n_aunt)

    def get_grid(self, obj, region_x, region_y):
        """
        获得指定区域坐标数据的函数
        :param obj:
        :param region_x:
        :param region_y:
        :return:
        """
        id_x = obj['district_x'] == region_x
        id_y = obj['district_y'] == region_y
        id = id_x & id_y
        return obj[id]

    def time_solve(self):
        time_linspace = np.linspace(0, 13, 27)
        obj = 0
        n = 0
        for time in time_linspace:
            self.order.updata_order_available(time)
            self.aunt.updata_aunt_assign_status(time)
            print(f"*************第{time}时刻*************")
            obj_t, n_t = self.grid_iter_solve(time)
            obj += obj_t
            n += n_t
        return obj, n

    def grid_iter_solve(self, timestamp):
        """
        网格化循环求解的函数
        :param timestamp: 当前时间戳
        :return: obj_final列表，n_final整数
        """
        obj_final = 0
        n_final = 0
        iter_num = 0
        order_remain = np.inf
        # for iter_num in range(self.max_grid_iter):
        #     result1, n = self.grid_solve(solver=solver, timestamp=timestamp, iter_num=iter_num)
        #     obj_final += sum(result1)
        #     n_final += n
        #     if self.cur_order_all_assign:
        #         self.cur_order_all_assign = False
        #         self.all_to_program = False
        #         break
        while order_remain >= 5 and self.force_to_next_time == False:
            print(f"**********第{iter_num}次网格迭代搜索**********")
            result1, n = self.grid_solve(solver=solver, timestamp=timestamp, iter_num=iter_num)
            obj_final += sum(result1)
            n_final += n
            iter_num += 1
            order_remain = self.order.get_order(timestamp).shape[0]
        if self.force_to_next_time:
            print('**********强制进入下一个时刻**********')
        self.cur_order_all_assign = False
        self.all_to_program = False
        self.force_to_next_time = False
        return obj_final, n_final

    def grid_solve(self, solver, timestamp, iter_num):
        """
        网格化求解的基函数
        :param solver: 指定的求解器
        :param timestamp: 当前时间戳
        :param iter_num: 当前网格化求解的迭代次数
        :return:result1是一个列表,内部包含了求解器的目标函数值*订单个数;n是一个数字,代表此次求解的总订单数
        因此sum(result1)/n 即为此次求解的最终目标函数值
        """
        cur_gridshape = self.enlarge_gridshape(iter_num)
        if cur_gridshape == self.enlarge_gridshape(iter_num - 1):
            self.force_to_next_time = True
            return [], 0
        self.grid_iter(cur_gridshape)
        print('********当前gridsize:(%d, %d)********' % (cur_gridshape[0], cur_gridshape[1]))
        # 根据时间和阿姨&订单状态选出候选阿姨
        aunt = self.aunt.get_aunt(timestamp)
        order = self.order.get_order(timestamp)
        # 判断此时是否可以考虑将全部阿姨订单同时加入规划
        self.check_all_to_program(aunt, order)
        result1, result2 = [], []
        assign_order = []
        n = 0
        for i in range(cur_gridshape[0]):
            for j in range(cur_gridshape[1]):
                # 从候选阿姨&订单中选出指定区域位置的阿姨&订单
                cur_aunt = self.get_grid(aunt, i, j)
                cur_order = self.get_grid(order, i, j)
                if cur_aunt.shape[0] > 0 and cur_order.shape[0] > 0:
                    # 排除订单和阿姨两者任一一者为空的情况
                    if cur_aunt.shape[0] >= cur_order.shape[0]:
                        # 阿姨数量大于订单数量，则所有订单都能被分配
                        print('位置坐标(%d,%d)' % (i, j))
                        print('Order的个数：%d,Aunt的个数：%d' % (cur_order.shape[0], cur_aunt.shape[0]))
                        # prob是一个cvxpy对象，x是一个pandas对象，是解矩阵
                        if self.use_high_quality:
                            high_quality_aunt_id = self.choose_high_quality_aunt(cur_aunt, cur_order)
                            prob, x = solver(cur_aunt, cur_order, timestamp, high_quality_aunt_id)
                        else:
                            prob, x = solver(cur_aunt, cur_order, timestamp)
                        assign_order.append(cur_order.id.values)
                        result1.append(prob.value * cur_order.shape[0])
                        result2.append(self.aunt.extract_info_x(x, cur_aunt, cur_order))
                        n += cur_order.shape[0]
                    elif self.cur_order_all_assign:
                        # 阿姨数小于订单数，存在订单不饿能被分配
                        self.cur_order_all_assign = False
                elif self.cur_order_all_assign and cur_order.shape[0] > 0:
                    # 阿姨数量大于订单数量分支种订单全部被分配的条件下，存在订单数>0而阿姨数等于0的情况
                    self.cur_order_all_assign = False
        # 更新订单的状态
        self.order.update_order_assign_status(assign_order)
        # 更新阿姨的状态
        aunt_order_indexer = self.aunt.updata_aunt_info(result2, timestamp)
        self.updata_aunt_xy(aunt_order_indexer)
        return result1, n

    def check_all_to_program(self, cur_aunt, cur_order):
        """
        判断所给定数据是否能够一次性加入求解器
        :param cur_aunt:
        :param cur_order:
        :return:
        """
        var_num = cur_aunt.shape[0] * cur_order.shape[0]
        if self.var_limit > var_num:
            self.all_to_program = True

    def enlarge_gridshape(self, iter_num):
        """
        网格扩大化求解中，更新网格参数的函数
        :param iter_num:
        :return:
        """
        if iter_num == 0:
            return self.gridshape
        else:
            if self.all_to_program:
                size = (1, 1)
                return size
            else:
                # r = round(math.pow(self.gridshape[0], 1 / 2 * iter_num))
                # c = round(math.pow(self.gridshape[1], 1 / 2 * iter_num))
                # r = round(self.gridshape[0] / (iter_num))
                # c = round(self.gridshape[1] / (iter_num))
                r = self.gridshape[0] - 1 * iter_num
                c = self.gridshape[1] - 1 * iter_num
                if r == 0 or c == 0:
                    r = self.gridshape[0] - 1 * (iter_num - 1)
                    c = self.gridshape[1] - 1 * (iter_num - 1)
                    size = (r, c)
                    return size
                size = (r, c)
                return size

    def updata_aunt_xy(self, indexer):
        for index in range(len(indexer)):
            order_id = indexer.iloc[index, 1]
            aunt_id = indexer.iloc[index, 0]
            p1 = (self.aunt.data.loc[aunt_id, 'x'], self.aunt.data.loc[aunt_id, 'y'])
            p2 = (self.order.data.loc[order_id, 'x'], self.order.data.loc[order_id, 'y'])
            dist = math.dist(p1, p2)
            self.aunt.data.loc[aunt_id, 'avail_time'] = self.calculate_time(dist) + self.order.data.loc[
                index, 'serviceUnitTime']
            self.aunt.data.loc[aunt_id, 'x'] = self.order.data.loc[order_id, 'x']
            self.aunt.data.loc[aunt_id, 'y'] = self.order.data.loc[order_id, 'y']

    def calculate_time(self, dist):
        t = dist / self.aunt.velocity
        k = t // 0.5
        if k * 0.5 == t:
            return t
        else:
            return (k + 1) * 0.5

    def choose_high_quality_aunt(self, aunt, order):
        if self.assign_has_huge_diff(aunt, order):
            num = int(order.shape[0] * 1.5)
            high_quality_aunt = aunt.sort_values(by='serviceScore', ascending=False)[:num]
            return high_quality_aunt.id
        return aunt.id

    def assign_has_huge_diff(self, aunt, order):
        if aunt.shape[0] > 4 * order.shape[0]:
            return True
        return False
