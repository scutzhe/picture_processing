#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @author  : 郑祥忠
# @license : (C) Copyright,2016-2020
# @contact : dylenzheng@gmail.com
# @file    : feature.py
# @time    : 11/22/20 3:52 PM
# @desc    : 
'''
"""
HOG 方向梯度直方图
address:https://blog.csdn.net/ppp8300885/article/details/71078555
HOG特征提取算法的整个实现过程大致如下：
    读入所需要的检测目标即输入的image
    将图像进行灰度化（将输入的彩色的图像的r,g,b值通过特定公式转换为灰度值）
    采用Gamma校正法对输入图像进行颜色空间的标准化（归一化）
    计算图像每个像素的梯度（包括大小和方向），捕获轮廓信息
    统计每个cell的梯度直方图（不同梯度的个数），形成每个cell的descriptor
    将每几个cell组成一个block（以3*3为例），一个block内所有cell的特征串联起来得到该block的HOG特征descriptor
    将图像image内所有block的HOG特征descriptor串联起来得到该image（检测目标）的HOG特征descriptor，这就是最终分类的特征向量
HOG参数设置是：2*2细胞／区间、8*8像素／细胞、8个直方图通道,步长为1。
"""
import math
import matplotlib.pyplot as plt
import cv2
import numpy as np

def hog_example(image):
    """
    @param image:
    @return:
    """
    # first step
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    # second step
    height, width = image_gray.shape
    gradient_values_x = cv2.Sobel(image_gray, cv2.CV_64F, 1, 0, ksize=5)
    gradient_values_y = cv2.Sobel(image_gray, cv2.CV_64F, 0, 1, ksize=5)
    gradient_magnitude = cv2.addWeighted(gradient_values_x, 0.5, gradient_values_y, 0.5, 0)
    gradient_angle = cv2.phase(gradient_values_x, gradient_values_y, angleInDegrees=True)
    print(gradient_magnitude.shape, gradient_angle.shape)

    # third step
    cell_size = 8
    bin_size = 8
    angle_unit = 360 / bin_size
    gradient_magnitude = abs(gradient_magnitude)
    cell_gradient_vector = np.zeros((height / cell_size, width / cell_size, bin_size))
    print(cell_gradient_vector.shape)

    def cell_gradient(cell_magnitude, cell_angle):
        orientation_centers = [0] * bin_size
        for k in range(cell_magnitude.shape[0]):
            for l in range(cell_magnitude.shape[1]):
                gradient_strength = cell_magnitude[k][l]
                gradient_angle = cell_angle[k][l]
                min_angle = int(gradient_angle / angle_unit) % 8
                max_angle = (min_angle + 1) % bin_size
                mod = gradient_angle % angle_unit
                orientation_centers[min_angle] += (gradient_strength * (1 - (mod / angle_unit)))
                orientation_centers[max_angle] += (gradient_strength * (mod / angle_unit))
        return orientation_centers

    for i in range(cell_gradient_vector.shape[0]):
        for j in range(cell_gradient_vector.shape[1]):
            cell_magnitude = gradient_magnitude[i * cell_size:(i + 1) * cell_size,
                             j * cell_size:(j + 1) * cell_size]
            cell_angle = gradient_angle[i * cell_size:(i + 1) * cell_size,
                         j * cell_size:(j + 1) * cell_size]
            print(cell_angle.max())
            cell_gradient_vector[i][j] = cell_gradient(cell_magnitude, cell_angle)

    # fourth step
    hog_image = np.zeros([height, width])
    cell_gradient = cell_gradient_vector
    cell_width = cell_size / 2
    max_mag = np.array(cell_gradient).max()
    for x in range(cell_gradient.shape[0]):
        for y in range(cell_gradient.shape[1]):
            cell_grad = cell_gradient[x][y]
            cell_grad /= max_mag
            angle = 0
            angle_gap = angle_unit
            for magnitude in cell_grad:
                angle_radian = math.radians(angle)
                x1 = int(x * cell_size + magnitude * cell_width * math.cos(angle_radian))
                y1 = int(y * cell_size + magnitude * cell_width * math.sin(angle_radian))
                x2 = int(x * cell_size - magnitude * cell_width * math.cos(angle_radian))
                y2 = int(y * cell_size - magnitude * cell_width * math.sin(angle_radian))
                cv2.line(hog_image, (y1, x1), (y2, x2), int(255 * math.sqrt(magnitude)))
                angle += angle_gap

    plt.imshow(hog_image, cmap=plt.cm.gray)
    plt.show()

if __name__ == '__main__':
    image_path = ""
    image = cv2.imread(image_path)
    hog_example(image)
    pass