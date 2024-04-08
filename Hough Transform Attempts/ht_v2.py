import os, sys, inspect
sys.path.append('/home/alysandra/project/lib/python3.11/site-packages')
import cv2
import numpy as np

cam = cv2.VideoCapture(0)

while True:
	ret, frame = cam.read()
	bwCam = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	vid = frame

	dst = np.copy(vid)
	def onTrackbarChange(max_slider):
		global vid
		global dst
		global bwCam
		th1 = max_slider 
		th2 = th1 * 0.4
		edges = cv2.Canny(bwCam, th1, th2)
		lines = cv2.HoughLinesP(edges, 2, np.pi/180, 1, None, minLineLength=10, maxLineGap=100)
	
		if lines is not None:
			for line in lines:	
				x1, y1, x2, y2 = line[0]
				cv2.line(dst, (x1, y1), (x2, y2), (0,0,255), 3)

		cv2.imshow("Result Image", dst)	
		cv2.imshow("Edges",edges)

	

	while cam.isOpened():
		if __name__ == "__main__":
			
			

			# Create display windows
			cv2.namedWindow("Edges")
			cv2.namedWindow("Result Image")
			  

			# Initialize threshold value
			initThresh = 50

			# Maximum threshold value
			maxThresh = 1250

			cv2.createTrackbar("threshold", "Result Image", initThresh, maxThresh, onTrackbarChange)
			onTrackbarChange(initThresh)

	key = cv2.waitKey(1)		
	if key != -1:
		break

cam.release()
cv2.destroyAllWindows()
