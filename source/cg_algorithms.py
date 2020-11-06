#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math

def Round(x):
    return int(x + 0.5)

def fraction(n):
    result = 1
    for i in range(n):
        result *= (i + 1)
    return result
    
def Combinational(n:int, m:int):
    ret = 1
    for i in range(m):
        ret *= (n - i)
    ret /= fraction(m)
    return ret

def draw_line(p_list, algorithm):               #
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]                          # Float in p_list
    x1, y1 = p_list[1]
    if algorithm == 'Naive':
        result = [[Round(x0), Round(y0)], [Round(x1), Round(y1)]]
        if x1 == x0 and y1 == y0:
            return result
        if abs(x1 - x0) >= abs(y1 - y0):
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1- y0) / (x1 - x0)                # x1 - x0 won't be 0
            for x in range(Round(x0), Round(x1 + 1)):
                y = y0 + k * (x - x0)
                result.append([Round(x), Round(y)])
        else:
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (x1 - x0) / (y1 - y0)
            for y in range(Round(y0), Round(y1 + 1)):
                x = x0 + k * (y - y0)
                result.append([Round(x), Round(y)])
        return result
    elif algorithm == 'DDA':
        result = []
        dx = x1 - x0
        dy = y1 - y0
        r = Round(max(abs(dx), abs(dy)))
        if r != 0:
            xinc = dx / r
            yinc = dy / r
        else:
            xinc = 0
            yinc = 0
        x = x0
        y = y0
        for i in range(r + 1):
            result.append([Round(x), Round(y)])
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
        x = Round(x0)
        y = Round(y0)
        d = dy - (dx - dy)
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
            result.append([result_x, result_y])
            x = x + 1
        return result

        
        pass
    return result

def draw_polygon(p_list, algorithm):            #
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
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    if x0 == x1 or y0 == y1:
        return draw_line(p_list, 'Naive')
    a = abs(x1 - x0) / 2
    b = abs(y1 - y0) / 2
    x2 = abs(x1 + x0) / 2
    y2 = abs(y1 + y0) / 2
    result = [[Round(x2), Round(y2 + b)], [Round(x2), Round(y2 - b)]]

    p = b * b + a * a * (1 / 4 - b)
    x = 0
    y = b
    while x <= a and abs(b * b * x) <= abs(a * a * y):
        if p < 0:
            p += b * b * (2 * x + 3) 
        else:
            y = y - 1
            p += b * b * (2 * x + 3) - 2 * a * a * y
        x = x + 1
        result.append([Round(x2 + x), Round(y2 + y)])
        result.append([Round(x2 + x), Round(y2 - y)])
        result.append([Round(x2 - x), Round(y2 + y)])
        result.append([Round(x2 - x), Round(y2 - y)])
    p = b * b * (x + 1 / 2) * (x + 1 / 2) + a * a * (y - 1) * (y - 1) - a * a * b * b
    while y >= 0:
        if p < 0:
            x = x + 1
            p += b * b * (2 * x) - a * a * (2 * y - 3)
        else:
            p += (-a * a * (2 * y - 3))
        y = y - 1
        result.append([Round(x2 + x), Round(y2 + y)])
        result.append([Round(x2 + x), Round(y2 - y)])
        result.append([Round(x2 - x), Round(y2 + y)])
        result.append([Round(x2 - x), Round(y2 - y)])
    return result

def get_Bezier_Point(t: float, p_list):                 # should only used in draw_curve
    n = len(p_list)
    x = 0.0
    y = 0.0
    for i in range(n):
        x += p_list[i][0] * pow(t, i) * pow(1 - t, n - 1 - i) * Combinational(n - 1, i)   
        y += p_list[i][1] * pow(t, i) * pow(1 - t, n - 1 - i) * Combinational(n - 1, i)
    return [Round(x), Round(y)]

def draw_Bezier(t1: float, t2: float, P1, P2, p_list):  # should only used in draw_curve
    if math.hypot(P1[0] - P2[0], P1[1] - P2[1]) < 2:    # To make curve continuous
        return []
    else:
        result = []
        Pm = get_Bezier_Point((t1 + t2) / 2.0, p_list)
        result.append(Pm)
        result += draw_Bezier(t1, (t1 + t2) / 2.0, P1, Pm, p_list)
        result += draw_Bezier((t1 + t2) / 2.0, t2, Pm, P2, p_list)
        return result

def draw_curve(p_list, algorithm):              ##
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = [[Round(p_list[0][0]), Round(p_list[0][1])], [Round(p_list[-1][0]), Round(p_list[-1][1])]]
    if algorithm == 'Naive':        # 
        return draw_polygon(p_list, 'Naive')
    if algorithm == "Bezier": 
        result += draw_Bezier(0.0, 1.0, p_list[0], p_list[-1], p_list)
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
