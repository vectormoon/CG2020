#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append([x0, y])
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append([x, int(y0 + k * (x - x0))])

    elif algorithm == 'DDA':
        if (x0 == x1):
            if (y0 > y1):
                y0,y1 = y1, y0
            y0 = int(y0)
            y1 = int(y1)
            for y in range(y0, y1 + 1):
                result.append([x0,y])
            return result
        m = abs((y1-y0) / (x1-x0))
        #m<1
        if abs(x0-x1) > abs(y0-y1):
            if x0 > x1:
                x0, x1 = x1, x0
                y0, y1 = y1, y0
            delta_y = m
            #start at left
            if y0 < y1:
                result.append([x0,y0])
                y_k = y0
                x0 = int(x0)
                x1 = int(x1)
                for x in range(x0 + 1, x1 + 1):
                    y_k += delta_y
                    result.append([x, int(y_k + 0.5)])
            #start at right
            else:
                result.append([x1,y1])
                y_k = y1
                x1 = int(x1)
                x0 = int(x0)
                for x in range(x1 - 1, x0 - 1, -1):
                    y_k += delta_y
                    result.append([x, int(y_k + 0.5)])
        #m>=1
        else:
            if y0 > y1:
                x0, x1 = x1, x0
                y0, y1 = y1, y0
            delta_x = 1/m
            #start at left
            if x0 < x1:
                result.append([x0,y0])
                x_k = x0
                y0 = int(y0)
                y1 = int(y1)
                for y in range(y0 + 1, y1 + 1):
                    x_k += delta_x
                    result.append([int(x_k + 0.5), y])
            #start at right
            else:
                result.append([x1,y1])
                x_k = x1
                y1 = int(y1)
                y0 = int(y0)
                for y in range(y1 - 1, y0 - 1, -1):
                    x_k += delta_x
                    result.append([int(x_k + 0.5), y])

    elif algorithm == 'Bresenham':
        if (x0 == x1):
            if (y0 > y1):
                y0,y1 = y1,y0
            y0 = int(y0)
            y1 = int(y1)
            for y in range(y0, y1 + 1):
                result.append([x0,y])
            return result
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        if abs(dy/dx) < 1:
            if x0 > x1:
                x0, x1 = x1, x0
                y0, y1 = y1, y0
            flag = 0        #flag=0 start at left flag = 1 start at right
            if y0 > y1:
                flag = 1
            result.append([x0, y0])
            p_k = 2*dy-dx
            y_k = y0
            x0 = int(x0)
            x1 = int(x1)
            for x in range(x0 + 1, x1 + 1):
                if (p_k >= 0):
                    p_k = p_k + 2*dy - 2*dx
                    if flag == 0:
                        y_k += 1
                    elif flag == 1:
                        y_k -= 1
                    result.append([x, y_k])
                elif (p_k < 0):
                    p_k = p_k + 2*dy
                    result.append([x, y_k])
        else:
            dy, dx = dx, dy
            if y0 > y1:
                x0, x1 = x1, x0
                y0, y1 = y1, y0
            flag = 0        #flag=0 start at right flag = 1 start at left
            if x0 > x1:
                flag = 1
            result.append([x0, y0])
            p_k = 2*dy-dx
            x_k = x0
            y0 = int(y0)
            y1 = int(y1)
            for y in range(y0 + 1, y1 + 1):
                if (p_k >= 0):
                    p_k = p_k + 2*dy - 2*dx
                    if flag == 0:
                        x_k += 1
                    elif flag == 1:
                        x_k -= 1
                    result.append([x_k, y])
                elif (p_k < 0):
                    p_k = p_k + 2*dy
                    result.append([x_k, y])
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    dx = int((x0+x1) / 2)
    dy = int((y0+y1) / 2)
    r_x = int(abs((x1 - x0) / 2))
    r_y = int(abs((y1 - y0) / 2))
    r_x_2 = r_x * r_x
    r_y_2 = r_y * r_y
    x_k = 0
    y_k = r_y
    p_k = r_y_2 - r_x_2*r_y + (r_x_2/4)
    result.append([x_k, y_k])
    while 2*r_y_2*x_k < 2*r_x_2*y_k:
        #p_k = r_y_2 * pow((x_k+1), 2) + r_x_2 * pow((y_k - 1/2), 2) - r_x_2*r_y_2
        if p_k < 0:
            p_k = p_k + 2*r_y_2*x_k + 3*r_y_2
        else:
            p_k = p_k + 2*r_y_2*x_k - 2*r_x_2*y_k + 2*r_x_2 + 3*r_y_2
            y_k -= 1
        x_k += 1
        result.append([x_k, y_k])
    p_k = r_y_2*pow((x_k+1/2), 2) + r_x_2*pow((y_k-1),2) - r_x_2*r_y_2
    while y_k > 0:
        if p_k > 0:
            p_k = p_k - 2*r_x_2*y_k + 3*r_x_2
        else:
            x_k += 1
            p_k = p_k + 2*r_y_2*x_k - 2*r_x_2*y_k + 2*r_y_2 + 3*r_x_2
        y_k -= 1
        result.append([x_k,y_k])
    
    first_quadrant = result
    second_quadrant = []
    third_quadrant = []
    fourth_quadrant = []
    for i in range(len(first_quadrant)):
        tmp_point_1 = [[0,0]]
        tmp_point_1[0][0] = first_quadrant[i][0]
        tmp_point_1[0][1] = -first_quadrant[i][1]
        second_quadrant.append(tmp_point_1[0])
        tmp_point_2 = [[0,0]]
        tmp_point_2[0][0] = -first_quadrant[i][0]
        tmp_point_2[0][1] = -first_quadrant[i][1]
        third_quadrant.append(tmp_point_2[0])
        tmp_point_3 = [[0,0]]
        tmp_point_3[0][0] = -first_quadrant[i][0]
        tmp_point_3[0][1] = first_quadrant[i][1]
        fourth_quadrant.append(tmp_point_3[0])

    result = first_quadrant + second_quadrant + third_quadrant + fourth_quadrant

    for i in range(len(result)):
        result[i][0] = int(result[i][0]) + int(dx)
        result[i][1] = int(result[i][1]) + int(dy)

    return result


