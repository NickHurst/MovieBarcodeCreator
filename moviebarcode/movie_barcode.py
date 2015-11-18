#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ast
import shutil
import argparse
import threading
import subprocess
import os, os.path
from PIL import Image, ImageDraw

try:
    import queue
except ImportError:
    import Queue as queue


parser = argparse.ArgumentParser()
frame_group = parser.add_mutually_exclusive_group()
barcode_group = parser.add_argument_group('Barcode Options', 'options for customizing the barcode.')
parser.add_argument('infile', type=str, nargs='?', help='video filename')
parser.add_argument('-o', '--outfile', type=str, default='barcode.png',
                    help='name of the generated barcode. Default is barcode.png')
frame_group.add_argument('-fc', '--framecolors', action='store_true',
                    help='A frame_colors.txt file exists in the movies directory.')
frame_group.add_argument('-nf', '--noframes', action='store_true',
                    help='Won\'t create the frames. Must already have them in a directory called frames.')
barcode_group.add_argument('-bw', '--barwidth', type=int, default=5,
                    help='Set the width of the bars in the barcode. Default is 5px.')
barcode_group.add_argument('-ht', '--height', type=int, default=1200,
                    help='Set the height of the barcode. Default is 1200px.')
barcode_group.add_argument('-w', '--width', type=int, default=1920,
                    help='Set the final width of the barcode. Default is 1920px.')
parser.add_argument('-nd', '--nodelete', action='store_true',
                    help='Won\'t delete the movie frames after done executing.')
parser.add_argument('-fr', '--framerate', type=str,
                    help='Set the framerate for breaking the movie into frames. Default is 1/24.')
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


def create_movie_frames(infile):
    os.chdir('./frames')

    framerate = args.framerate if args.framerate else '1/24'
    ffmpeg_args = ['ffmpeg', '-threads', '0', '-i', '../' + infile, '-r', framerate,
                   '-f', 'image2', 'image-%07d.png']

    output = open('ffmpeg_log.txt', 'w')

    print('Creating frames (this might take a while)...')

    try:
        subprocess.call(ffmpeg_args, stderr=output, stdout=subprocess.PIPE)
    except OSError:
        print('ERROR: Could not start FFmpeg process. Please make sure you have FFmpeg installed before running.')
        exit(1)

    output.close()


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


def distribute_frame_lists(n):
    img_list = [img for img in os.listdir(os.getcwd()) if img.endswith('.png')]
    slice_size = len(img_list) // n
    remainder = len(img_list) % n
    result = []
    iterater = iter(img_list)

    for i in range(n):
        result.append([])
        for j in range(slice_size):
            result[i].append(next(iterater))
        if remainder:
            result[i].append(next(iterater))
            remainder -= 1

    return result


def spawn_threads():
    # change directories if it already isn't in frames
    if not '/frames' in os.getcwd():
        os.chdir('frames')

    q = queue.Queue()
    num_threads = args.threads

    # get a distributed list of images for the threads
    images = distribute_frame_lists(num_threads)

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=get_image_colors, args=(i, q, images[i]))
        threads.append(thread)

    print('Generating frame colors...')
    for thread in threads:
        thread.daemon = True
        thread.start()

    thread_results = [None] * num_threads
    for i in range(num_threads):
        result = q.get()
        thread_results[result[0]] = result[1]

    # return to the original directory
    os.chdir('..')

    return [item for sublist in thread_results for item in sublist]


def create_barcode(colors, bar_width, height, width, fname):
    barcode_width = len(colors) * bar_width
    bc = Image.new('RGB', (barcode_width, height))
    draw = ImageDraw.Draw(bc)

    posx = 0
    print('Creating barcode...')
    for color in colors:
        draw.rectangle([posx, 0, posx + bar_width, height], fill=color)
        posx += bar_width

    del draw

    bc = bc.resize((width, height), Image.ANTIALIAS)
    bc.save(fname, 'PNG')


def main():
    try:
        # attempt to create the directory structure if it doesn't exist
        os.mkdir('frames')
    except OSError:
        pass

    if not args.noframes and not args.framecolors:
        create_movie_frames(args.infile)

    if not args.framecolors:
        colors = spawn_threads()

        with open('frame_colors.txt', 'w') as f:
            f.write('\n'.join('(%i, %i, %i, %i)' % x for x in colors))
    else:
        with open('frame_colors.txt', 'r') as f:
            colors = [ast.literal_eval(line) for line in f]

    create_barcode(colors, args.barwidth, args.height, args.width, args.outfile)

    if not args.nodelete:
        print('Cleaning up...')
        shutil.rmtree('frames')


if __name__ == '__main__':
    main()
