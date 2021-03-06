import json
import os
import pprint
import re
import sys
from base64 import b64encode

import flask
from flask import Flask, request, jsonify, render_template

import hy.hy_ocr
from hy.hy_ocr import byte_to_imcv, ocr_mat, tesseract_test
from hy_util.hy_file import save_byte
from ocr import process_image_byte, process_image

app = Flask(__name__)
_VERSION = 1  # API version


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/v{}/ocr'.format(_VERSION), methods=["POST"])
def ocr():
    try:
        url = request.json['image_url']
        if 'jpg' in url:
            output = process_image(url)
            return jsonify({"output": output})
        else:
            return jsonify({"error": "only .jpg files, please"})
    except:
        return jsonify(
                {"error": "Did you mean to send: {'image_url': 'some_jpeg_url'}"}
        )


@app.route('/v{}/upload'.format(_VERSION), methods=['GET'])
def upload():
    return render_template('upload.html')


@app.route('/v{}/upload'.format(_VERSION), methods=['POST'])
def ocr_byte():
    # print(request.headers)
    # print(request.data)
    data = request.files['image']
    b = data.read()

    dest = save_byte(b, tag='origin', ext='jpg')
    result = []
    result.append(('pytesseract + pillow', process_image_byte(b)))
    result.extend(tesseract_test(b))

    temp = hy.hy_ocr.ocr_byte(b)
    temp_text = '\n'.join([t['text'] for t in temp])
    temp_tag = 'cpp tesseract + cpp extraction morphological gradient filter + opencv sharpen'
    result.append((temp_tag, temp_text))

    text = ''
    for each in result:
        text += '---- result ----\n{}\n----------------\n{}\n\n'.format(each[0], each[1])

    final = text
    # final = {
    #     'n_rect': len(temp),
    #     'rect': temp
    # }
    # final = json.dumps(final, indent=4)
    # return flask.jsonify(**final)

    print(final)
    final = ''.join([i if ord(i) < 128 else '' for i in final])
    # final = re.sub('[^0-9A-Za-z#&()+,\-./:;<=>@[\\\]\^_\{\|\}\~\n ]', '', final)
    return render_template('result.html', image=b64encode(b), result=final)


@app.errorhandler(500)
def internal_error(error):
    return str(error)


@app.errorhandler(404)
def not_found_error(error):
    return str(error)


# # what?
# if not app.debug:
#     file_handler = FileHandler('error.log')
#     file_handler.setFormatter(
#         Formatter('%(asctime)s %(levelname)s: \
#             %(message)s [in %(pathname)s:%(lineno)d]')
#     )
#     app.logger.setLevel(logging.INFO)
#     file_handler.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)
#     app.logger.info('errors')


if __name__ == '__main__':
    import cv2

    print('cv2.__version__ = ' + str(cv2.__version__))
    sys.stdout.flush()

    debug = True
    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug, host=host, port=port)
