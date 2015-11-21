#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ast
import shutil
import argparse
import os, os.path

# module imports
import moviebarcode.color_gen as cg
import moviebarcode.run_ffmpeg as ffmpg
import moviebarcode.color_barcode_gen as cbg
import moviebarcode.image_barcode_gen as ibg


parser = argparse.ArgumentParser()
frame_group = parser.add_mutually_exclusive_group()
barcode_group = parser.add_argument_group('Barcode Options', 'options for customizing the barcode.')
video_group = parser.add_argument_group('Video Options', 'options for customizing the video')
parser.add_argument('infile', type=str, nargs='?', help='video filename')
parser.add_argument('-o', '--outfile', type=str, default='barcode.png',
                    help='name of the generated barcode. Default is barcode.png')
parser.add_argument('-im', '--images', action='store_true',
                    help='name of the generated barcode. Default is barcode.png')
frame_group.add_argument('-fc', '--framecolors', action='store_true',
                    help='A frame_colors.txt file exists in the movies directory.')
frame_group.add_argument('-nf', '--noframes', action='store_true',
                    help='Won\'t create the frames. Must already have them in a directory called frames.')
parser.add_argument('-nd', '--nodelete', action='store_true',
                    help='Won\'t delete the movie frames after done executing.')
barcode_group.add_argument('-k', '--kmeans', action='store_true',
                    help='Use kmeans to generate color instead of just PIL (slower but more accurate colors).')
barcode_group.add_argument('-bw', '--barwidth', type=int, default=5,
                    help='Set the width of the bars in the barcode. Default is 5px.')
barcode_group.add_argument('-ht', '--height', type=int, default=1200,
                    help='Set the height of the barcode. Default is 1200px.')
barcode_group.add_argument('-w', '--width', type=int, default=1920,
                    help='Set the final width of the barcode. Default is 1920px.')
video_group.add_argument('-fr', '--framerate', type=str, default='1/24',
                         help='Set the framerate for breaking the movie into frames. Default is 1/24.')
video_group.add_argument('-sc', '--scale', type=str, default='-1:480',
                         help='Set the scale of the frames generated. Default is -1:480.')
video_group.add_argument('-ss', '--start', type=str,
                         help='Set the starting point in the video e.g. 01:08:45.000 or 83 (seconds)')
video_group.add_argument('-d', '--duration', type=str,
                         help='Set the duration for the video e.g. 01:08:45.000 or 83 (seconds).')
video_group.add_argument('-en', '--end', type=str,
                         help='Set the duration end point for the video e.g. 01:08:45.000 or 83 (seconds).')
parser.add_argument('-t', '--threads', type=int, default=8,
                    help='Number of threads to be spawned when finding frame colors. Default is 8.')
args = parser.parse_args()

# check if there was no filename given and was not markd with frame colors
if not args.infile and not args.framecolors and not args.noframes:
    parser.error('and infile name is required unless -fc or -nf is passed.')

if args.noframes and not os.path.exists('frames'):
    parser.error('the no frames argument was passed, but there is no frames directory.')

if args.framecolors and not os.path.isfile('frame_colors.txt'):
    parser.error('the use frame_colors.txt argument was passed, but frame_colors.txt does not exist.')

if args.images and args.framecolors:
    parser.error('-im and -fc cannot be used together.')


def main():
    try:
        # attempt to create the directory structure if it doesn't exist
        os.mkdir('frames')
    except OSError:
        pass

    if not args.noframes and not args.framecolors:
        ffmpg.create_movie_frames(args.infile, args.scale, args.framerate, 
                                  args.start, args.duration, args.end)

    if args.images:
        # create the barcode using images
        ibg.spawn_image_threads(args.threads, args.outfile, args.barwidth, args.height, args.width)
    else:
        if not args.framecolors:
            colors = cg.spawn_threads(args.threads, args.kmeans)

            with open('frame_colors.txt', 'w') as f:
                if args.kmeans:
                    f.write('\n'.join('(%i, %i, %i)' % x for x in colors))
                else:
                    f.write('\n'.join('(%i, %i, %i, %i)' % x for x in colors))
        else:
            with open('frame_colors.txt', 'r') as f:
                colors = [ast.literal_eval(line) for line in f]

        cbg.create_color_barcode(colors, args.barwidth, args.height, args.width, args.outfile)

    if not args.nodelete:
        print('Cleaning up...')
        shutil.rmtree('frames')


if __name__ == '__main__':
    main()
