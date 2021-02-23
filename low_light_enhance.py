#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @author  : dylen
# @license : (C) Copyright,2018-
# @contact : dylenzheng@gmail.com
# @file    : low_light_enhance.py
# @time    : 2/21/21 8:29 PM
# @desc    : Retinex算法不仅能够增强图像的亮度信息，同时可以去除图片中的部分阴影信息；但是该算法的运算速度比较慢，不能应用到一些实时的场景中
'''
# 参考链接：https://blog.csdn.net/wzz18191171661/article/details/104325353
import numpy as np
import cv2

def singleScaleRetinex(img, sigma=80):
    """
    @param img:
    @param sigma:
    @return:
    """
    '''单尺度Retinex函数'''
    '''sigma取值一般80-100之间'''
    '''
   cv.GaussianBlur(src, ksize, sigmaX, dst=None, sigmaY=None, borderType=None)
    高斯核ksize越大会导致更大程度的过滤，并在输出图像中产生更多的模糊，并增加计算复杂性
    sigmax在高斯滤波器中控制其均值附近的变化，sigmax越大平均值周围允许的方差越大
    增加sigma时，看到广阔的场景而没有注意细节出口，减少该值时获得更多的相信信息
    '''
    retinex = np.log10(img) - np.log10(cv2.GaussianBlur(img, (0, 0), sigma))
    return retinex


def multiScaleRetinex(img, sigma_list=[80,90,100]):
    """
    @param img:
    @param sigma_list:
    @return:
    """
    '''多尺度Retinex函数'''
    # 提前分配空间
    retinex = np.zeros_like(img)
    # 遍历所有的尺度
    for sigma in sigma_list:
        # 对计算的结果进行叠加
        retinex += singleScaleRetinex(img, sigma)
    # 计算多个尺度的平均值
    retinex = retinex / len(sigma_list)
    return retinex

def colorRestoration(img, alpha, beta):
    """
    @param img:
    @param alpha:
    @param beta:
    @return:
    """
    '''颜色灰度函数'''
    img_sum = np.sum(img, axis=2, keepdims=True)
    color_restoration = beta * (np.log10(alpha * img) - np.log10(img_sum))
    return color_restoration

def simplestColorBalance(img, low_clip, high_clip):
    """
    @param img:
    @param low_clip:
    @param high_clip:
    @return:
    """
    '''最简单的颜色均衡函数'''
    total = img.shape[0] * img.shape[1]
    for i in range(img.shape[2]):
        unique, counts = np.unique(img[:, :, i], return_counts=True)
        current = 0
        for u, c in zip(unique, counts):
            if float(current) / total < low_clip:
                low_val = u
            if float(current) / total < high_clip:
                high_val = u
            current += c
        img[:, :, i] = np.maximum(np.minimum(img[:, :, i], high_val), low_val)
    return img


def MSRCR(img, sigma_list, G, b, alpha, beta, low_clip, high_clip):
    """
    @param img:
    @param sigma_list:
    @param G:
    @param b:
    @param alpha:
    @param beta:
    @param low_clip:
    @param high_clip:
    @return:
    """
    '''MSRCR函数'''

    img = np.float64(img) + 1.0
    # 对原图先做多尺度的Retinex
    img_retinex = multiScaleRetinex(img, sigma_list)
    # 对原图做颜色恢复
    img_color = colorRestoration(img, alpha, beta)
    # 进行图像融合
    img_msrcr = G * (img_retinex * img_color + b)

    for i in range(img_msrcr.shape[2]):
        img_msrcr[:, :, i] = (img_msrcr[:, :, i] - np.min(img_msrcr[:, :, i])) / \
                             (np.max(img_msrcr[:, :, i]) - np.min(img_msrcr[:, :, i])) * \
                             255
    # 将图像调整到[0,255]范围内
    img_msrcr = np.uint8(np.minimum(np.maximum(img_msrcr, 0), 255))
    # 做简单的颜色均衡
    img_msrcr = simplestColorBalance(img_msrcr, low_clip, high_clip)
    return img_msrcr


def automatedMSRCR(img, sigma_list):
    """
    @param img:
    @param sigma_list:
    @return:
    """
    '''automatedMSRCR函数'''
    img = np.float64(img) + 1.0
    img_retinex = multiScaleRetinex(img, sigma_list)
    for i in range(img_retinex.shape[2]):
        unique, count = np.unique(np.int32(img_retinex[:, :, i] * 100), return_counts=True)
        for u, c in zip(unique, count):
            if u == 0:
                zero_count = c
                break

        low_val = unique[0] / 100.0
        high_val = unique[-1] / 100.0
        for u, c in zip(unique, count):
            if u < 0 and c < zero_count * 0.1:
                low_val = u / 100.0
            if u > 0 and c < zero_count * 0.1:
                high_val = u / 100.0
                break
        img_retinex[:, :, i] = np.maximum(np.minimum(img_retinex[:, :, i], high_val), low_val)
        img_retinex[:, :, i] = (img_retinex[:, :, i] - np.min(img_retinex[:, :, i])) / \
                               (np.max(img_retinex[:, :, i]) - np.min(img_retinex[:, :, i])) \
                               * 255
    img_retinex = np.uint8(img_retinex)
    return img_retinex


def MSRCP(img, sigma_list, low_clip, high_clip):
    """
    @param img:
    @param sigma_list:
    @param low_clip:
    @param high_clip:
    @return:
    """
    '''MSRCP函数'''
    img = np.float64(img) + 1.0
    intensity = np.sum(img, axis=2) / img.shape[2]
    retinex = multiScaleRetinex(intensity, sigma_list)
    intensity = np.expand_dims(intensity, 2)
    retinex = np.expand_dims(retinex, 2)
    intensity1 = simplestColorBalance(retinex, low_clip, high_clip)
    intensity1 = (intensity1 - np.min(intensity1)) / \
                 (np.max(intensity1) - np.min(intensity1)) * \
                 255.0 + 1.0
    img_msrcp = np.zeros_like(img)

    for y in range(img_msrcp.shape[0]):
        for x in range(img_msrcp.shape[1]):
            B = np.max(img[y, x])
            A = np.minimum(256.0 / B, intensity1[y, x, 0] / intensity[y, x, 0])
            img_msrcp[y, x, 0] = A * img[y, x, 0]
            img_msrcp[y, x, 1] = A * img[y, x, 1]
            img_msrcp[y, x, 2] = A * img[y, x, 2]
    img_msrcp = np.uint8(img_msrcp - 1.0)
    return img_msrcp

if __name__ == '__main__':

    pass