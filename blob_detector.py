import cv2
import numpy as np

def nothing(pos):
	pass

vid = cv2.VideoCapture(0)
x_o = 0
y_o = 240
x_d = 0.0
y_d = 0.0
x_d_p = 0.0
y_d_p = 0.0

while(1):
	_, frame = vid.read()
	    
	# Converting BGR to HSV 

	frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower = np.array([0,111,162], np.uint8)
	upper = np.array([255,255,255], np.uint8)

	mask = cv2.inRange(frameHSV, lower, upper)
	
	# Morphological transformation, Dilation  	
	kernel = np.ones((5 ,5), "uint8")
	
	mask = cv2.dilate(mask, kernel)
	frame = cv2.circle(frame, (x_o,y_o), 5, (255,0,0), -1)

			
	# Tracking the colour specified by the mask
	(contours, hierarchy) = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	if len(contours) > 0:
		contour = max(contours, key = cv2.contourArea)
		area = cv2.contourArea(contour)
		if area > 800: 
			x,y,w,h = cv2.boundingRect(contour)	
			img = cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0),2)
			img = cv2.circle(frame, ((2*x+w)//2, (2*y+h)//2), 5, (255,0,0), -1)
			img = cv2.line(frame, (x_o,y_o), ((2*x+w)//2, (2*y+h)//2), (0,255,0), 2)
		
			x_d = (((2*y+h)/2)-68) * 0.06
			y_d = (((2*x+w)/2)-260) * 0.075
			
			s = 'x_d:'+ str(x_d)+ 'y_d:'+ str(y_d)
			
			cv2.putText(frame, s, (x-20,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
		

		
			if (abs(x_d-x_d_p) > 1 or abs(y_d-y_d_p) > 1):
			
				x_d_p = x_d
				y_d_p = y_d
			
		
	
	cv2.imshow("Mask", mask)
	cv2.imshow("Color Tracking", frame)
	if cv2.waitKey(1) == ord('q'):
		break

vid.release()
cv2.destroyAllWindows()