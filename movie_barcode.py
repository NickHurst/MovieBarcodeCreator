#!/usr/bin/env python3

import shutil
import argparse
import subprocess
import os, os.path
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str, help='movie filename')
parser.add_argument('-bw', '--barwidth', type=int, 
                    help='Set the width of the bars in the barcode. Default is 5px.')
parser.add_argument('-ht', '--height', type=int,
                    help='Set the height of the barcode. Default is 1200px.')
parser.add_argument('-w', '--width', type=int,
                    help='Set the final width of the barcode. Default is 1920px.')
parser.add_argument('-nd', '--nodelete', action='store_true',
                    help='Won\'t delete the movie frames after done executing.')
parser.add_argument('-nf', '--noframes', action='store_true',
                    help='Won\'t create the frames. Must already have them in a directory called frames.')
parser.add_argument('-fr', '--framerate', type=int,
                    help='Set the framerate for breaking the movie into frames. Default is 25.')
args = parser.parse_args()


def create_movie_frames(infile):
    os.chdir('./frames')

    ffmpeg_args = ['ffmpeg', '-i', '../' + infile, '-f', 'image2', 'image-%07d.png']

    if args.framerate:
        ffmpeg_args += ['-r', framerate]

    output = open('ffmpeg_log.txt', 'w')

    print('Creating frames (this will take a while)...')
    subprocess.run(ffmpeg_args, stderr=output, stdout=subprocess.PIPE)

    output.close()


def find_frame_bar_color(infile, last_col=None):
    img = Image.open(infile)
    result = img.convert('P', palette=Image.ADAPTIVE)
    result.putalpha(0)
    colors = result.getcolors()

    if last_col == colors[0][1]:
        return last_col

    return colors[0][1]


def get_image_colors():
    colors = []
    last_col = None
    print('Getting frame colors (this could take a while)...')
    for img in os.listdir(os.getcwd()):
        if img.endswith('.png'):
            last_col = find_frame_bar_color(img, last_col=last_col)

            if not colors:
                colors.append(last_col)
            elif colors[-1] != last_col:
                colors.append(last_col)

    # return back to the original directory
    os.chdir('..')

    return colors


def create_barcode(colors, bar_width=5, height=1200, width=1920):
    barcode_width = len(colors) + bar_width
    bc = Image.new('RGB', (barcode_width, height))
    draw = ImageDraw.Draw(bc)

    posx = 0

    print('Creating barcode...')
    for color in colors:
        draw.rectangle([posx, 0, posx + bar_width, height], fill=color)
        posx += bar_width

    del draw

    bc.resize((width, height))
    bc.save('barcode.png', 'PNG')


def main():
    try:
        # attempt to create the directory structure if it doesn't exist
        os.mkdir('frames')
    except FileExistsError:
        pass

    fname = args.filename
    bar_width=5
    height=1200
    width=1920

    if args.barwidth: bar_width = args.barwidth
    if args.height: bar_height = args.height
    if args.width: width = args.width

    if not args.noframes:
        create_movie_frames(fname)

    colors = get_image_colors()
    create_barcode(colors, bar_width=bar_width, height=height, width=width)

    if not args.nodelete:
        print('Cleaning up...')
        shutil.rmtree('frames')


if __name__ == '__main__':
    main()