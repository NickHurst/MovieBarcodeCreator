#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os, os.path

def distribute_frame_lists(n):
    # build a list of images the threads need
    # img_list = [img for img in os.listdir(os.getcwd()) if img.endswith('.png')]
    img_list = []
    for img in os.listdir(os.getcwd()):
        if img.endswith('.png') and 'thread_' not in img:
            img_list.append(img)

    # determine the size each thread is going to get
    slice_size = len(img_list) // n
    # check if it wasn't an even division
    remainder = len(img_list) % n
    result = []
    iterater = iter(img_list)

    # build each threads image list
    for i in range(n):
        result.append([])
        for j in range(slice_size):
            result[i].append(next(iterater))
        if remainder:
            result[i].append(next(iterater))
            remainder -= 1

    return result
