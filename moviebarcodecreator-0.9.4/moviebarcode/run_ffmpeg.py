#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import subprocess
import os, os.path

def create_movie_frames(infile, scale, framerate, start=None, duration=None, end=None):
    if not 'frames' in os.getcwd():
        os.chdir('frames')

    # build the args
    ffmpeg_args = ['ffmpeg', '-threads', '0']

    if start:
        ffmpeg_args += ['-ss', start]
    if duration:
        ffmpeg_args += ['-t', duration]
    if end:
        ffmpeg_args += ['-to', end]

    ffmpeg_args += ['-i', '../' + infile, '-r', framerate]

    ffmpeg_args += ['-vf', 'scale={}'.format(scale), '-f', 'image2', 'image-%09d.png']

    # open a log for output to be piped to
    output = open('ffmpeg_log.txt', 'w')

    print('Creating frames (this might take a while)...')
    try:
        subprocess.call(ffmpeg_args, stderr=output, stdout=subprocess.PIPE)
    except OSError:  # this will occur if FFmpeg is not installed
        print('ERROR: Could not start FFmpeg process. Please make sure you have FFmpeg installed before running.')
        exit(1)

    output.close()