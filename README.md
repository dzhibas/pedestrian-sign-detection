blue pedestrian crossing sign detection
=========================

idea is to develop algorithm to detect EU pedestrian crossing signs (blue)
in images or stream.

requirements
==

python >2.7, opencv >2.*, python-opencv, numpy

install
==

1. In ubuntu linux

sudo apt-get update
sudo apt-get install libcv2.3 libcv-dev python-numpy python-opencv


usage
==
prepare file with picture filenames inside with help of command
    
    > ls data/*|grep -i -P (jpg|png)$ > pictures.txt

then run:

    > python detect_pedestrians.py 

help of detect_pedestrians.py
==

please enter text filename with images listed inside
to create one you can use something like

ls data/*|grep -i -P (jpg|png)$ > pictures.txt

Usage: detect_pedestrians.py [options] pictures.txt

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -d, --debug           show debugging window and do not create blob files
  -v, --verbose         show more information in stdout
  -c CLASSIFIER, --classifier=CLASSIFIER
                        classifier file name. default: haar_classifier.xml
  -l DEBUG_LEVEL, --debug-level=DEBUG_LEVEL

you can run program in debug mode to see detected objects in image,
if you increse level -l 2 you will even see blue blobs detected

with verbosity you can output more info into console

p.s.
debug mode is not creating descriptor files next to images

pipepline
==

1. detect blue blobs in images by converting image to HLS and extracting tresholded blue color
2. exclude smaller and bigger blobs by ratio of blob area with image area
3. exclude blobs which aspect ratio is more than .49 and less than 1.49
4. detect object with haar like features trained on traffic sign (with min neighbours 2)
5. check for intersected blobs and haar objects (those are what we interested in)
