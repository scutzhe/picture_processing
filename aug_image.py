#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @author  : dylen
# @license : (C) Copyright,2018-
# @contact : dylenzheng@gmail.com
# @file    : aug_image.py
# @time    : 2/4/21 9:02 AM
# @desc    : 
'''
import cv2
import numpy as np
from imgaug import augmenters as iaa

def image_aug(image):
    """
    @param image:
    @return:
    """
    seq = iaa.SomeOf((1, 3), [
        iaa.Crop(px=(0, 16)),  # 裁剪
        iaa.Multiply((0.7, 1.3)),  # 改变色调
        iaa.Affine(
            scale=(0.5, 0.7)),  # 放射变换
        iaa.GaussianBlur(sigma=(0, 1.5)),  # 高斯模糊
        iaa.AddToHueAndSaturation(value=(25, -25)),
        iaa.ChannelShuffle(1),  # RGB三通道随机交换
        iaa.ElasticTransformation(alpha=0.1),
        iaa.Grayscale(alpha=(0.2, 0.5)),
        iaa.Pepper(p=0.03),
        iaa.AdditiveGaussianNoise(scale=(0.03 * 255, 0.05 * 255)),
        iaa.Dropout(p=(0.03, 0.05)),
        iaa.Salt(p=(0.03, 0.05)),
        iaa.AverageBlur(k=(1, 3)),
        iaa.Add((-10, 10)),
        iaa.CoarseSalt(size_percent=0.01)
    ])
    seq_det = seq.to_deterministic()
    image_aug = seq_det.augment_images([image])[0]

    return image_aug

if __name__ == '__main__':
    pass