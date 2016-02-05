# start with a base image
FROM cly753/ocr_opencv

# change working directory to /flask_server
WORKDIR /flask_server

CMD ["python", "app.py"]
