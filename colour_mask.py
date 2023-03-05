import cv2
import numpy as np

vid = cv2.VideoCapture(0)

def nothing(pos):
	pass

# Creating a new window where users can change the HSV values with trackbars
cv2.namedWindow('HSV Values')
cv2.createTrackbar('LH','HSV Values',0,255, nothing)
cv2.createTrackbar('LS','HSV Values',0,255, nothing)
cv2.createTrackbar('LV','HSV Values',0,255, nothing)
cv2.createTrackbar('UH','HSV Values',255,255, nothing)
cv2.createTrackbar('US','HSV Values',255,255, nothing)
cv2.createTrackbar('UV','HSV Values',255,255, nothing)

while(1):
    _, frame = vid.read() # Reading live webcam video
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Converting the webcam video from RGB to HSV

# Reading position of the trackbars
    lh = cv2.getTrackbarPos('LH','HSV Values')
    ls = cv2.getTrackbarPos('LS','HSV Values')
    lv = cv2.getTrackbarPos('LV','HSV Values')
    uh = cv2.getTrackbarPos('UH','HSV Values')
    us = cv2.getTrackbarPos('US','HSV Values')
    uv = cv2.getTrackbarPos('UV','HSV Values')

# Storing the HSV values obtained from the trackbar window
    lower_values = np.array([lh,ls,lv],np.uint8)
    upper_values = np.array([uh,us,uv],np.uint8)

# Assigning HSV values obtained from trackbar window to a mask
    colour_mask = cv2.inRange(frameHSV,lower_values, upper_values)

    kernal = np.ones((5 ,5), "uint8")

    colour_mask = cv2.dilate(colour_mask,kernal)
    cv2.imshow("Mask", colour_mask)
    cv2.imshow("Normal Live Webcam Video", frame)

    if cv2.waitKey(1)== ord('q'):
        break

vid.release()
cv2.destroyAllWindows()