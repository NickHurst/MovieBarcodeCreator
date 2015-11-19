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


def find_frame_bar_color(infile, last_col=None):
    img = Image.open(infile)
    result = img.convert('P', palette=Image.ADAPTIVE)
    result.putalpha(0)
    colors = result.getcolors()

    if last_col == colors[0][1]:
        return last_col

    return colors[0][1]


def get_image_colors(thread_id, q, images):
    colors = []
    for img in images:
        colors.append(find_frame_bar_color(img))

    q.put((thread_id, colors))


def create_color_barcode(colors, bar_width, height, width, fname):
    barcode_width = len(colors) * bar_width
    bc = Image.new('RGB', (barcode_width, height))
    draw = ImageDraw.Draw(bc)

    posx = 0
    print('Generating barcode...')
    for color in pyprind.prog_bar(colors):
        draw.rectangle([posx, 0, posx + bar_width, height], fill=color)
        posx += bar_width

    del draw

    bc = bc.resize((width, height), Image.ANTIALIAS)
    bc.save(fname, 'PNG')


def spawn_threads(threads):
    # change directories if it already isn't in frames
    if not 'frames' in os.getcwd():
        os.chdir('frames')

    q = queue.Queue()
    num_threads = threads

    # get a distributed list of images for the threads
    images = helpers.distribute_frame_lists(num_threads)

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=get_image_colors, args=(i, q, images[i]))
        threads.append(thread)

    print('{} threads generating frame colors with {} frames each...'.format(num_threads, len(images[0])))
    for thread in threads:
        thread.daemon = True
        thread.start()

    thread_results = [None] * num_threads
    for i in pyprind.prog_bar(range(num_threads)):
        result = q.get()
        thread_results[result[0]] = result[1]

    # return to the original directory
    os.chdir('..')

    return [item for sublist in thread_results for item in sublist]