def deBoox_Cox(u, k, i):
    if k == 1:
        if i <= u and u < i + 1:
            return 1
        else:
            return 0
    else:
        coef_1, coef_2 = 0, 0
        if (u-i == 0) and (k-1 == 0):
            coef_1 = 0
        else:
            coef_1 = (u-i) / (k-1)
        if (i+k-u == 0) and (k-1 == 0):
            coef_2 = 0
        else:
            coef_2 = (i+k-u) / (k-1)
    return coef_1 * deBoox_Cox(u, k-1, i) + coef_2 * deBoox_Cox(u, k-1, i+1)


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'，其中"B-spline"要求为三次（四阶）均匀B样条曲线，曲线不必经过首末控制点
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    if algorithm == 'Bezier':
        P = []
        r = len(p_list)
        for j in range(0, r):
            x, y = p_list[j][0], p_list[j][1]
            P.append([x, y])
        j = 0
        for i in range(0, 2923): #2020/09/23
            tmp_r = r
            for j in range(0, r):
                x, y = p_list[j][0], p_list[j][1]
                P[j][0] = x
                P[j][1] = y
            u = i/2923
            x, y = 0, 0
            while (tmp_r != 1):
                for k in range(0, r-1):
                    x0, y0 = P[k][0], P[k][1]
                    x1, y1 = P[k+1][0], P[k+1][1]
                    P[k][0] = (1-u)*x0 + u*x1
                    P[k][1] = (1-u)*y0 + u*y1
                tmp_r -= 1
            x = int(P[0][0] + 0.5)
            y = int(P[0][1] + 0.5)
            result.append([x, y])
    elif algorithm == 'B-spline':
        n = len(p_list)
        k = 4
        u = k - 1
        while (u < n):
            x = 0
            y = 0
            #calc P(u)
            for i in range(0, n):
                B_ik = deBoox_Cox(u, k, i)
                x += B_ik * p_list[i][0]
                y += B_ik * p_list[i][1]
            result.append([int(x + 0.5), int(y + 0.5)])
            u += 1/2927 # 2020/09/27

    return result


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    n = len(p_list)
    result = []
    for i in range(0, n):
        x2 = p_list[i][0] + dx
        y2 = p_list[i][1] + dy
        result.append([x2, y2])
    return result


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    n = len(p_list)
    sin = math.sin(math.radians(r))
    cos = math.cos(math.radians(r))
    result = []

    for i in range(0, n):
        p_list[i][0] -= x
        p_list[i][1] -= y

    for i in range(0, n):
        x1 = p_list[i][0]
        y1 = p_list[i][1]
        x2 = int(x1 * cos - y1 * sin)
        y2 = int(x1 * sin + y1 * cos)
        result.append([x2, y2])

    for i in range(0, n):
        result[i][0] += x
        result[i][1] += y

    return result


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    n = len(p_list)
    result = []

    for i in range(0, n):
        p_list[i][0] -= x
        p_list[i][1] -= y

    for i in range(0, n):
        x1 = p_list[i][0]
        y1 = p_list[i][1]
        x2 = int(x1 * s)
        y2 = int(y1 * s)
        result.append([x2, y2])

    for i in range(0, n):
        result[i][0] += x
        result[i][1] += y

    return result


