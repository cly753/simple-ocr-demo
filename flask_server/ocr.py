import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO


def process_image_byte(b):
    image = Image.open(StringIO(b))
    image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image)


def process_image(url):
    image = _get_image(url)
    image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image)


def _get_image(url):
    return Image.open(StringIO(requests.get(url).content))
