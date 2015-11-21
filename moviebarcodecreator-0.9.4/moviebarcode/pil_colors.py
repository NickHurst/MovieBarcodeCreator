#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from PIL import Image, ImageDraw

def find_frame_bar_color(infile, last_col=None):
    # grab the dominant color
    img = Image.open(infile)
    result = img.convert('P', palette=Image.ADAPTIVE, colors=1)
    result.putalpha(0)
    colors = result.getcolors()

    return colors[0][1]


def get_image_colors(thread_id, q, images):
    # build a list of all the colors from each threads
    # set of images
    colors = []
    for img in images:
        colors.append(find_frame_bar_color(img))

    q.put((thread_id, colors))