import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO

from hy_util.hy_file import get_file_name


def process_image_byte(b):
    image = Image.open(StringIO(b))
    image.save(get_file_name(tag='pillow', ext='jpg'))
    image.filter(ImageFilter.SHARPEN)
    image.save(get_file_name(tag='pillow_sharpen', ext='jpg'))
    return pytesseract.image_to_string(image)


def process_image(url):
    b = _get_byte(url)
    return process_image_byte(b)


def _get_byte(url):
    return requests.get(url).content
