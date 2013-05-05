#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'nikolajus krauklis <nikolajus@gmail.com>'

import os
import sys
from optparse import OptionParser
import time

import cv2

from pedestrian_lib import *


usage = "usage: %prog [options] pictures.txt"
parser = OptionParser(usage=usage, version="%prog 1.0.1")

parser.add_option("-d", "--debug", action="store_true",
                  help="show debugging window and do not create blob files", default=False)
parser.add_option("-v", "--verbose", action="store_true", default=False,
                  help="show more information in stdout")
parser.add_option("-c", "--classifier", default="haar_classifier.xml",
                  help="classifier file name. default: haar_classifier.xml")
parser.add_option("-l", "--debug-level", default=1, dest="debug_level")

(options, args) = parser.parse_args()

DEBUG = options.debug
DEBUG_LEVEL = options.debug_level
VERBOSE = options.verbose


def process(images, cascade):
    for image in images:
        started_process = time.time()

        if os.path.exists(image):
            cv_image = cv2.imread(image)
        else:
            if VERBOSE:
                print "image file '{0}' does not exists. skipping...".format(image)
            continue

        haar_objects = detect_objects(cv_image, cascade)
        color_blobs = detect_blobs(cv_image, DEBUG, DEBUG_LEVEL)
        final_blobs = []

        for haar_object in haar_objects:
            found = False
            for color_blob in color_blobs:
                if is_overlapping(haar_object, color_blob):
                    found = True
                    break
            if found:
                final_blobs.append(haar_object)

        elapsed_time = time.time() - started_process

        if VERBOSE:
            print "{0} pedestrian traffic signs found in image '{1}' in {2}s".format(len(final_blobs), image,
                                                                                     elapsed_time)
            print final_blobs

        if not DEBUG:
            save_found_blobs(image, final_blobs)
        else:
            show_blobs(cv_image, final_blobs)


if __name__ == '__main__':
    if len(args) == 0 or not os.path.exists(args[0]):
        print_usage()
        parser.print_help()
        sys.exit(-1)

    file_name = args[0]
    classifier_filename = options.classifier

    images = read_image_list(file_name)

    if not os.path.exists(classifier_filename):
        print "Classifier file does not exist"
        parser.print_help()
        sys.exit(-1)

    cascade = cv2.CascadeClassifier(classifier_filename)

    process(images, cascade)
