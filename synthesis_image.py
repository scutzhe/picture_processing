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

def synthesis(image_one,image_two):
    """
    @param image_one:
    @param image_two:
    @return:
    """

if __name__ == '__main__':
    pass