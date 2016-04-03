# start with a base image
FROM cly753/ocr_opencv

# RUN apt-get install -y liblapacke-dev
# RUN apt-get install -y liblapack3
# RUN apt-get install -y libopenblas-base
# RUN apt-get install -y libopenblas-dev
# RUN ln /usr/lib/liblapack.so.3gf /usr/lib/liblapack.so
# RUN apt-get install -y gfortran
# RUN pip install scipy

# change working directory to /flask_server
WORKDIR /flask_server

CMD ["python", "app.py"]
