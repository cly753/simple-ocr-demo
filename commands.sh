#!/bin/sh

exit(0)

# fork and modified from
# https://realpython.com/blog/python/setting-up-a-simple-ocr-server/

# build the image
# save to repo cly753
# as name flask_ocr
# with not tag
# use the Dockerfile from . (current dir)
# and Remove intermediate containers after a successful build
docker build --rm -t cly753/flask_ocr .

# run (create and start) the container
# from repo cly753
# with name flask_ocr
# with not tag
# forward (?) port
# to host 5000
# from container 5000
# from the default network "bridge"
# and mount $(pwd)/flask_server to container /flask_server for flask to autoreload
docker run -v $(pwd)/flask_server:/flask_server -p 5000:5000 cly753/flask_ocr

# open a bash in the running container
docker exec -it [CONTAINER] bash

# show the docker-machine ip
# named default
docker-machine ip default

# go to http://[... docker-machine ip default ...]:5000
# test images
# https://www.realpython.com/images/blog_images/ocr/ocr.jpg
# https://www.realpython.com/images/blog_images/ocr/sample1.jpg
# https://www.realpython.com/images/blog_images/ocr/sample2.jpg
# https://www.realpython.com/images/blog_images/ocr/sample3.jpg
# https://www.realpython.com/images/blog_images/ocr/sample4.jpg
# https://www.realpython.com/images/blog_images/ocr/sample5.jpg

# push the image to docker hub
docker push cly753/flask_ocr

