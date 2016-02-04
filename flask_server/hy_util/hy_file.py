import os

import time


def save_byte(b, tag='', ext='jpg'):
    dest = get_file_name(tag, ext)
    with open(dest, 'wb') as f:
        f.write(b)

    return True


def get_file_name(tag='', ext='jpg'):
    return '/flask_server/temporary_file/{}_{}.{}'.format(time.strftime("%m-%d_%H.%M.%S"), tag, ext)
