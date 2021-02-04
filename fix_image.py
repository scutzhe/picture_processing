#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @author  : dylen
# @license : (C) Copyright,2018-
# @contact : dylenzheng@gmail.com
# @file    : fix_image.py
# @time    : 2/3/21 4:33 PM
# @desc    : 
'''
import torch
import random
import cv2
import numpy as np
import torch.nn.functional as F

def fix_box(image):
    """
    @param image:
    @return:
    """
    H,W = image.shape[:2]
    scale = max(H,W)
    square = np.zeros((scale,scale,3),np.uint8)
    if H > W:
        square[:,(scale-W)//2 : W+(scale-W)//2,:] = image
    else:
        square[(scale - H) // 2 : H + (scale - H) // 2, :, :] = image
    return square

def crop_box(image_ori,box):
    """
    @param image_ori:
    @param box: [x_min,y_min,x_max,y_max]
    @return:
    """
    # crop image from origin image
    image = image_ori[box[1]:box[3],box[0]:box[2],:]
    w = box[2] - box[0]
    h = box[3] - box[1]
    scale = max(w,h)
    square = np.zeros((scale,scale,3),np.uint8)
    if h > w:
        square[:, (scale - w) // 2: w + (scale - w) // 2, :] = image
    else:
        square[(scale - h) // 2: h + (scale - h) // 2, :, :] = image


def pad_to_square(img, pad_value):
    """
    @param img: tensor
    @param pad_value:
    @return:
    """
    c, h, w = img.shape
    dim_diff = np.abs(h - w)
    # (upper / left) padding and (lower / right) padding
    pad1, pad2 = dim_diff // 2, dim_diff - dim_diff // 2
    # Determine padding
    pad = (0, 0, pad1, pad2) if h <= w else (pad1, pad2, 0, 0)
    # Add padding
    img = F.pad(img, pad, "constant", value=pad_value)

    return img, pad

def resize(image, size):
    """
    @param image: tensor
    @param size:
    @return:
    """
    image = F.interpolate(image.unsqueeze(0), size=size, mode="nearest").squeeze(0)
    return image

def random_resize(images, min_size=288, max_size=448):
    new_size = random.sample(list(range(min_size, max_size + 1, 32)), 1)[0]
    images = F.interpolate(images, size=new_size, mode="nearest")
    return images


if __name__ == '__main__':
    pass
    image = cv2.imread("/home/zhex/git_me/nanodet/test_image/01.png")
    image_fix = fix_box(image)
    print(image_fix.shape)
    cv2.imshow("image",image_fix)
    cv2.waitKey(5000)