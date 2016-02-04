import ctypes
from StringIO import StringIO

import cv2
import sys

import numpy as np

from hy_util.hy_file import get_file_name


def byte_to_imcv(b, flags=1):
    img_array = np.asarray(bytearray(b), dtype=np.uint8)
    imcv = cv2.imdecode(img_array, flags=flags)  # >0 3-channel color image. =0 grayscale image. <0 load image as is (with alpha channel).
    return imcv


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


def black_white(b):
    im_gray = byte_to_imcv(b, 0)
    im_gray = cv2.medianBlur(im_gray, 5)
    imcv_bw = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return imcv_bw


def tesseract_detect(imcv):
    libtesseract_path = '/usr/local/lib/libtesseract.so.3'
    tesseract = ctypes.CDLL(libtesseract_path)

    class _TessBaseAPI(ctypes.Structure):
        pass

    TessBaseAPI = ctypes.POINTER(_TessBaseAPI)

    tesseract.TessBaseAPICreate.restype = TessBaseAPI

    tesseract.TessBaseAPIDelete.restype = None  # void
    tesseract.TessBaseAPIDelete.argtypes = [TessBaseAPI]

    tesseract.TessBaseAPIInit3.argtypes = [TessBaseAPI,
                                           ctypes.c_char_p,
                                           ctypes.c_char_p]

    tesseract.TessBaseAPISetImage.restype = None
    tesseract.TessBaseAPISetImage.argtypes = [TessBaseAPI,
                                              ctypes.c_void_p,
                                              ctypes.c_int,
                                              ctypes.c_int,
                                              ctypes.c_int,
                                              ctypes.c_int]

    tesseract.TessBaseAPIGetUTF8Text.restype = ctypes.c_char_p
    tesseract.TessBaseAPIGetUTF8Text.argtypes = [TessBaseAPI]

    api = tesseract.TessBaseAPICreate()
    rc = tesseract.TessBaseAPIInit3(api, '', 'eng')
    if rc:
        tesseract.TessBaseAPIDelete(api)
        raise RuntimeError('tesseract init failed')

    h, w, d = imcv.shape
    tesseract.TessBaseAPISetImage(api, imcv.ctypes, w, h, d, w * d)
    text = tesseract.TessBaseAPIGetUTF8Text(api)
    return text.strip()
    # return text.strip().decode('utf-8')


def tesseract_test(b):
    imcv = byte_to_imcv(b)
    print type(imcv), imcv.shape

    imcv_sharpen = sharpen_image(imcv)
    imcv_bw = black_white(b)
    imcv_bw = cv2.cvtColor(imcv_bw , cv2.COLOR_GRAY2RGB)
    cv2.imwrite(get_file_name(tag='opencv', ext='jpg'), imcv)
    cv2.imwrite(get_file_name(tag='opencv_sharpen', ext='jpg'), imcv_sharpen)
    cv2.imwrite(get_file_name(tag='opencv_bw', ext='jpg'), imcv_bw)

    text_sharpen = tesseract_detect(imcv_sharpen)
    text_bw = tesseract_detect(imcv_bw)
    print "----text sharpen----\n" + text_sharpen
    print "----text bw     ----\n" + text_bw
    sys.stdout.flush()
