import sys
import numpy as np
import cv2
import cv2.aruco as aruco
import argparse
from Vehicle_detection import track_vehicle_positions, get_nearest_tile
from tile_detection import detect_tile_type 

ap = argparse.ArgumentParser()
ap.add_argument("--type", type=str,
    default="DICT_ARUCO_ORIGINAL",
    help="type of ArUCo tag to detect")
args, unknown = ap.parse_known_args()

cap = cv2.VideoCapture(-1)
#print(cv2.__version__)

# Define the grid parameters
GRID_SIZE = 3  # Grid size (3x3)
GRID_SPACING = 1  # Spacing between grid lines (in meters)


# Define the ArUco marker size (in meters)
MARKER_SIZE = 0.1

# Define the camera intrinsic matrix
CAMERA_MATRIX = np.array([[1.26437615e+03, 0.00000000e+00, 6.39019835e+02],
                          [0.00000000e+00, 1.26346852e+03, 3.79144506e+02],
                          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
                          
cap = cv2.VideoCapture(-1)
while True:
    ret, frame = cap.read()
    
    if ret == True: 
        cv2.imshow('frame', frame)
        
        # use functions to get vehicle center and the closest tile, tile type and tile id
        vehicle_center = detect_marker_positions(self, frame) 
        closest_values, closest_tile = get_nearest_tile(self, vehicle_center, tile_center, tile_id):

        
        key = cv2.waitKey(1)

   
        if key == ord('q'):
            break
            

        

            

cap.release()
cv2.destroyAllWindows()


