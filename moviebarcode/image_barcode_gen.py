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


def create_thread_barcode(bar_width, height, fname, images, thread_id, q):
    t_bc = Image.new('RGB', (bar_width * len(images), height))
    # save how wide the piece is for stiching together the pieces
    piece_width = bar_width * len(images)

    posx = 0
    for img in images:
        temp = Image.open(img)
        temp = temp.resize((bar_width, height), Image.ANTIALIAS)
        t_bc.paste(temp, (posx, 0))

        posx += bar_width


    t_bc.save(fname, 'PNG')
    q.put((thread_id, t_bc, piece_width))


def create_final_image_barcode(pieces_width, final_width, height, fname, images):
    bc = Image.new('RGB', (pieces_width, height))
    
    posx = 0
    for img in pyprind.prog_bar(images):
        bc.paste(img[0], (posx, 0))
        posx += img[1]

    os.chdir('..')
    bc = bc.resize((final_width, height), Image.ANTIALIAS)
    bc.save(fname, 'PNG')


def spawn_image_threads(num_threads, fname, bar_width, height, width):
    # change directories if it already isn't in frames
    if not 'frames' in os.getcwd():
        os.chdir('frames')

    q = queue.Queue()

    # get a distributed list of images for the threads
    images = helpers.distribute_frame_lists(num_threads)
    
    threads = []
    for i in range(num_threads):
        t_fname = 'thread_{}_barcode.png'.format(i)
        thread = threading.Thread(target=create_thread_barcode, 
                                  args=(bar_width, height, t_fname, images[i], i, q))
        threads.append(thread)


    # stitch together several smaller barcodes on seperate threads
    # to speed up the process
    print('{} threads creating barcodes with {} frames each...'.format(num_threads, len(images[0])))
    print('Progress bar may take a while to start moving if there are a lot of frames.')
    for thread in threads:
        # thread.daemon = True
        thread.start()

    pieces_width = 0
    # a list to put the thread results in the correct order
    thread_results = [None] * num_threads 
    for i in pyprind.prog_bar(range(num_threads)):
        result = q.get()
        thread_results[result[0]] = [result[1], result[2]]
        pieces_width += result[2]

    # then finally stitch together all the pices that the threads
    # generated
    print('Generating final barcode...')
    create_final_image_barcode(pieces_width, width, height, fname, thread_results)

    # delete thread pieces
    for i in range(num_threads):
        os.remove('frames/thread_{}_barcode.png'.format(i))

    return