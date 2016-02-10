import numpy as np

import cv2


def preprocess(imcv):
    return sharpen_image(imcv)


def sharpen_image(imcv):
    # http://www.cc.gatech.edu/classes/AY2015/cs4475_summer/documents/sharpen.py
    kernel = np.zeros((9, 9), np.float32)
    kernel[4, 4] = 3.0  # Identity, times two!

    # Create a box filter:
    box_filter = np.ones((9, 9), np.float32) / 81.0

    # Subtract the two:
    kernel = kernel - box_filter

    # Note that we are subject to overflow and underflow here...but I believe that
    # filter2D clips top and bottom ranges on the output, plus you'd need a
    # very bright or very dark pixel surrounded by the opposite type.
    imcv_sharpen = cv2.filter2D(imcv, -1, kernel)
    return imcv_sharpen


def black_white(im_gray):
    im_gray = cv2.medianBlur(im_gray, 5)
    imcv_bw = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return imcv_bw