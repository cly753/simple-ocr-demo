# start with a base image
FROM cly753/ocr_dev_env

# copy file from ./flask_server to image /flask_server
# COPY ./flask_server /flask_server

# change working directory to /flask_server
WORKDIR /flask_server

CMD ["python", "app.py"]
