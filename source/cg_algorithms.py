#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math

def Round(f):
    return int(f + 0.5)
def fraction(n):
    if n <= 1:
        return 1
    else:
        return n * fraction(n - 1)
def Combinational(n:int, m:int):
    ret = 1
    for i in range(m):
        ret *= (n - i)
    ret /= fraction(m)
    return ret

def draw_line(p_list, algorithm):               ##
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]                          # Float in p_list
    x1, y1 = p_list[1]
    if algorithm == 'Naive':
        result = [(Round(x0), Round(y0)), (Round(x1), Round(y1))]
        if x1 == x0 and y1 == y0:
            return result
        if abs(x1 - x0) >= abs(y1 - y0):
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1- y0) / (x1 - x0)                # x1 - x0 won't be 0
            for x in range(int(x0), int(x1 + 1)):
                y = y0 + k * (x - x0)
                result.append((Round(x), Round(y)))
        else:
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (x1 - x0) / (y1 - y0)
            for y in range(int(y0), int(y1 + 1)):
                x = x0 + k * (y - y0)
                result.append((Round(x), Round(y)))
        return result
    elif algorithm == 'DDA':
        result = []
        dx = Round(x1 - x0)
        dy = Round(y1 - y0)
        if abs(dy) > abs(dx):
            epsilon = abs(dy)
        else:
            epsilon = abs(dx)
        if epsilon != 0:
            xinc = dx / epsilon             # 1 or dx / dy
            yinc = dy / epsilon
        else:
            xinc = 0
            yinc = 0
        x = x0
        y = y0
        for i in range(epsilon + 1):
            result.append((Round(x), Round(y)))
            x += xinc
            y += yinc
        return result
        pass
    elif algorithm == 'Bresenham':
        swap_x = False
        swap_y = False
        swap_xy = False
        if x0 == x1 or y0 == y1:
            return draw_line(p_list, 'Naive')
        if abs(y0 - y1) > abs(x0 - x1):
            x0, y0, x1, y1 = y0, x0, y1, x1
            swap_xy = True
        if y0 > y1:
            y0, y1 = y1, y0
            swap_y = True
        if x0 > x1:
            x0, x1 = x1, x0
            swap_x = True

        result = []
        dx = Round(x1 - x0)
        dy = Round(y1 - y0)
        d = dy - (dx - dy)
        x = Round(x0)
        y = Round(y0)
        while x <= x1:
            if d < 0:
                d += 2 * dy
            else:
                y = y + 1
                d += (dy - dx) * 2
            result_x = x
            result_y = y
            if swap_x:
                result_x = (x0 + x1) - result_x
            if swap_y:
                result_y = (y0 + y1) - result_y
            if swap_xy:
                result_x, result_y = result_y, result_x
            result.append((result_x, result_y))
            x = x + 1
        return result

        
        pass
    return result


def draw_polygon(p_list, algorithm):            ##
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(1, len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    #if len(p_list) > 2:
    #result += draw_line([p_list[-1], p_list[0]], algorithm)
    return result


def draw_ellipse(p_list):                       #
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    if x0 == x1 or y0 == y1:
        return draw_line(p_list, 'Naive')
    a = abs(x1 - x0) / 2
    b = abs(y1 - y0) / 2
    x2 = abs(x1 + x0) / 2
    y2 = abs(y1 + y0) / 2
    x = 0
    y = b
    while x <= a and abs(b * b * x) <= abs(a * a * y):
        result.append((Round(x2 + x), Round(y2 + y)))
        result.append((Round(x2 + x), Round(y2 - y)))
        result.append((Round(x2 - x), Round(y2 + y)))
        result.append((Round(x2 - x), Round(y2 - y)))
        x = x + 1
        y = math.sqrt(abs(b * b * (1 - x * x / a / a)))
    x = a
    y = 0
    while y <= b and abs(b * b * x) >= abs(a * a * y):
        result.append((Round(x2 + x), Round(y2 + y)))
        result.append((Round(x2 + x), Round(y2 - y)))
        result.append((Round(x2 - x), Round(y2 + y)))
        result.append((Round(x2 - x), Round(y2 - y)))
        y = y + 1
        x = math.sqrt(abs(a * a * (1 - y * y / b / b)))
 
    return result


def draw_curve(p_list, algorithm):              ##
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    print(p_list, end = '')
    result = []
    if algorithm == 'Naive':        # 
        return draw_polygon(p_list, 'Naive')
    if algorithm == "Bezier":
        print("Bezier Curve")
        N = 2000
        for i in range(1, N):
            t = i / N
            x_i = 0
            y_i = 0
            e = len(p_list) 
            for j in range(e):
                x_i += p_list[j][0] * pow(t, j) * pow(1 - t, e - 1 - j) * Combinational(e - 1, j)
                y_i += p_list[j][1] * pow(t, j) * pow(1 - t, e - 1 - j) * Combinational(e - 1, j)
            result.append((Round(x_i), Round(y_i)))
    elif algorithm == "B-spline":
        pass
    else:
        pass
    return result

def translate(p_list, dx, dy):                  #
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    for p in p_list:
        p[0] += dx
        p[1] += dy
    pass


def rotate(p_list, x, y, r):                    #
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    #print("Rotate at", x, y, "| degree =", r)
    r = math.radians(r)
    m = [[math.cos(r), -math.sin(r)], [math.sin(r), math.cos(r)]]
    for p in p_list:
        p[:] = [p[0] - x, p[1] - y]
        p[:] = [p[0] * m[0][0] + p[1] * m[0][1], p[0] * m[1][0] + p[1] * m[1][1]]
        p[:] = [p[0] + x, p[1] + y]
    pass


def scale(p_list, x, y, s):                     #
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    for p in p_list:
        p[0] = (p[0] - x) * s + x
        p[1] = (p[1] - y) * s + y
    pass

                                                
def clip(p_list, x_min, y_min, x_max, y_max, algorithm):    ##
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    pass
