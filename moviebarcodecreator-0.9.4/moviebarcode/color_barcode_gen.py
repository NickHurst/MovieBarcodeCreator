#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pyprind
import threading
import os, os.path
from PIL import Image, ImageDraw
import moviebarcode.helpers as helpers

try:
    import queue
except ImportError:
    import Queue as queue


def create_color_barcode(colors, bar_width, height, width, fname):
    barcode_width = len(colors) * bar_width
    bc = Image.new('RGB', (barcode_width, height))
    draw = ImageDraw.Draw(bc)

    # draw the new barcode
    posx = 0
    print('Generating barcode...')
    for color in pyprind.prog_bar(colors):
        draw.rectangle([posx, 0, posx + bar_width, height], fill=color)
        posx += bar_width

    del draw

    bc = bc.resize((width, height), Image.ANTIALIAS)
    bc.save(fname, 'PNG')
