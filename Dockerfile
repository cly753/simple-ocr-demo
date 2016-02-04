# start with a base image
# FROM cly753/ocr_dev_env
FROM lushl9301/ocr_dev_env

# change working directory to /flask_server
WORKDIR /flask_server

CMD ["python", "app.py"]
