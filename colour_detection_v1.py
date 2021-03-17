import cv2
import numpy as np

vid = cv2.VideoCapture(0)
coords = []

while True:
    ret, frame = vid.read()
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(frameHSV, low_red, high_red)
    red = cv2.bitwise_and(frame, frame, mask = red_mask)
    last_x_red, last_y_red = 0, 0 # Store the last x and y red positions

    # Every colour except white
    low = np.array([0, 42, 0])
    high = np.array([179, 255, 255])
    mask = cv2.inRange(frameHSV, low, high)
    result = cv2.bitwise_and(frame, frame, mask = mask)

    cv2.imshow("Frame", frame)
    cv2.imshow("Red mask", red)
    cv2.imshow("Result", result)

    # Find coordinates
    rows, cols, _ = result.shape
    for x in range(rows):
        for y in range(cols):
            px = list(result[x, y])
            if px == red_mask:
                if len(coords) == 0:
                    coords.append((y, x))

                last_x_red, last_y_red = x, y
    
    coords.append((last_y_red, last_x_red))
    print(coords)
    top_left = coords[0]
    bottom_left = (coords[0][0], coords[1][1])
    top_right = (coords[1][0], coords[0][1])
    bottom_right = coords[1]
    center = (top_right[0] - top_left[0], bottom_right[1] - top_right[1])
    print('The coordinates of the mask from left to right and top to bottom and also the center are:')
    print(f'Top Left: {top_left}, Top Right: {top_right}, Bottom Left: {bottom_left}, Bottom Right: {bottom_right}, Center: {center}')
    
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()