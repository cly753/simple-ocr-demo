// #include "stdafx.h"

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <stdio.h>
#include <iostream>
#include <fstream>

using namespace cv;
using namespace std;

// #define INPUT_FILE      string("/flask_server/hy_cpp/1.jpg")
// #define OUTPUT_PATH     string("/flask_server/hy_cpp")

vector<Rect> detectLetters(Mat& img) {
    vector<Rect> boundRect;
    Mat img_gray, img_sobel, img_threshold, element;
    cvtColor(img, img_gray, CV_BGR2GRAY);
    Sobel(img_gray, img_sobel, CV_8U, 1, 0, 3, 1, 0, BORDER_DEFAULT);
    threshold(img_sobel, img_threshold, 0, 255, CV_THRESH_OTSU+CV_THRESH_BINARY);
    element = getStructuringElement(MORPH_RECT, Size(30, 30));
    morphologyEx(img_threshold, img_threshold, CV_MOP_CLOSE, element); //Does the trick
    vector<vector<Point>> contours;
    findContours(img_threshold, contours, 0, 1);
    vector<vector<Point>> contours_poly(contours.size());

    Size size = img.size();
    for (int i = 0; i < contours.size(); i++) {
        if (contours[i].size() > 100) {
            approxPolyDP(Mat(contours[i]), contours_poly[i], 3, true);
            Rect appRect(boundingRect(Mat(contours_poly[i])));
            if (appRect.width > appRect.height) {
                appRect.width = min(size.width - appRect.x, appRect.width + 2);
                appRect.height = min(size.height - appRect.y, appRect.height + 2);
                boundRect.push_back(appRect);
            }
        }
    }
    return boundRect;
}

void sobel_filter(Mat& large, const string OUTPUT_PATH) {
    vector<Rect> letterBBoxes1 = detectLetters(large);
    for (int i = 0; i < letterBBoxes1.size(); i++)
        rectangle(large, letterBBoxes1[i], Scalar(0, 255, 0), 3, 8, 0);
    imwrite(OUTPUT_PATH + "image_out.jpg", large);
}

void morphological_gradient_filter(Mat& large, const string OUTPUT_PATH) {
    // Mat large = imread(INPUT_FILE);
    Mat large_out;
    large.copyTo(large_out);
    Size size_large = large.size();
    // printf("size large %dx%d\n", size_large.width, size_large.height);
    Mat rgb;
    // downsample and use it for processing
    pyrDown(large, rgb);
    Size size_rgb = rgb.size();
    // printf("size rgb   %dx%d\n", size_rgb.width, size_rgb.height);
    float ratio = size_large.height / (float)size_rgb.height;
    // printf("ratio = %f\n", ratio);
    // rgb = large;
    Mat small;
    cvtColor(rgb, small, CV_BGR2GRAY);
    // morphological gradient
    Mat grad;
    Mat morphKernel = getStructuringElement(MORPH_ELLIPSE, Size(3, 3));
    morphologyEx(small, grad, MORPH_GRADIENT, morphKernel);
    // binarize
    Mat bw;
    threshold(grad, bw, 0.0, 255.0, THRESH_BINARY | THRESH_OTSU);
    // connect horizontally oriented regions
    Mat connected;
    morphKernel = getStructuringElement(MORPH_RECT, Size(9, 1));
    morphologyEx(bw, connected, MORPH_CLOSE, morphKernel);
    // find contours
    Mat mask = Mat::zeros(bw.size(), CV_8UC1);
    vector<vector<Point>> contours;
    vector<Vec4i> hierarchy;
    findContours(connected, contours, hierarchy, CV_RETR_CCOMP, CV_CHAIN_APPROX_SIMPLE, Point(0, 0));
    // filter contours
    for(int idx = 0; idx >= 0; idx = hierarchy[idx][0]) {
        Rect rect = boundingRect(contours[idx]);
        Mat maskROI(mask, rect);
        maskROI = Scalar(0, 0, 0);
        // fill the contour
        drawContours(mask, contours, idx, Scalar(255, 255, 255), CV_FILLED);
        // ratio of non-zero pixels in the filled region
        double r = (double)countNonZero(maskROI)/(rect.width*rect.height);

        if (r > 0.45 /* assume at least 45% of the area is filled if it contains text */
            && 
            (rect.height > 8 && rect.width > 8) /* constraints on region size */
            /* these two conditions alone are not very robust. better to use something 
            like the number of significant peaks in a horizontal projection as a third condition */
            )
        {
            // origin
            // rectangle(rgb, rect, Scalar(0, 255, 0), 1);
            

            
            rect.x *= ratio;
            rect.y *= ratio;
            rect.width *= ratio;
            rect.height *= ratio;
            rect.width = min(size_large.width - rect.x, rect.width + 2);
            rect.height = min(size_large.height - rect.y, rect.height + 2);
            // printf("x=%4d, y=%4d, x+width=%4d, y+height=%4d\n", rect.x, rect.y, rect.x+rect.width, rect.y+rect.height);

            rectangle(large_out, rect, Scalar(0, 255, 0), 1);

            Mat sub;
            large(rect).copyTo(sub);
            imwrite(OUTPUT_PATH + to_string(idx) + ".jpg", sub);
            ofstream f(OUTPUT_PATH + to_string(idx) + ".txt");
            f << rect.x << " " << rect.y << " " << rect.width << " " << rect.height << "\n"
                << "x y width height" << "\n"
                << idx << "\n"
                << "index" << "\n";
            f.close();
        }
    }
    // origin
    // imwrite(OUTPUT_PATH, rgb);
    
    // imwrite(OUTPUT_PATH + "rgb.jpg", large_out);   
}


int main(int argc, char* argv[]) {
    for (int i = 0; i < argc; i++)
        printf("%s\n", argv[i]);
    assert(argc == 3);

    string INPUT_FILE(argv[1]);
    string OUTPUT_PATH(argv[2]);
    assert(OUTPUT_PATH[OUTPUT_PATH.length() - 1] == '/');
    
    Mat large = imread(INPUT_FILE);
    morphological_gradient_filter(large, OUTPUT_PATH);
    // sobel_filter(large, OUTPUT_PATH); // bad

    return 0;
}
