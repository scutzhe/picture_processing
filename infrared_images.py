#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @author  : 郑祥忠
# @license : (C) Copyright,2016-2020
# @contact : dylenzheng@gmail.com
# @file    : infrared_images.py
# @time    : 11/14/20 10:18 AM
# @desc    : 
'''
import cv2
import numpy as np

def infrared_image(image):
    """
    @param image:
    @return:
    """
    # step 2 BGR->HSV
    image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    # next step



def BGR2HSV(image_bgr):
    """
    @param image_bgr:
    @return:
    """
    img = image_bgr.copy() / 255.
    hsv = np.zeros_like(img, dtype=np.float32)
    # get max and min
    max_v = np.max(img, axis=2).copy()
    min_v = np.min(img, axis=2).copy()
    min_arg = np.argmin(img, axis=2)
    # H
    hsv[..., 0][np.where(max_v == min_v)] = 0
    ## if min == B
    ind = np.where(min_arg == 0)
    hsv[..., 0][ind] = 60 * (img[..., 1][ind] - img[..., 2][ind]) / (max_v[ind] - min_v[ind]) + 60
    ## if min == R
    ind = np.where(min_arg == 2)
    hsv[..., 0][ind] = 60 * (img[..., 0][ind] - img[..., 1][ind]) / (max_v[ind] - min_v[ind]) + 180
    ## if min == G
    ind = np.where(min_arg == 1)
    hsv[..., 0][ind] = 60 * (img[..., 2][ind] - img[..., 0][ind]) / (max_v[ind] - min_v[ind]) + 300
    # S
    hsv[..., 1] = max_v.copy() - min_v.copy()
    # V
    hsv[..., 2] = max_v.copy()
    return hsv


def HSV2BGR(image_hsv, hsv):
    """
    @param image_hsv:
    @param hsv:
    @return:
    """
    img = image_hsv.copy() / 255.
    # get max and min
    max_v = np.max(img, axis=2).copy()
    min_v = np.min(img, axis=2).copy()
    out = np.zeros_like(img)
    H = hsv[..., 0]
    S = hsv[..., 1]
    V = hsv[..., 2]
    C = S
    H_ = H / 60.
    X = C * (1 - np.abs(H_ % 2 - 1))
    Z = np.zeros_like(H)
    vals = [[Z, X, C], [Z, C, X], [X, C, Z], [C, X, Z], [C, Z, X], [X, Z, C]]
    for i in range(6):
        ind = np.where((i <= H_) & (H_ < (i + 1)))
        out[..., 0][ind] = (V - C)[ind] + vals[i][0][ind]
        out[..., 1][ind] = (V - C)[ind] + vals[i][1][ind]
        out[..., 2][ind] = (V - C)[ind] + vals[i][2][ind]
    out[np.where(max_v == min_v)] = 0
    out = np.clip(out, 0, 1)
    out = (out * 255).astype(np.uint8)
    return out

def grary_image(image):
    """
    @param image:
    @return:
    """
    image_name = ""
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    cv2.imwrite("result/{}".format(image_name),image_gray)
    pass

def blak_white_opencv(image):
    """
    @param image:
    @return:
    """
    # step 1 转换成灰度图片
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    # step2 灰度图片转换成黑白图片
    ret, thresh = cv2.threshold(image_gray,125,255,cv2.THRESH_BINARY)
    cv2.imwrite("result.jpg",thresh)


def black_white_pil(image_path):
    """
    @param image_path:
    @return:
    """
    from PIL import Image
    image = Image.open(image_path)
    image_black_white = image.convert("1")
    image_black_white.save("result.png")


if __name__ == '__main__':
    pass