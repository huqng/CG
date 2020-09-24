#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math

def Round(f):
    if f - int(f) >= 0.5:
        return int(f) + 1
    else:
        return int(f)
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
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = [[Round(x0), Round(y0)]]
    if algorithm == 'Naive':
        if x0 == x1:
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            for y in range(int(y0), int(y1 + 1)):
                result.append((Round(x0), Round(y)))
            return result
        if x0 > x1:
            x0, y0, x1, y1 = x1, y1, x0, y0
        k = (y1 - y0) / (x1 - x0)
        for x in range(int(x0), int(x1 + 1)):
            px = x
            py = y0 + k * (x - x0)
            result.append((Round(px), Round(py)))
        
        if abs(k) > 1:
            if y0 > y1:     # y0 won't = y1, otherwise k = 0
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (x1 - x0) / (y1 - y0)       
            for y in range(int(y0), int(y1 + 1)):
                py = y
                px = x0 + k * (y - y0)
                result.append((Round(px), Round(py)))
        
    elif algorithm == 'DDA':
        pass
    elif algorithm == 'Bresenham':
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
    if len(p_list) > 2:
        result += draw_line([p_list[-1], p_list[0]], algorithm)
    return result


def draw_ellipse(p_list):                       #
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    if x0 == x1:
        return draw_line(p_list, 'Naive')
    if y0 == y1:
        return draw_line(p_list, 'Naive')
    x2 = (x0 + x1) / 2
    y2 = (y0 + y1) / 2
    k = abs((y1 - y0) / (x1 - x0))
    r = abs(x2 - x0)
    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0
    for x in range(int(-r), int(r + 1)):
        y = math.sqrt(r * r - x * x)
        y = y * k
        result.append((Round(x + x2), Round(y2 + y)))
        result.append((Round(x + x2), Round(y2 - y)))
    
    k = abs((x1 - x0) / (y1 - y0))
    r = abs(y2 - y0)
    if y0 > y1:
        x0, y0, x1, y1 = x1, y1, x0, y0
    for y in range(int(- r), int(r + 1)):
        x = math.sqrt(r * r - y * y)
        x = x * k
        result.append((Round(x2 + x), Round(y2 + y)))
        result.append((Round(x2 - x), Round(y2 + y)))
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
    print("Rotate at", x, y, "| degree =", r)
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
