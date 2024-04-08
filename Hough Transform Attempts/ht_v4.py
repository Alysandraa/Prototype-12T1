import os, sys, inspect
sys.path.append('/home/alysandra/project/lib/python3.11/site-packages')
import cv2
import numpy as np

cam = cv2.VideoCapture(0)


while True:
	ret, frame = cam.read()
	vid = frame
	bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(bw, (9, 9), 0)
	
	edges = cv2.Canny(blur, 50, 150)
	lines = cv2.HoughLinesP(edges, 1, np.pi/180, 20, None, 100, 0)
	
	if lines is not None:
		for line in lines:	
			x1, y1, x2, y2 = line[0]
			cv2.line(vid, (x1, y1), (x2, y2), (0,255,0), 2)
	
		
	cv2.imshow("Result Image", vid)	
	cv2.imshow("Edges",edges)
	#also fixed that wait key was in a while true loop which kept the program stuck in the overall true loop
	key = cv2.waitKey(1)		
	if key != -1:
		break
cam.release()
cv2.destroyAllWindows()
