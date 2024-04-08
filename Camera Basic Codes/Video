import os, sys, inspect
sys.path.append('/home/alysandra/project/lib/python3.11/site-packages')
import cv2 
 
cam = cv2.VideoCapture(0)

#for trouble shooting
if not cam.isOpened():
 print("Cannot open camera")
 exit()
while True:
 
ret, frame = cap.read()
gray = cv2.cvtColor(frame, cv.COLOR_BGR2GRAY)
cv2.imshow('frame', gray)

 if cv2.waitKey(1)!= -1:
  break
 
cam.release()
cv2.destroyAllWindows()
