import os, sys, inspect
sys.path.append('/home/alysandra/project/lib/python3.11/site-packages')
import cv2
import numpy as np
import math
import serial
import time

#ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)


def frame_prep(frame):
    #put frame in black and white
    bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #blur the black and white frame
    blur = cv2.GaussianBlur(bw, (9, 9), 0)
    #detect edges on the product of the previous 2 steps
    edges = cv2.Canny(blur, 50, 150)
    cv2.imshow("Edges",edges)
    return edges

def roi (edges):
    height, width = edges.shape
    #work out these 2 steps properly
    mask = np.zeros_like(edges)
    polygon = np.array([[
        (0, height),
        (width/3, (height/3)*2),
        (width/2, (height/3)*2),
        (width, height),
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)
    cropped_edges = cv2.bitwise_and(edges, mask)
    cv2.imshow("Region Of Interest", cropped_edges)
    
    return cropped_edges

def detect_lines (cropped_edges):
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 10, 5, 0)
    
    return lines

def average_slope_intercept(frame, lines):
    lane_lines = []
    
    #if there are no lines it stops here and returns it as none
    if lines is None:
        print("no line segments detected")
        return lane_lines
    height, width,_ = frame.shape
    
    left_fit = []
    right_fit = []
    
    boundary = 1/3
    left_boundary = width * (1 - boundary)
    right_boundary = width * boundary
    
    for line in lines:  
            for x1, y1, x2, y2 in line:
                if x1 == x2:
                    #print ("skipping vertical lines (slope = infinity)")
                    continue
                fit = np.polyfit((x1, x2), (y1, y2), 1)
                slope = (y2 - y1)/(x2 - x1)
                intercept = y1 - (slope * x1)
                
                if slope > 0:
                    if x1 < left_boundary and x2 < left_boundary:
                        left_fit.append((slope, intercept))
                else:
                    if x1 > right_boundary and x2 > right_boundary:
                        right_fit.append((slope, intercept))

                        
    left_avg = np.average(left_fit, axis = 0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(frame, left_avg))
        
    right_avg = np.average(right_fit, axis = 0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(frame, right_avg))
    return lane_lines

        
def make_points(frame, line):
    height, width, _ = frame.shape
    
    slope, intercept = line
    
    y1 = height
    y2 = int(y1/2)
    
    if slope == 0:
        slope = 0.1

    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    
    return [[x1, y1, x2, y2]]

def show_lane_lines (frame, lines):
    line_display = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            
    line_display = cv2.addWeighted(frame, 0.8, line_display, 1, 1)
    
    return line_display

def show_direction (frame, lane_lines):
    direction_image = np.zeros_like(frame)
    height, width, _ = frame.shape
    #why do i have to keep repeating this 
    if len(lane_lines) == 2:
        _, _, left_x2, _ = lane_lines[0][0]
        _, _, right_x2, _ = lane_lines[1][0]
        mid = int(width / 2)
        x_offset = (left_x2 + right_x2) / 2 - mid
        reference_point = (left_x2 + right_x2) / 2
    #if theres only one lane line
    elif len(lane_lines) == 1:
        x1, _, x2, _ = lane_lines[0][0]
        x_offset = x2 - x1
        reference_point = x2-x1
    #if there are no lane lines
    elif len(lane_lines) == 0:
        x_offset = 0
        reference_point = 160

    x = int(reference_point)
    y = 120
    
    cv2.circle(direction_image, (x, y), 10, (0, 0, 255), 5)
    direction_image = cv2.addWeighted(frame, 0.8, direction_image, 1, 1)
    
    return direction_image
    
def find_direction (frame, lane_lines):
    height, width, _ = frame.shape
    #if there are 2 lane lines
    if len(lane_lines) == 2:
        _, _, left_x2, _ = lane_lines[0][0]
        _, _, right_x2, _ = lane_lines[1][0]
        mid = int(width / 2)
        x_offset = (left_x2 + right_x2) / 2 - mid
    #if theres only one lane line
    elif len(lane_lines) == 1:
        x1, _, x2, _ = lane_lines[0][0]
        x_offset = x2 - x1
    #if there are no lane lines
    elif len(lane_lines) == 0:
        x_offset = 0
        
    direction = (x_offset / 320)
    
    return direction

#def serial_comm (direction):
    #have to convert direction to a number between 100 and 200 because I can't find a way to send negative numbers for serial communication
    position = int((direction*100)+200)
    print(int(position))
    ser.write(int(position).to_bytes())
    ser.flush()
    return(position)

def other_lines(left_boundary, right_boundary, frame, lines, lane_lines):
    horizontal_lines = []
    other_lines_image = np.zeros_like(frame)
    
    lx1, ly1, lx2, ly2 = lane_lines[0][0]

    rx1, ry1, rx2, ry2 = lane_lines[1][0]

    if lines is None:
        print("no line segments detected")
        return lane_lines
    height, width,_ = frame.shape
    if len(lane_lines) == 2:
        left_lane_slope = ((ly2 - ly1)/(lx2 - lx1))
        right_lane_slope = (((ry2 - ry1)/(rx2 - rx1))) 
    elif len(lane_lines) == 1:
        one_line__slope = ((lane_lines[0][3])-(lane_lines[0][1]))/((lane_lines[0][2])-(lane_lines[0][0]))
    elif len(lane_lines) == 0:
        return horizontal_lines
    if lines is not None:
        for line in lines:  
                for x1, y1, x2, y2 in line:
                    if x1 == x2:
                        #print ("skipping vertical lines (slope = infinity)")
                        continue
                    fit = np.polyfit((x1, x2), (y1, y2), 1)
                    slope = (y2 - y1)/(x2 - x1)
                    intercept = y1 - (slope * x1)
                    #check if this is right way around and do you need to average these too?
                    if left_boundary > x1 > right_boundary and left_boundary > x2 > right_boundary:
                        left_check = slope - left_lane_slope
                        right_check = slope - right_lane_slope
                        print("checking")
                        upper_bound = left_check + 1
                        lower_bound = left_check - 1
                        if lower_bound < right_check < upper_bound:
                            horizontal_lines.append([x1, y1, x2, y2])
                            other_lines_image = cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                            other_lines_image = cv2.addWeighted(frame, 0.8, other_lines_image, 1, 1)
                            print("horizontal!")
                    else:
                        horizontal_lines.append([0, 0, 0, 0])
    return other_lines_image





cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_FRAME_WIDTH,320)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

time.sleep(1)

lastTime = 0
lastError = 0

while True:
    ret, frame = cam.read()
    frame = cv2.flip(frame,-1)
    height, width, _ = frame.shape
    boundary = 1/3
    left_boundary = width * (1 - boundary)
    right_boundary = width * boundary

    edges = frame_prep(frame)
    lines = detect_lines(roi(edges))
    lane_lines = average_slope_intercept(frame, lines)
    line_display = show_lane_lines(frame,lane_lines)
    direction = find_direction(frame, lane_lines)
    direction_image = show_direction(line_display, lane_lines)
    #position = serial_comm(direction)
    other_lines_image = other_lines(left_boundary, right_boundary, frame, lines, lane_lines)
    cv2.imshow("Result",direction_image)
    cv2.imshow ("Other lines", other_lines_image)
    #print(position)
    now = time.time()
    dt = now - lastTime
    
    lastTime = time.time()
    
    key = cv2.waitKey(1)        
    if key != -1:
        break
    
cam.release()
cv2.destroyAllWindows()
