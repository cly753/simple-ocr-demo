#!/usr/bin/env bash
exit(0)

g++ -std=c++11 main.cpp -I/usr/local/include -L/usr/local/lib
# or 
# pkg-config is at /usr/local/lib/pkgconfig/opencv.pc
# delete -lippicv in pkg-config opencv.pc
g++ -std=c++11 main.cpp `pkg-config --libs opencv`

# code
# http://stackoverflow.com/questions/23506105/extracting-text-opencv
