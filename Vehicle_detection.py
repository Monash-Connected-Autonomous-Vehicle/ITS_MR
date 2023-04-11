class vehicle_detection:
	def __init__(self, marker_length=MARKER_SIZE, camMatrix = CAMERA_MATRIX): #robot
		self.camera_matrix = camMatrix
		#self.distortion_params - robot.camera_dist
		self.marker_length = marker_length
		self.aruco_params = aruco.DetectorParameters_create()
		self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

	def track_vehicle_positions(self, img) :
		# Perform detection
		corners, ids, rejected = aruco.detectMarkers(img, self.aruco_dict, parameters=self.aruco_params) 
		rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, self.marker_length, self.camera_matrix, None)
		positions = tvecs.squeeze()
		frame_markers = aruco.drawDetectedMarkers(img.copy(), corners, ids)
		
		vehicle_center = np.zeros((len(ids))
		
		for i in range(len(ids)):
            		if np.isin(ids, i).any() == True:
                		bottomLeft = corners[i][0][0]
                		topRight = corners[i][0][2]
                		centerx = (bottomLeft[0] + topRight[0])/2
                		centery = (bottomLeft[1] + topRight[1])/2
                		vehicle_center[i] = (centerx, centery)
                		cv2.circle(frame, (int(centerx), int(centery)), 4, (50, 200, 50), -1)
			else: 
            			print('id',i, 'is not valid')
            	return vehicle_center
            	
	def get_nearest_tile(self, vehicle_center, tile_center, tile_id):
		closest_values = np.zeros_like(vehicle_center)
		closest_tile = np.zeros_like(vehicle_center)
		for i in range(len(vehicle_center)):
			tile_count = np.argmin(np.abs(vehicle_center[i] - tile_center))
			closest_values[i] = tile_center[tile_count]
			closest_tile[i] = tile_id[tile_count]
		return closest_values, closest_tile
