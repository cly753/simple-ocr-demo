#!/bin/sh
exit(0)

# build the image
# save to repo cly753
# as name python_ocr_dev_env
# with not tag
# use the Dockerfile from . (current dir)
# and Remove intermediate containers after a successful build
docker build --rm -t cly753/ocr_dev_env .

# to verify opencv install
docker run cly753/ocr_dev_env

# push the image to docker hub
docker push cly753/ocr_dev_env
