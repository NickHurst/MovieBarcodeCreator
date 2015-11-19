Python Movie Barcode Creator
=============================

This is a simple script to create "barcodes" from frames of a movie. This works by using ffmpeg to create images from the frames of the video. Then uses [Pillow](https://github.com/python-pillow/Pillow) to extract the dominant color from each frame and then string them together into a "barcode."

Installation:
-------------

Before you install moviebarcode creator, you will need to install ffmpeg. FFmpeg can be downloaded [here](https://www.ffmpeg.org/download.html). Or you can install it with your favorite package manager:

    sudo apt-get install ffmpeg
    brew install ffmpeg

*Note: If you are having troubles getting it to run on Windows because of FFMpeg install issues [see this wiki page](https://github.com/TheNickHurst/MovieBarcodeCreator/wiki/Windows-FFMpeg-Install) for a guide to setting it up*

This script can be installed via pip (either python2 or 3):

    pip install moviebarcodecreator

This will also install all dependencies. Or you can install it manually via:

    python setup.py install

Usage:
------

From the command line, go to the directory the video file is in and type:

    moviebarcode VideoFileName.mpg

And a barcode.png file will be generated, as well as a frame_colors.txt file for faster barcode generation if you ever want to change the size in the future.

###Options:

#####-o, --outfile OUTFILENAME               

Name of the generated barcode png. Default is barcode.

####-h, --help

Display the help information.

####-im, -images

Use this command if you want it to make a barcode from the frames themselves instead of the colors.

####-fc, --framecolors

Use this if your already have a frame_colors.txt generated to skip frame and color generation. (Can't be used at the same time as -nf).

####-nf, --noframes

Use this if you already have the movie frames inside a frames directory inside the video directory. This will skip the frame generation process. (Can't be used at the same time as -fc).

*Note: With both -fc and -nf you do not have to specify a video file name if either are used.*

####-nd, --nodelete

The default behavior for the script is to delete all the frames it generates when it's done. Add this -nd flag and the frames directory and all the frames won't be deleted.

####-ht, --height HEIGHT

Set the image height in pixels. Default is 1200px.

####-bw, --barwidth BARWIDTH

Set the width of each bar, before the image get's resized to its final width. Default is 5px.

####-w, --width WIDTH

Set the final width of the barcode in pixels. Default is 1920px.

####-fr, --framerate FRAMERATE

You can set FFMPEG's frame rate with this. Default is 1/24 (1 frame every 24 seconds). Keep in mind, the higher you set the framerate (e.g. setting it to 24 will capture 24 frames per second the average fps for a movie), the more frames are going to be generated and the longer the process will take.

####-ss, --start START

You can set the point you want ffmpeg to start cutting the video into frames.
Format: 01:08:45.000 or 109 (seconds).

####-d, --duration DURATION

You can set how long you want ffmpeg to cut the video into frames.
Format: 01:08:45.000 or 109 (seconds).

####-en, --end END

You can set the point you want ffmpeg to stop cutting the video into frames.
Format: 01:08:45.000 or 109 (seconds).

####-t, --threads THREADS

You can set the amount of threads python will use when generating the colors for the barcode. Default is 8.

------------------------------

####Generate a barcode for a video that is 500x500 without deleting the frames:

    moviebarcode VideoFileName.avi -ht 500 -w 500 -nd

####Generate a barcode from previously generated frames and name the barcode test.png:

    moviebarcode -nf -o test.png

####Generate a barcode from previously generated frame colors:

    moviebarcode -fc

####Generate a barcode with a higher framerate and more threads:

    moviebarcode VideoFileName.mkv -fr 1/2 -t 16

####Start the video at 1 hour and 28 minutes and stop after 30 minutes

    moviebarcode VideoFileName.mp4 -ss 01:28:00.00 -d 00:30:00.00

####End the video at the 45 minute mark

    moviebarcode VideoFileName.mp4 -en 2700

####Make a barcode from the images of the frames, instead of the colors

    moviebarcode VideoFileName.mpg -im

Examples:
---------

These examples were generated with (unless noted otherwise):

    moviebarcode VideoFile -ht 500 -w 2000

####Interstellar

![Interstellar Barcode](http://i.imgur.com/4JIqc3q.png)

####500 Days of Summer

![500 Days of Summer](http://i.imgur.com/JNlmwLc.png)

####Mad Max: Fury Road

![Mad Max: Fury Road](http://i.imgur.com/h6qKY7B.png)

####A Goofy Movie 

*Default framerate*

![Goofy Movie Default](http://i.imgur.com/WWLiUCc.png)

####A Goofy Movie 

*higher framerate (1/2)*

![Goofy Movie Higher](http://i.imgur.com/zIejkfA.png)

####Rick and Morty: The Wedding Squanchers

`moviebarcode VideoName -im -fr 1 -w 8000 -bw 640 -ht 2000`

![Rick and Morty](http://i.imgur.com/mCAWrKs.jpg)

