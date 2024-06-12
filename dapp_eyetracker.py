import cv2
import numpy as np
import dlib
from math import hypot

#change the camera by changing the index below, 0 is default
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

font = cv2.FONT_HERSHEY_PLAIN

def get_mouth_open_ratio(upper_lip_point, lower_lip_point, landmarks):
    upper_lip = (landmarks.part(upper_lip_point).x, landmarks.part(upper_lip_point).y)
    lower_lip = (landmarks.part(lower_lip_point).x, landmarks.part(lower_lip_point).y)

    # Calculating the vertical distance between the upper and lower lip
    distance = hypot((upper_lip[0] - lower_lip[0]), (upper_lip[1] - lower_lip[1]))
    return distance


def midpoint(point1,point2):
    return int((point1.x + point2.x)/2), int((point1.y + point2.y)/2)

def get_blinking_ratio(eye_points, landmarks):
    left_point = (landmarks.part(eye_points[0]).x,landmarks.part(eye_points[0]).y)
    right_point = (landmarks.part(eye_points[3]).x,landmarks.part(eye_points[3]).y)
    center_top = midpoint(landmarks.part(eye_points[1]),landmarks.part(eye_points[2]))
    center_bottom = midpoint(landmarks.part(eye_points[5]),landmarks.part(eye_points[4]))

    #hor_line = cv2.line(frame,left_point,right_point,(0,255,0),2)
    #ver_line = cv2.line(frame, center_top, center_bottom, (0,255,0), 2)

    ver_line_length = hypot((center_top[0] - center_bottom[0]), (center_top[1]- center_bottom[1]))
    hor_line_length = hypot((left_point[0] - right_point[0]), (left_point[1]- right_point[1]))
        
    ratio = (hor_line_length/ver_line_length)
    return ratio

def get_gaze_ratio(eye_points, landmarks, frame, gray):
    region = np.array([(landmarks.part(point).x, landmarks.part(point).y) for point in eye_points], np.int32)
    # Calculate the mask for the eye
    h, w = frame.shape[:2]
    mask = np.zeros((h, w), np.uint8)
    cv2.polylines(mask, [region], True, 255, 2)
    cv2.fillPoly(mask, [region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)

    # Find the bounding box of the eye
    min_x = np.min(region[:, 0])
    max_x = np.max(region[:, 0])
    min_y = np.min(region[:, 1])
    max_y = np.max(region[:, 1])
    gray_eye = eye[min_y:max_y, min_x:max_x]

    # Threshold to isolate the pupil
    _, threshold = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    
    # Calculate the horizontal gaze ratio
    h, w = threshold.shape
    left_threshold = threshold[0:h, 0:int(w / 2)]
    left_white = cv2.countNonZero(left_threshold)
    right_threshold = threshold[0:h, int(w / 2):w]
    right_white = cv2.countNonZero(right_threshold)
    horizontal_gaze_ratio = left_white / (right_white + 1e-1)

    # Calculate the vertical gaze ratio
    top_threshold = threshold[0:int(h / 2), :]
    top_white = cv2.countNonZero(top_threshold)
    bottom_threshold = threshold[int(h / 2):h, :]
    bottom_white = cv2.countNonZero(bottom_threshold)
    vertical_gaze_ratio =(bottom_white + 1e-1)

    return horizontal_gaze_ratio, vertical_gaze_ratio
