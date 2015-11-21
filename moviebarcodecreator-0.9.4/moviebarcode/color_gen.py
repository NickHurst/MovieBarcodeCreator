#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pyprind
import threading
import os, os.path

# moviebarcode modues
import moviebarcode.pil_colors as pc
import moviebarcode.k_means_colors as kc
import moviebarcode.helpers as helpers

try:
    import queue
except ImportError:
    import Queue as queue


def spawn_threads(threads, kmeans):
    # change directories if it already isn't in frames
    if not 'frames' in os.getcwd():
        os.chdir('frames')

    q = queue.Queue()
    num_threads = threads

    # get a distributed list of images for the threads
    images = helpers.distribute_frame_lists(num_threads)

    threads = []
    for i in range(num_threads):
        if kmeans:
            thread = threading.Thread(target=kc.get_image_colors,
                                      args=(i, q, images[i]))
        else:
            thread = threading.Thread(target=pc.get_image_colors,
                                      args=(i, q, images[i]))

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