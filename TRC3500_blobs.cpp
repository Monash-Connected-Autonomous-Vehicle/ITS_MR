////////////////////////////////////////////////////////////////
// Skeleton program for TRC3500
// Grabs images from a USB camera using OpenCV
// Written by Andy Russell 09th February 2006
// Modified by Michael Curtis 2011-2012 - updated for newer OpenCV
/////////////////////////////////////////////////////////////////
#include "cv.h"
#include "highgui.h"
#include <iostream>
#include <stdio.h>

using namespace std;

////////////////////////////////////////////////////////////////
// main - initialises OpenCV and captures an image and changes it
////////////////////////////////////////////////////////////////
int main()
{
    CvCapture* capture = 0;
    IplImage* processedImage = 0;

    cout << "Andy's USB camera program" << endl << "Press 'q' to quit" << endl;

    // Initializes capturing video from camera
    capture = cvCaptureFromCAM(0);
    if (!capture) {
        fprintf(stderr, "Could not initialize capturing...\n");
        return -1;
    }


    // Creates window
    cvNamedWindow("Camera image", 1);

    // Camera image
    IplImage* frame = 0;

    // Grabs and returns a frame from camera
    frame = cvQueryFrame(capture);

    // Print details of image
    cout << "image width =" << frame->width << " height =" << frame->height;
    cout << " depth =" << frame->depth << " channels =" << frame->nChannels << endl;

    //Initializing threshold value
    int threshold = 255 / 2;


    do {
        // Grabs and returns a frame from camera
        frame = cvQueryFrame(capture);
        if (!frame) {
            break;
        }

        //Initialize moments
        double moment_00 = 0;
        double moment_10 = 0;
        double moment_01 = 0;
        double moment_11 = 0;
        double moment_20 = 0;
        double moment_02 = 0;

        //Cropped size
        int size_h = 120;
        int size_w = 180;

        // Convert half of the image to gray
        for (int y = size_h; y < frame->height-size_h; y++) {
            for (int x = size_w; x < frame->width-size_w; x++) {
                // This is a pointer to the start of the current row.
                //  Note: The image is stored as a 1-D array which is mapped back
                //  into 2-space by multiplying the widthStep (the image width rounded to
                //  a "nice" value, eg a multiple of 4 or 8 depending on the OS and CPU)
                //  by the row number.
                uchar* row = (uchar*)(frame->imageData + frame->widthStep * y);

                int gray = (row[x * 3] + row[x * 3 + 1] + row[x * 3 + 2]) / 3;

                row[x * 3] = gray;
                row[x * 3 + 1] = gray;
                row[x * 3 + 2] = gray;

            }
        }

        cvRectangle(frame, cvPoint(size_w, size_h), cvPoint(frame->width-size_w, frame->height-size_h), cvScalar(0, 255, 0), 3);

        // Shows the resulting image in the window
        cvShowImage("Camera image", frame);

        if ('c' == cvWaitKey(10)) {
            processedImage = frame;

            for (int y = size_h; y < frame-> height - size_h; y++) {
                for (int x = size_w; x < frame->width - size_w; x++) {
                    uchar* row = (uchar*)(frame->imageData + frame->widthStep * y);

                    // If the pixel value is greater than the threshold, we turn it white and set its tau value to 0
                    if (threshold < row[x * 3] && threshold < row[x * 3 + 1] && threshold < row[x * 3 + 2]) {
                        row[x * 3] = 255;
                        row[x * 3 + 1] = 255;
                        row[x * 3 + 2] = 255;

                    }

                    // If the pixel value is less than the threshold, we turrn it black and set its tau value to 1
                    if (row[x * 3] < threshold && row[x * 3 + 1] < threshold && row[x * 3 + 2] < threshold) {
                        row[x * 3] = 0;
                        row[x * 3 + 1] = 0;
                        row[x * 3 + 2] = 0;

                        moment_00 += 1;
                        moment_10 += 1 * y;
                        moment_01 += 1 * x;
                        moment_11 += (1 * x * y);
                        moment_20 += (1 * y * y);
                        moment_02 += (1 * x * x);

                    }
                }
            }

            // Calculating the coordinates for the centre of the blob
            double i_0 = moment_10 / moment_00;
            double j_0 = moment_01 / moment_00;
            // Calculating the angle of the axis of rotation
            double mo_angle1 = 2 * (moment_00 * moment_11 - moment_10 * moment_01);
            double mo_angle2 = ((moment_00 * moment_20 - (moment_10 * moment_10)) - (moment_00 * moment_02 - (moment_01 * moment_01)));

            //Depending on the signs of the numerator and denominator, we will have to resolve the angles
            //- (90 * 3.1415 / 180) (for use later)
            double theta_0 = 0;

            if (mo_angle1 > 0 && mo_angle2 > 0) {
                theta_0 = 0.5 * (atan2(mo_angle1, mo_angle2));
            }
            else if (mo_angle1 > 0 && mo_angle2 < 0) {
                theta_0 = 0.5 * (atan2(mo_angle1, mo_angle2) + (180 * 3.1415 / 180));
            }
            else if (mo_angle1 < 0 && mo_angle2 > 0) {
                theta_0 = 0.5 * (atan2(mo_angle1, mo_angle2) - (90 * 3.1415 / 180));
            }
            else if (mo_angle1 < 0 && mo_angle2 < 0) {
                theta_0 = 0.5 * (atan2(mo_angle1, mo_angle2) - (180 * 3.1415 / 180));
            }

            //theta_0 -= (90 * 3.1415 / 180);

            // Plotting the centre point
            cv::Mat ss = frame;
            drawMarker(ss, cvPoint(j_0, i_0), cvScalar(0, 0, 255), 0, 8, 2, 8);

            // Drawing a line to show the axis of rotation
            double x_2 = j_0 + (500 * cos(theta_0));
            double y_2 = i_0 - (500 * sin(theta_0));
            double alt_x = j_0 - (500 * cos(theta_0));
            double alt_y = i_0 + (500 * sin(theta_0));

            line(ss, cvPoint(j_0, i_0), cvPoint(x_2, y_2), cvScalar(0, 255, 0), 2, 1);
            line(ss, cvPoint(j_0, i_0), cvPoint(alt_x, alt_y), cvScalar(0, 255, 0), 2, 1);

            //Displaying values for the blob on the capture frame
            std::string area_str = std::string("Area: ") + std::to_string(moment_00);
            std::string cent_str = std::string("Center: ") + std::to_string(i_0) + ", " + std::to_string(j_0);
            std::string ang_str = std::string("Angle: ") + std::to_string(theta_0 * 180 / 3.14);


            cv::putText(ss, area_str, cvPoint(10, 80), cv::FONT_HERSHEY_SIMPLEX, 0.4, cvScalar(0, 255, 0), 1);
            cv::putText(ss, cent_str, cvPoint(10, 100), cv::FONT_HERSHEY_SIMPLEX, 0.4, cvScalar(0, 255, 0), 1);
            cv::putText(ss, ang_str, cvPoint(10, 120), cv::FONT_HERSHEY_SIMPLEX, 0.4, cvScalar(0, 255, 0), 1);



            cvShowImage("Screenshot", processedImage);

        }

    } while ('q' != cvWaitKey(10));

    //tidy up

    // Releases the CvCapture structure
    cvReleaseCapture(&capture);
    // Destroys all the HighGUI windows
    cvDestroyAllWindows();

    return 0;

} //end of main 

