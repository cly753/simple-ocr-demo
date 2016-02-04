#!/bin/sh
exit(0)

# build the image
# save to repo cly753
# as name ocr_opencv
# with not tag
# use the Dockerfile from . (current dir)
# and Remove intermediate containers after a successful build
# docker build --rm -t cly753/ocr_opencv .
# ！！！
# current Dockerfile are for DockerHub Continuous Build
# for local build, go through Dockerfile and change accordingly

# to verify opencv install
docker run cly753/ocr_opencv

# push the image to docker hub
# docker push cly753/ocr_opencv
