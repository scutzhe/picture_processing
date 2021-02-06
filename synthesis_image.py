#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @author  : 郑祥忠
# @license : (C) Copyright,2016-2020
# @contact : dylenzheng@gmail.com
# @file    : synthesis_image.py
# @time    : 11/22/20 4:14 PM
# @desc    : 
'''
import os
import cv2
import random
from PIL import Image

def pic_video(image_dir):
    """
    @param image_dir:
    @return:
    """
    assert os.path.exists(image_dir),"{} is null!!!".format(image_dir)
    fps = 24
    size = (1920, 1080)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    video_path = "{}.mp4".format(image_dir.split("/")[-2])
    video = cv2.VideoWriter(video_path, fourcc, fps, size)
    image_names = os.listdir(image_dir)
    image_names_sorted = sorted(image_names, key=lambda x: int(x.split('/')[-1].split('.')[0].split("_")[-1]))
    for image_name in image_names_sorted:
        image_path = os.path.join(image_dir, image_name)
        image = cv2.imread(image_path)
        video.write(image)
        # cv2.imshow("image", image)
        # cv2.waitKey(1)

def zip_video(ori_video_path,fps,zip_video_path):
    """
    @param ori_video_path:
    @param fps:
    @param zip_video_path:
    @return:
    """
    # 默认压缩文件方式
    os.system("ffmpeg -i {} {}".format(ori_video_path,zip_video_path))
    # 指定输出帧率 -r
    os.system("ffmpeg -i {} -r {} {}".format(ori_video_path, fps, zip_video_path))
    # 指定文件大小 -fs
    os.system("ffmpeg -i {} -r {} -fs {} {}".format(ori_video_path, fps, 15, zip_video_path))
    # 改变分辨率 -s
    os.system("ffmpeg -i {} -r {} -s {} {}".format(ori_video_path, fps, (640,480), zip_video_path))
    # 改变码率 -b:v
    os.system("ffmpeg -i {} -r {} -b:v {} {}".format(ori_video_path, fps, "1.5M", zip_video_path))
    # ffmpeg -i old.mp4 -r 24 -b:v 1.5M new.mp4

def split_channel(image):
    """
    @param image:
    @return:
    """
    # split channel
    (B,G,R) = cv2.split(image)
    cv2.imshow("B",B)
    cv2.imshow("G",G)
    cv2.imshow("R",R)
    cv2.waitKey(1000)
    # merge channel
    image_new = cv2.merge([R,G,B])
    cv2.imshow("image_new",image_new)
    cv2.waitKey(1000)

def extract_background(image):
    """
    @param image:
    @return:
    """

def extract_foreground(image):
    """
    @param image:
    @return:
    """

def synthesis_simple_image(image_mother,image_son,coordination=None,factor=1):
    """
    @param image_mother:母图
    @param image_son:子图
    @param coordination:子图在母图中的坐标
    @param factor:子图缩放因子
    @return:
    """
    H_M,W_M = image_mother.size
    H_S,W_S = image_son.size
    size_h = H_S / factor
    size_w = W_S / factor

    if size_h > H_M:
        size_h = H_M
    if size_w > W_M:
        size_w = W_M

    icon = image_son.resize((size_w,size_h),Image.CUBIC)
    x_start = (W_M - W_S) // 2
    y_start = (H_M - H_S) // 2
    try:
        if coordination == None:
            coordination = (x_start,y_start)
            image_mother.paste(icon,coordination,mask=None)
        else:
            print(" paint by coordination")
            image_mother.paste(icon,coordination,mask=None)
    except Exception as e:
        print(e)

    return image_mother


def synthesis_random_image(image_mother,image_son,coordination=None,factor=1):
    """
    @param image_mother:
    @param image_son:
    @param coordination:
    @param factor:
    @return:
    """
    """
    这是一种方法在原图任意位置上贴图的方法,目的是增强目标检测
    """
    H_M, W_M = image_mother.size
    H_S, W_S = image_son.size
    size_h = H_S / factor
    size_w = W_S / factor

    if size_h > H_M:
        size_h = H_M
    if size_w > W_M:
        size_w = W_M

    icon = image_son.resize((size_w, size_h), Image.CUBIC)
    x_start = (W_M - W_S) // 2
    y_start = (H_M - H_S) // 2
    try:
        if coordination == None:
            coordination = (x_start, y_start)
            image_mother.paste(icon, coordination, mask=None)
        else:
            x = random.randint(0,W_M-size_w)
            y = random.randint(0,H_M-size_h)
            if (x < W_M-size_w and y < H_M-size_h):
                coordination = (x,y)
                image_mother.paste(icon,coordination,mask=None)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    pass