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

    ffmpeg_args = ['ffmpeg', '-i', '../' + infile]

    if args.start:
        ffmpeg_args += ['-ss', start]
    if args.duration:
        ffmpeg_args += ['-t', duration]
    if args.end:
        ffmpeg_args += ['-to', end]

    ffmpeg_args += ['-s', scale, '-r', framerate, '-f', 
                    'image2', 'image-%09d.png']

    output = open('ffmpeg_log.txt', 'w')

    print('Creating frames (this might take a while)...')

    try:
        subprocess.call(ffmpeg_args, stderr=output, stdout=subprocess.PIPE)
    except OSError:
        print('ERROR: Could not start FFmpeg process. Please make sure you have FFmpeg installed before running.')
        exit(1)

    output.close()