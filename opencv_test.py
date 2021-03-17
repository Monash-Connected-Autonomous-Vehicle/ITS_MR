import cv2
import numpy as np

vid = cv2.VideoCapture(0)

while True:
    ret, frame = vid.read()
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    low = np.array([90, 50, 50])
    high = np.array([130, 255, 255])
    mask = cv2.inRange(frameHSV, low, high)
    result = cv2.bitwise_and(frame, frame, mask = mask)
    cv2.imshow('Result', result)
    if cv2.waitKey(1) == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()