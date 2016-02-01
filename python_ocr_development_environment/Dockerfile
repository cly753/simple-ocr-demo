# https://realpython.com/blog/python/setting-up-a-simple-ocr-server/
# start with a base image
FROM ubuntu:14.04

# install dependencies
RUN apt-get update
RUN apt-get install -y autoconf automake libtool
RUN apt-get install -y libpng12-dev
RUN apt-get install -y libjpeg62-dev
RUN apt-get install -y g++
RUN apt-get install -y libtiff4-dev
RUN apt-get install -y libopencv-dev libtesseract-dev
RUN apt-get install -y git
RUN apt-get install -y cmake
RUN apt-get install -y build-essential
RUN apt-get install -y libleptonica-dev
RUN apt-get install -y liblog4cplus-dev
RUN apt-get install -y libcurl3-dev
RUN apt-get install -y python2.7-dev
RUN apt-get install -y tk8.5 tcl8.5 tk8.5-dev tcl8.5-dev
RUN apt-get build-dep -y python-imaging --fix-missing
RUN apt-get install -y imagemagick
RUN apt-get install -y wget
RUN apt-get install -y python python-pip

# build leptonica
RUN wget http://www.leptonica.org/source/leptonica-1.70.tar.gz
RUN tar -zxvf leptonica-1.70.tar.gz
WORKDIR leptonica-1.70/
RUN ./autobuild
RUN ./configure
RUN make
RUN make install
RUN ldconfig
WORKDIR /

COPY requirements.txt /
RUN pip install -r requirements.txt

# build tesseract
RUN wget https://tesseract-ocr.googlecode.com/files/tesseract-ocr-3.02.02.tar.gz
RUN tar -zxvf tesseract-ocr-3.02.02.tar.gz
WORKDIR tesseract-ocr/
RUN ./autogen.sh
RUN ./configure
RUN make
RUN make install
RUN ldconfig
WORKDIR /

# download the relevant Tesseract English Language Packages
RUN wget https://tesseract-ocr.googlecode.com/files/tesseract-ocr-3.02.eng.tar.gz
RUN tar -xf tesseract-ocr-3.02.eng.tar.gz
RUN sudo cp -r tesseract-ocr/tessdata /usr/local/share/



# python opencv
# http://docs.opencv.org/3.0-beta/doc/tutorials/introduction/linux_install/linux_install.html
# http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/
RUN apt-get install -y build-essential
RUN apt-get install -y cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
RUN apt-get install -y python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
WORKDIR /
RUN git clone https://github.com/Itseez/opencv_contrib.git
WORKDIR /opencv_contrib
RUN git checkout 3.1.0
WORKDIR /
RUN git clone https://github.com/Itseez/opencv.git
WORKDIR /opencv
RUN mkdir build
WORKDIR /opencv/build
RUN git checkout 3.1.0
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_C_EXAMPLES=OFF \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib/modules \
	-D BUILD_EXAMPLES=ON ..
RUN make -j4
RUN make install
RUN ldconfig

WORKDIR /
CMD ["python", "-c", "import cv2; print('cv2.__version__ = ' + str(cv2.__version__))"]
