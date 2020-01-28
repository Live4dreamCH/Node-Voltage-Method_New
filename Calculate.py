# -*- coding: utf-8 -*-
import numpy as np


def cal(node: int, elements: list):
    """
    此函数：将输入形成的列表elements转化为系数矩阵，并求解。

    node：输入的结点数目。

    elements：储存电路元件信息的列表，如：[['电导', 10.0, 1.0, 2.0], ['VCCS', 2.2, 3.0, 5.0, 7.0, 9.0]]
    """
    rank = node  # 系数矩阵的秩，即未知量个数、方程数
    for ele in elements:
        if ele[0][0] in ('VCVS', '电压源', 'CCCS'):  # 部分元件需要增设变量、增加方程
            rank += 1
        elif ele[0][0] == 'CCVS':
            rank += 2
        ele[1] = (int(ele[1][0]), int(ele[1][1]), int(ele[1][2]))  # 下标只能为整数或者切片，不能为浮点数
        if ele[0] in ('CCCS', 'VCCS', 'VCVS', 'CCVS'):
            ele[2] = (int(ele[2][0]), int(ele[2][1]), int(ele[2][2]))  # 下标只能为整数或者切片，不能为浮点数
    A = np.zeros((rank, rank))
    B = np.zeros((rank, 1))

    add = node
    for element in elements:  # 分类别逐个填入元件
        ty = element[0][0]
        vl = element[0][1]
        fr = element[1][0]
        to = element[1][2]
        # ['请选择元件', '电阻', '电导', '电流源', '电压源', 'CCCS', 'VCCS', 'VCVS', 'CCVS', "电容", "电感"]
        if ty == '电导':
            A[fr][fr] += vl
            A[to][to] += vl
            A[fr][to] -= vl
            A[to][fr] -= vl
        elif ty == '电阻':
            try:
                G = 1 / vl
            except ZeroDivisionError:  # 若电阻为零，处理1/0异常
                G = 1e10
            A[fr][fr] += G
            A[to][to] += G
            A[fr][to] -= G
            A[to][fr] -= G
        elif ty == '电流源':
            B[fr] -= vl
            B[to] += vl
        elif ty == '电压源':
            A[fr][add] += 1
            A[to][add] -= 1
            A[add][fr] += 1
            A[add][to] -= 1
            B[add][0] += vl
            add += 1
        else:
            cl_fr = element[2][0]
            cl_lb = element[2][1]
            cl_to = element[2][2]
            if ty == 'VCCS':
                A[fr][cl_fr] += vl
                A[fr][cl_to] -= vl
                A[to][cl_fr] -= vl
                A[to][cl_to] += vl
            elif ty == 'VCVS':
                A[fr][add] += 1
                A[to][add] -= 1
                A[add][fr] += 1
                A[add][to] -= 1
                A[add][cl_fr] -= vl
                A[add][cl_to] += vl
                add += 1
            elif ty == 'CCCS':  # 存疑：为何可以增加变量而不增加方程？ 已明白，等待改写。 另外一个问题：若电路的图非简单图，那控制电流到底是哪条支路上的？
                A[fr][add] += vl
                A[to][add] -= vl

                add += 1
            elif ty == 'CCVS':  # 也有问题：它默认控制电流为0V电压源的了
                A[fr][add] += 1
                A[to][add] -= 1
                A[add][fr] += 1
                A[add][to] -= 1
                A[add][add + 1] -= vl
                add += 2
    AA = A[1:][..., 1:]
    BB = B[1:]
    X = np.linalg.solve(AA, BB)
    print(X)
    return X


if __name__ == '__main__':
    # 下标只能为整数或者切片，不能为浮点数
    # 电压源、电压控制电压源VCVS、电流控制电压源CCVS需要增加变量和方程数（列数和行数）
    # 电流控制电流源CCCS需要增加变量，但是不需要增加方程数
    cal(10, [])
    a = [[10000000000, -10000000000], [1, 0]]
    b = [[10], [3]]
    A = np.array(a)
    B = np.array(b)
    X = np.linalg.solve(A, B)
    print('X=', X, sep='\n')
