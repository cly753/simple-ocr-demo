import sys

import numpy as np
import cv2
import os
import os.path

import time

from hy.hy_cv import preprocess, sharpen_image, black_white
from hy.hy_tesseract import tesseract_detect
from hy_util.hy_file import BASE_PATH, get_file_name


def ocr_mat(imcv):
    # (save to disk) / (load cpp binary)
    time_string = time.strftime("%m-%d_%H.%M.%S")
    img_in = '{}/{}_img_in.jpg'.format(BASE_PATH, time_string)
    dir_out = '{}/{}_output/'.format(BASE_PATH, time_string)
    print 'img_in : {}'.format(img_in)
    print 'dir_out: {}'.format(dir_out)
    if not os.path.exists(dir_out):
        os.makedirs(dir_out)

    cv2.imwrite(img_in, imcv)

    # invoke cpp to split image
    invoke_cpp(img_in, dir_out)

    # ocr each sub image
    fs = [os.path.join(dir_out, f) for f in os.listdir(dir_out) if os.path.isfile(os.path.join(dir_out, f))]

    from pprint import pprint
    pprint([f for f in fs if f[-4:] != '.txt'], width=-1)
    pprint([f for f in fs if f[-4:] == '.txt'], width=-1)
    sys.stdout.flush()

    subimg = [cv2.imread(f, flags=1) for f in fs if f[-4:] != '.txt']
    subtext = [tesseract_detect(preprocess(imcv=img)) for img in subimg]
    subrect = read_rect([f for f in fs if f[-4:] == '.txt'])

    # assemble return data (xy+ocr of sub images) in json
    result = []
    for idx in range(0, len(subimg)):
        result.append({
            'rect': subrect[idx],
            'text': subtext[idx]
        })

    from pprint import pprint
    pprint(result, width=-1)
    sys.stdout.flush()
    return result


def ocr_byte(b):
    return ocr_mat(byte_to_imcv((b)))


def byte_to_imcv(b, flags=1):
    img_array = np.asarray(bytearray(b), dtype=np.uint8)
    imcv = cv2.imdecode(img_array, flags=flags)  # >0 3-channel color image. =0 grayscale image. <0 load image as is (with alpha channel).
    return imcv


def invoke_cpp(img_in, dir_out):
    if img_in is None or dir_out is None:
        raise Exception

    import subprocess

    CPP_BINARY = '/flask_server/hy_cpp/a.out'
    subprocess.call([CPP_BINARY, img_in, dir_out])  # blocking


def read_rect(fs):
    #
    # file format:
    # x y width height
    # "x y width height"
    #
    # see hy_cpp/main.cpp
    #

    ret = []
    for fname in fs:
        with open(fname, 'r') as f:
            x, y, width, height = [int(x) for x in f.readline().split()]
            ret.append({
                'x': x,
                'y': y,
                'width': width,
                'height': height
            })
    return ret


def tesseract_test(b):
    imcv = byte_to_imcv(b)
    print type(imcv), imcv.shape

    imcv_sharpen = sharpen_image(imcv)
    imcv_bw = black_white(im_gray=byte_to_imcv(b, 0))
    imcv_bw = cv2.cvtColor(imcv_bw, cv2.COLOR_GRAY2RGB)
    cv2.imwrite(get_file_name(tag='opencv', ext='jpg'), imcv)
    cv2.imwrite(get_file_name(tag='opencv_sharpen', ext='jpg'), imcv_sharpen)
    cv2.imwrite(get_file_name(tag='opencv_bw', ext='jpg'), imcv_bw)

    text_sharpen = tesseract_detect(imcv_sharpen)
    text_bw = tesseract_detect(imcv_bw)  # low accuracy
    print "----text sharpen----\n" + text_sharpen
    print "----text bw     ----\n" + text_bw
    sys.stdout.flush()

    return [('cpp text sharpen', text_sharpen), ('cpp text bw', text_bw)]


if __name__ == '__main__':
    from pprint import pprint

    dir = '/Users/cly/Dropbox/code/fyp/ocr/my_python_ocr/flask_server/hy_cpp/output'
    fs = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f[-4:] != '.txt']
    pprint(fs)
