import os
import logging
from logging import Formatter, FileHandler
from flask import Flask, request, jsonify, render_template

from hy_util.hy_file import save_byte
from ocr import process_image

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
    print(request.headers)
    print(request.data)
    data = request.files['image']
    b = data.read()

    # dest = '/temp_file/x.jpg'
    dest = '/flask_server/temp_img/x.jpg'
    save_byte(b, dest=dest)

    return 'ok'


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
    debug = True
    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug, host=host, port=port)
