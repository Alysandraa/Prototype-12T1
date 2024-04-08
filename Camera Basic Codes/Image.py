import os, sys, inspect
sys.path.append('/home/alysandra/project/lib/python3.11/site-packages')
import cv2

vid = cv2.VideoCapture(0)

while True:
	ret, frame = vid.read()
	cv2.imshow('frame', frame)

vid.release()
cv2.destroyAllWindows()
