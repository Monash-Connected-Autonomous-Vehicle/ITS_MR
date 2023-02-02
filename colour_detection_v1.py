import sys
import numpy as np
import pyzed.sl as sl
import cv2

def save_sbs_image(zed, filename) :

    image_sl_left = sl.Mat()
    zed.retrieve_image(image_sl_left, sl.VIEW.LEFT)
    image_cv_left = image_sl_left.get_data()

    image_sl_right = sl.Mat()
    zed.retrieve_image(image_sl_right, sl.VIEW.RIGHT)
    image_cv_right = image_sl_right.get_data()

    sbs_image = np.concatenate((image_cv_left, image_cv_right), axis=1)

    cv2.imwrite(filename, sbs_image)

def main():

    zed = sl.Camera()

    input_type = sl.InputType()
    if len(sys.argv) >= 2:
        input_type.set_from_svo_file(sys.argv[1])
    init = sl.InitParameters(input_t=input_type)
    init.camera_resolution = sl.RESOLUTION.HD1080
    init.coordinate_units = sl.UNIT.MILLIMETER

    err = zed.open(init)
    if err != sl.ERROR_CODE.SUCCESS :
        print(repr(err))
        zed.close()
        exit(1)

    runtime = sl.RuntimeParameters()
    runtime.sensing_mode = sl.SENSING_MODE.STANDARD

    image_size = zed.get_camera_information().camera_resolution
    image_size.width = image_size.width /2
    image_size.height = image_size.height /2

    image_zed = sl.Mat(image_size.width, image_size.height, sl.MAT_TYPE.U8_C4)
    image_ocv = image_zed.get_data()
    
    cv2.imshow("Image", image_ocv)
    b = image_ocv[:, :, :1]
    g = image_ocv[:, :, 1:2]
    r = image_ocv[:, :, 2:]

    b_mean = np.mean(b)
    g_mean = np.mean(g)
    r_mean = np.mean(r)

    if (b_mean > g_mean and b_mean > r_mean):
        print("Blue")
    if (g_mean > r_mean and g_mean > b_mean):
        print("Green")
    else:
        print("Red")

cv2.destroyAllWindows
zed.close() 

if __name__ == "__main__":
    main()
