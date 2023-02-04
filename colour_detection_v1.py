import cv2
import numpy as np

video = cv2.VideoCapture(0)

while True:
    _, frame = video.read()
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(frameHSV, low_red, high_red)
    red = cv2.bitwise_and(frame, frame, mask = red_mask)

    # Every colour except white
    low = np.array([0, 42, 0])
    high = np.array([179, 255, 255])
    mask = cv2.inRange(frameHSV, low, high)
    result = cv2.bitwise_and(frame, frame, mask = mask)

    cv2.imshow("Frame", frame)
    cv2.imshow("Red mask", red)
    cv2.imshow("Result", result)
    
    key = cv2.waitKey(1)
    if key == 27:  # "s" key
        break
