blue pedestrian crossing sign detection
=========================

idea is to develop algorithm to detect EU pedestrian crossing signs (blue)
in images or stream.

pipepline
==

1. detect blue blobs in images by converting image to HLS and extracting tresholded blue color
2. exclude smaller and bigger blobs by ration on blob area with image area
3. exclude blobs which aspect ratio is more than .49 and 1.49
4. detect object with haar like features trained on traffic sign (with min neighbours 2)
5. check for intersected blobs and haar objects (those are what we interested in)

requirements
==

python >2.7, opencv >2.*, python-opencv, numpy
