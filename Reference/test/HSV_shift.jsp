//reference:https://answers.opencv.org/question/178766/adjust-hue-and-saturation-like-photoshop/
#include <opencv2/opencv.hpp>
using namespace cv;
#pragma comment(lib, "opencv_world331.lib")

#include <iostream>
using namespace std;


int int_hue = 180;
int int_saturation = 100;
int int_value = 100;

Mat frame = imread("puppets.png");


static void on_trackbar(int, void*)
{
    frame = imread("puppets.png");

    Mat hsv;
    cvtColor(frame, hsv, CV_BGR2HSV);
    signed short hue_shift = (int_hue - 180) / 2;

    for (int j = 0; j < frame.rows; j++)
    {
        for (int i = 0; i < frame.cols; i++)
        {
            signed short h = hsv.at<Vec3b>(j, i)[0];
            signed short h_plus_shift = h;
            h_plus_shift += hue_shift;

            if (h_plus_shift < 0)
                h = 180 + h_plus_shift;
            else if (h_plus_shift > 180)
                h = h_plus_shift - 180;
            else
                h = h_plus_shift;

            hsv.at<Vec3b>(j, i)[0] = static_cast<unsigned char>(h);

            double s = hsv.at<Vec3b>(j, i)[1];
            double s_shift = (int_saturation - 100) / 100.0;
            double s_plus_shift = s + 255.0*s_shift;

            if (s_plus_shift < 0)
                s_plus_shift = 0;
            else if (s_plus_shift > 255)
                s_plus_shift = 255;

            hsv.at<Vec3b>(j, i)[1] = static_cast<unsigned char>(s_plus_shift);


            double v = hsv.at<Vec3b>(j, i)[2];
            double v_shift = (int_value - 100) / 100.0;
            double v_plus_shift = v + 255.0 * v_shift;

            if (v_plus_shift < 0)
                v_plus_shift = 0;
            else if (v_plus_shift > 255)
                v_plus_shift = 255;

            hsv.at<Vec3b>(j, i)[2] = static_cast<unsigned char>(v_plus_shift);
        }
    }

    cvtColor(hsv, frame, CV_HSV2BGR);

    imshow("frame", frame);
}


int main(void)
{
    imshow("frame", frame);

    createTrackbar("Hue", "frame", &int_hue, 360, on_trackbar);
    createTrackbar("Saturation", "frame", &int_saturation, 200, on_trackbar);
    createTrackbar("Value", "frame", &int_value, 200, on_trackbar);
    on_trackbar(0, 0);

    waitKey(0);

    destroyAllWindows();

    return 0;
}