def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    result = []
    if (x_min == x_max or y_min == y_max):
        result = [[0,0], [0,0]]
        return result
    if x_min > x_max:
        x_min, x_max = x_max, x_min
    if y_min > y_max:
        y_min, y_max = y_max, y_min
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]

    if algorithm == 'Cohen-Sutherland':
        while 1:
            code0 = 0 #1_left, 2_right, 4_down, 8_up
            code1 = 0 #1_left, 2_right, 4_down, 8_up
            #calc code0
            if x0 < x_min:
                code0 += 1
            elif x0 > x_max:
                code0 += 2
            if y0 < y_min:
                code0 += 4
            elif y0 > y_max:
                code0 += 8
            #calc code1
            if x1 < x_min:
                code1 += 1
            elif x1 > x_max:
                code1 += 2
            if y1 < y_min:
                code1 += 4
            elif y1 > y_max:
                code1 += 8
            #inside
            if (code0 | code1) == 0:
                result = [[x0, y0], [x1, y1]]
                break
            #outside
            elif (code0 & code1) != 0:
                result.append([0,0])
                result.append([0,0])
                break
            #otherwise
            else:
                if code0 == 0:
                    x0, x1 = x1, x0
                    y0, y1 = y1, y0
                    code0, code1 = code1, code0
                #1_left, 2_right, 4_down, 8_up
                if (code0 & 1):
                    y0 = int(y0 + ((x_min-x0) * (y0-y1)/(x0-x1)) + 0.5)
                    x0 = x_min
                if (code0 & 2):
                    y0 = int(y0 + ((x_max-x0) * (y0-y1)/(x0-x1)) + 0.5)
                    x0 = x_max
                if (code0 & 4):
                    x0 = int(x0 + ((y_min-y0) * (x0-x1)/(y0-y1)) + 0.5)
                    y0 = y_min
                if (code0 & 8):
                    x0 = int(x0 + ((y_max-y0) * (x0-x1)/(y0-y1)) + 0.5)
                    y0 = y_max

    elif algorithm == 'Liang-Barsky':
        p = [x0-x1, x1-x0, y0-y1, y1-y0]
        q = [x0-x_min, x_max-x0, y0-y_min, y_max-y0]
        u0, u1 = 0, 1
        
        for i in range(4):
            if p[i] < 0:
                u0 = max(u0, q[i]/p[i])
            elif p[i] > 0:
                u1 = min(u1, q[i]/p[i])
            elif (p[i] == 0 and q[i] < 0):
                result = [[0,0], [0,0]]
                return result
            if u0 > u1:
                result = [[0,0], [0,0]]
                return result
        
        #res_x0, res_y0 = 0, 0
        #res_x1, res_y1 = 0, 0
        #if u0 > 0:
        res_x0 = int(x0 + u0*(x1-x0) + 0.5)
        res_y0 = int(y0 + u0*(y1-y0) + 0.5)
        #if u1 < 1:
        res_x1 = int(x0 + u1*(x1-x0) + 0.5)
        res_y1 = int(y0 + u1*(y1-y0) + 0.5)
        result = [[res_x0, res_y0], [res_x1, res_y1]]

    return result

#test_list=[[200,300],[400,150]]
#test_list=[[500,50],[100,200]]
#test_list=[[100,400],[200,200]]
#test_list=[[100,200],[200,400]]
#test_list=[[100,100],[100,200]]
#test_list=[[100,100],[100,50]]
#res = draw_line(test_list, "DDA")

#test_list=[[100,100],[150,100],[150,150]]
#test_list=[[50,50],[50,100],[100,100],[100,50]]
#res = draw_polygon(test_list, "Naive")

#test_list=[[0,100],[200,0]]
#test_list=[[50,150],[250,50]]
#res = draw_ellipse(test_list)

#test_list=[[0,0],[20,100],[40,400]]
#test_list=[[100, 100], [200, 0], [300, 100]]
#test_list=[[100,100], [200, 0], [300, 300], [400, 100], [500, 450]]
#res = draw_curve(test_list, 'B-spline')