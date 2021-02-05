#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @author  : dylen
# @license : (C) Copyright,2018-
# @contact : dylenzheng@gmail.com
# @file    : optical_process.py
# @time    : 12/29/20 3:16 PM
# @desc    : 
'''

import cv2
import numpy as np

def uneven_light_compensate(image, blockSize=32):
    """
    去除光照不均匀
    @param image: BGR
    @param blockSize: 
    @return:
    """
    # 1,求取源图I的平均灰度，并记录rows和cols；
    # 2,按照一定大小，分为N*M个方块，求出每块的平均值，得到子块的亮度矩阵D；
    # 3,用矩阵D的每个元素减去源图的平均灰度，得到子块的亮度差值矩阵E；
    # 4,用双立方差值法，将矩阵E差值成与源图一样大小的亮度分布矩阵R；
    # 5,得到矫正后的图像result=I-R；
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    average = np.mean(gray)

    rows_new = int(np.ceil(gray.shape[0] / blockSize))
    cols_new = int(np.ceil(gray.shape[1] / blockSize))

    blockImage = np.zeros((rows_new, cols_new), dtype=np.float32)
    for r in range(rows_new):
        for c in range(cols_new):
            row_min = r * blockSize
            row_max = (r + 1) * blockSize
            if (row_max > gray.shape[0]):
                row_max = gray.shape[0]
            col_min = c * blockSize
            col_max = (c + 1) * blockSize
            if (col_max > gray.shape[1]):
                col_max = gray.shape[1]

            imageROI = gray[row_min:row_max, col_min:col_max]
            temaver = np.mean(imageROI)
            blockImage[r, c] = temaver

    blockImage = blockImage - average
    blockImage2 = cv2.resize(blockImage, (gray.shape[1], gray.shape[0]), interpolation=cv2.INTER_CUBIC)
    gray2 = gray.astype(np.float32)
    dst = gray2 - blockImage2
    dst = dst.astype(np.uint8)
    # GaussianBlur核的大小,这里取3
    dst = cv2.GaussianBlur(dst, (3, 3), 0)
    dst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

    return dst


if __name__ == '__main__':
    image_path = ''
    blockSize = 16
    image = cv2.imread(image_path)
    dst = uneven_light_compensate(image, blockSize)
    result = np.concatenate([image, dst], axis=1)
    cv2.imshow('result', result)
    cv2.waitKey(0)
