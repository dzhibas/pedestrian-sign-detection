#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'nikolajus krauklis <nikolajus@gmail.com>'

import cv2
import numpy as np


B_HUE_MAX = 163
B_HUE_MIN = 100
B_SAT_MIN = 39


class Rect:
    """
        instead of opencv blobs which is described as
        x, y, width, height we use rectangle with coordinates top left x1,y1, and bottom right x2,y2
    """

    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h


def print_usage():
    """Prints usage
    """
    print "please enter text filename with images listed inside\n" \
          "to create one you can use something like\n\n" \
          "ls data/*|grep -i -P (jpg|png)$ > pictures.txt\n"


def read_image_list(images_filename):
    """Reads file and content inside. Expects filename in each line

    images_filename[in]         filename
    verbose[in]                 show or not notices about missing files
    """
    f = open(images_filename, "r")
    file_lines = f.readlines()
    f.close()

    all_files = []

    for file_name in file_lines:
        all_files.append(file_name.strip())

    return all_files


def detect_objects(image, cascade):
    """detect objects in image using haar features, cascade

    image[in] numpy matrix
    cascade[in]

    return array of blobs
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=2,
                                     minSize=(20, 20), flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []

    rects[:, 2:] += rects[:, :2]

    as_blobs = []
    for rect in rects:
        as_blobs.append((rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]))

    return as_blobs


def detect_blobs(image, debug=False, debug_level=1):
    """detect blue blobs in image

    :param image:
    """
    found_blobs = []

    BLUE_MIN = np.array([B_HUE_MIN, 0, B_SAT_MIN], np.uint8)
    BLUE_MAX = np.array([B_HUE_MAX, 255, 255], np.uint8)

    hls_img = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    tresholded_im = cv2.inRange(hls_img, BLUE_MIN, BLUE_MAX)

    contours, h = cv2.findContours(tresholded_im, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    image_width, image_height = tresholded_im.shape
    image_area = image_width * image_height

    for cnt in contours:
        convex = cv2.convexHull(cnt)
        (x, y, w, h) = cv2.boundingRect(convex)
        ratio = float(w) / h
        area = w * h

        if ratio >= 0.49 and ratio <= 1.49:
            #if (float(area)/image_area) > 1./2e4 and
            if (float(area) / image_area) < 1. / 20:
                found_blobs.append((x, y, w, h))
                if debug and debug_level > 1:
                    cv2.drawContours(hls_img, [convex], 0, (255, 255, 255), -1)

    if debug and debug_level > 1:
        cv2.imshow('hls', resized_image(hls_img))

    return found_blobs


def is_overlapping(blobA, blobB):
    """
    returns true if two blobs overaps

    :param blobA:
    :param blobB:
    :return: boolean
    """
    (x1, y1, w1, h1) = blobA
    rectA = Rect(x1, y1, w1, h1)
    (x2, y2, w2, h2) = blobB
    rectB = Rect(x2, y2, w2, h2)
    return rectA.x1 < rectB.x2 and rectA.x2 > rectB.x1 and rectA.y1 < rectB.y2 and rectA.y2 > rectB.y1


def save_found_blobs(image_filename, blobs):
    """save descriptor file next to image if blobs is not empty

    if image file was: 'image.jpg', descriptor file 'image.jpg.txt' is created
    with content of blobs found

    :param image_filename:
    :param blobs:
    """

    if len(blobs) == 0:
        return

    descriptor = image_filename + ".txt"
    f = open(descriptor, "w+")
    for blob in blobs:
        x, y, width, height = blob
        f.write("%d %d %d %d\n" % (x, y, width, height))
    f.close()


def resized_image(im, how_much_smaller=3):
    """resizes image matrix "how_much_smaller" times

    :param im:
    :param how_much_smaller:
    :return:
    """
    if len(im.shape) > 2:
        rows, cols, tmp = im.shape
    else:
        rows, cols = im.shape
    return cv2.resize(im, (cols / how_much_smaller, rows / how_much_smaller))


def draw_blobs(img, blobs, color=(0, 255, 0), line_size=2):
    """ draws blob minimal rectangle fit in preferred color on image

    :param img:
    :param blobs:
    :param color:
    :param line_size:
    :return:
    """
    for blob in blobs:
        x1, y1, w1, h1 = blob
        cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), color, line_size)
    return img


def show_blobs(image, blobs):
    """shows found blobs in image (debug mode)

    :param image:
    :param blobs:
    """
    image = draw_blobs(image, blobs, (0, 255, 0), 2)
    cv2.imshow('debug_image', resized_image(image))
    print "press [space] or any other key to process next image (focus image itself)"
    cv2.waitKey()
