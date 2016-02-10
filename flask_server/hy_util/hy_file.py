import os
import os.path

import time

BASE_PATH = '/flask_server/temporary_file'


def save_byte(b, tag='', ext='jpg'):
    dest = get_file_name(tag, ext)
    with open(dest, 'wb') as f:
        f.write(b)

    return True


def get_file_name(tag='', ext='jpg'):
    return '{}/{}_{}.{}'.format(BASE_PATH, time.strftime("%m-%d_%H.%M.%S"), tag, ext)
