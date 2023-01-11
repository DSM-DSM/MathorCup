# -*- coding: utf-8 -*-            
# @Time : 2022/12/23 15:21
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import math
import warnings
import numpy as np
import pandas as pd
from order import Order
from aunt import Aunt
from solve import solver
import matplotlib.pyplot as plt
import matplotlib as mpl
from adjustText import adjust_text

warnings.filterwarnings('ignore')


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
        self.force_to_next_time = False
        self.use_high_quality = False
        self.pressing_order = 0
        self.enlarge_time_axis = 0
        self.future_aunt = 0
        self.solver_mode = {'mode': 'off-line', 'start_time_axis': self.enlarge_time_axis,
                            'future_aunt': self.future_aunt, 'pressing_order': self.pressing_order}

    def online_order_assign(self):
        if self.enlarge_time_axis != 0:
            self.aunt.data['avail_time'] = -self.enlarge_time_axis
            self.order.data['current_time'] = self.order.data['current_time'] - 3600 * self.enlarge_time_axis
            self.solver_mode['mode'] = 'on-line'
            self.solver_mode['start_time_axis'] = self.enlarge_time_axis
            self.solver_mode['future_aunt'] = self.future_aunt
            self.solver_mode['pressing_order'] = self.pressing_order

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
        self.online_order_assign()
        time_max = self.order.TimeRange
        time_min = 0 - self.enlarge_time_axis
        time_linspace = np.linspace(time_min, time_max, 2 * (time_max - time_min) + 1)
        obj = 0
        n = 0
        result22 = pd.DataFrame()
        obj_n_t_list = np.zeros(shape=(2 * (time_max - time_min) + 1, 4))
        print("***********当前求解状态:***********\n")
        print("是否线上派单:" + str(bool(self.pressing_order)) + ';是否考虑当前时间点未来的Aunt:' + str(
            bool(self.future_aunt)) + '\n')
        print('考虑' + str(self.pressing_order) + '小时后的Order  考虑' + str(self.future_aunt) + '小时后的Aunt\n')
        for time in time_linspace:
            self.order.updata_order_available(time, self.pressing_order)
            self.aunt.updata_aunt_assign_status(time)
            print(f"*************第{time}时刻*************")
            order_exist = self.order.get_order(time, self.solver_mode).shape[0]
            obj_t, order_assign = self.grid_iter_solve(time)
            obj += obj_t
            n += order_assign
            self.order.if_retainable(time)
            result22 = pd.concat([result22, self.order.data])
            obj_n_t_list[int(2 * (time + self.enlarge_time_axis)), :] = [obj_t, order_exist, order_assign, time]
        # 计算目标函数的均值
        obj_n_t_list[:, 0] = obj_n_t_list[:, 0] / obj_n_t_list[:, 2]
        obj_n_t_list[np.isnan(obj_n_t_list[:, 0]), 0] = 0
        return obj, n, result22, obj_n_t_list

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
        while order_remain > 1 and not self.force_to_next_time:
            print(f"**********第{iter_num}次网格迭代搜索**********")
            result1, n = self.grid_solve(solver=solver, timestamp=timestamp, iter_num=iter_num)
            obj_final += sum(result1)
            n_final += n
            iter_num += 1
            order_remain = self.order.get_order(timestamp, self.solver_mode).shape[0]
        if self.force_to_next_time:
            print('\n##########强制进入下一个时刻##########')
            print(self.order.get_order(timestamp, self.solver_mode).index)
            print(f'##########order_remain:{order_remain}##########\n')
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
        aunt = self.aunt.get_aunt(timestamp, self.solver_mode)
        order = self.order.get_order(timestamp, self.solver_mode)
        result1 = []
        result2 = pd.DataFrame(columns=['aunt_id', 'order_id'])
        n = 0
        for i in range(cur_gridshape[0]):
            for j in range(cur_gridshape[1]):
                # 从候选阿姨&订单中选出指定区域位置的阿姨&订单
                cur_aunt = self.get_grid(aunt, i, j)
                cur_order = self.get_grid(order, i, j)
                if cur_aunt.shape[0] > 0 and cur_order.shape[0] > 0:
                    # 排除订单和阿姨两者任一一者为空的情况
                    print('网格区域：(%d,%d)' % (i, j))
                    print('Order的个数：%d,Aunt的个数：%d' % (cur_order.shape[0], cur_aunt.shape[0]))
                    # prob是一个cvxpy对象，x是一个pandas对象，是解矩阵
                    if self.use_high_quality:
                        high_quality_aunt_id = self.choose_high_quality_aunt(cur_aunt, cur_order)
                        prob, x, assign_order_num = solver(cur_aunt, cur_order, timestamp, self.solver_mode,
                                                           high_quality_aunt_id)
                    else:
                        prob, x, assign_order_num = solver(cur_aunt, cur_order, timestamp, self.solver_mode)
                    # 因为solver的求解情况有多种（仅考虑紧急订单~考虑当前时间段所有订单），因此需要明确prob.value对应分批的订单的个数
                    if prob.value >= 1:
                        # 可能存在当前阿姨无法完全分配掉当前时间的紧急订单情况
                        result1.append(prob.value)
                    else:
                        result1.append(prob.value * assign_order_num)
                    n += assign_order_num
                    info = self.extract_info(x, cur_aunt, cur_order)
                    result2 = pd.concat([result2, info])
                elif self.cur_order_all_assign and cur_order.shape[0] > 0:
                    # 阿姨数量大于订单数量分支种订单全部被分配的条件下，存在订单数>0而阿姨数等于0的情况
                    self.cur_order_all_assign = False
        # 更新阿姨的状态
        self.aunt.updata_aunt_info(result2, timestamp)
        # 更新订单的状态
        self.order.update_order_assign_status(result2)
        # 在Assign中更新有关Aunt和Order交互信息的状态
        self.updata_aunt_order(result2, timestamp)
        return result1, n

    def enlarge_gridshape(self, iter_num):
        """
        网格扩大化求解中，更新网格参数的函数
        :param iter_num: 当前网格化求解的迭代次数
        :return:
        """
        # 方案1：
        # r = round(math.pow(self.gridshape[0], 1 / 2 * iter_num))
        # c = round(math.pow(self.gridshape[1], 1 / 2 * iter_num))
        # 方案2：
        # r = round(self.gridshape[0] / (iter_num))
        # c = round(self.gridshape[1] / (iter_num))
        if iter_num == 0:
            return self.gridshape
        else:
            if self.all_to_program:
                size = (1, 1)
                return size
            else:
                r = self.gridshape[0] - 1 * iter_num
                c = self.gridshape[1] - 1 * iter_num
                if r == 0:
                    size = (1, c)
                    return size
                if c == 0:
                    size = (r, 1)
                else:
                    size = (r, c)
                return size

    def updata_aunt_order(self, indexer, timestamp):
        for index in range(len(indexer)):
            # aunt&order_id是派单双方的id。因为在初始化Aunt和Order类时，设置了以id为index,loc方法是以index索引的
            order_id = indexer.iloc[index, :].order_id
            aunt_id = indexer.iloc[index, :].aunt_id
            p1 = (self.aunt.data.loc[aunt_id, 'x'], self.aunt.data.loc[aunt_id, 'y'])
            p2 = (self.order.data.loc[order_id, 'x'], self.order.data.loc[order_id, 'y'])
            dist = math.dist(p1, p2)
            self.aunt.data.loc[aunt_id, 'avail_time'] += self.calculate_time(dist) + self.order.data.loc[
                order_id, 'serviceUnitTime']
            self.order.data.loc[order_id, 'serviceStartTime'] = 1662768000 + 3600 * (
                    timestamp + self.calculate_time(dist))
            # self.order.data.loc[order_id, 'serviceStartTime'] = timestamp + self.calculate_time(dist)
            self.order.data.loc[order_id, 'aunt_id'] = aunt_id
            self.aunt.data.loc[aunt_id, 'x'] = self.order.data.loc[order_id, 'x']
            self.aunt.data.loc[aunt_id, 'y'] = self.order.data.loc[order_id, 'y']

    def calculate_time(self, dist):
        k = math.floor(dist / self.aunt.velocity / 2)
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

    def extract_info(self, x, cur_aunt, cur_order):
        aunt_id = np.where(x == 1)[1]
        order_id = np.where(x == 1)[0]
        df = pd.DataFrame(columns=['aunt_id', 'order_id'])
        aunt = []
        order = []
        for i in range(len(aunt_id)):
            a = cur_aunt.iloc[aunt_id[i], :].name
            o = cur_order.iloc[order_id[i], :].name
            aunt.append(a)
            order.append(o)
        df['aunt_id'] = aunt
        df['order_id'] = order
        return df

    def plot_order_aunt_route(self):
        # 防止plt汉字乱码
        mpl.rcParams['font.sans-serif'] = ['simhei']
        mpl.rcParams['axes.unicode_minus'] = False
        plt.rcParams['savefig.dpi'] = 300
        plt.rcParams['figure.dpi'] = 300

        plt.figure(figsize=(24, 8))
        texts = []
        # 绘制Order信息
        for i in range(self.order.n):
            x = self.order.data.iloc[i, :].x_od
            y = self.order.data.iloc[i, :].y_od
            firstime = self.order.data.iloc[i, :].serviceFirstTime
            lastime = self.order.data.iloc[i, :].serviceLastTime + firstime
            order_id = self.order.data.iloc[i, :].name
            plt.scatter(x, y, s=400, c='red', marker='*', alpha=0.9)
            text_info = f'Order{order_id}' + '[' + str(firstime) + ',' + str(lastime) + ']'
            texts.append(plt.text(x, y, text_info))

        # 绘制Aunt信息
        c_list = ['b', 'c', 'g', 'k', 'm', 'r', 'y', '#F0E68C', '#00FF7F', '#F5DEB3',
                  'b', 'c', 'g', 'k', 'm', 'r', 'y', '#F0E68C', '#00FF7F', '#F5DEB3']
        for j in range(self.aunt.n):
            aunt_x_od = self.aunt.data.iloc[j, :].x_od
            aunt_y_od = self.aunt.data.iloc[j, :].y_od
            aunt_id = self.aunt.data.iloc[j, :].name
            aunt_get_order_list = self.aunt.data.iloc[j, :].order
            get_order_num = len(self.aunt.data.iloc[j, :].order)
            order_list = self.aunt.data.iloc[j, :].order
            for k in range(get_order_num):
                if k == 0:
                    plt.scatter(aunt_x_od, aunt_y_od, s=200, c=c_list[j], marker='v')
                    texts.append(plt.text(aunt_x_od, aunt_y_od, f'Aunt{aunt_id}' + str(aunt_get_order_list)))
                order_id = order_list[k]
                x, y, time_info = self.get_aunt_history_info(order_id)
                plt.scatter(x, y, s=40, c='green', marker='^')
                texts.append(plt.text(x, y, time_info))
                plt.plot([aunt_x_od, x], [aunt_y_od, y], color=c_list[j], linestyle=':', linewidth=1)
                aunt_x_od = x
                aunt_y_od = y
        adjust_text(texts, only_move={'text': 'y'})
        plt.title('Aunt-Order路线图')
        plt.xlim(self.x_min, self.x_max)
        plt.ylim(self.y_min, self.y_max)
        plt.savefig(f'../../pic/Aunt-Order路线图{self.gridshape}.png')
        plt.show()

    def get_aunt_history_info(self, order_id):
        cur_x = self.order.data.loc[order_id, 'x_od']
        cur_y = self.order.data.loc[order_id, 'y_od']
        serviceStartTime = 'arrive:' + str(self.order.data.loc[order_id, 'serviceStartTime'])
        return cur_x, cur_y, serviceStartTime
