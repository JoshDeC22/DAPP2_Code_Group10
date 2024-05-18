import cv2
import numpy as np
import dlib
from math import hypot

#change the camera by changing the index below, 0 is default
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

font = cv2.FONT_HERSHEY_PLAIN

def get_mouth_open_ratio(upper_lip_point, lower_lip_point, facial_landmarks):
    upper_lip = (facial_landmarks.part(upper_lip_point).x, facial_landmarks.part(upper_lip_point).y)
    lower_lip = (facial_landmarks.part(lower_lip_point).x, facial_landmarks.part(lower_lip_point).y)

    # Calculating the vertical distance between the upper and lower lip
    distance = hypot((upper_lip[0] - lower_lip[0]), (upper_lip[1] - lower_lip[1]))
    return distance


def midpoint(p1,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x,facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x,facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]),facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]),facial_landmarks.part(eye_points[4]))

    #hor_line = cv2.line(frame,left_point,right_point,(0,255,0),2)
    #ver_line = cv2.line(frame, center_top, center_bottom, (0,255,0), 2)

    ver_line_length = hypot((center_top[0] - center_bottom[0]), (center_top[1]- center_bottom[1]))
    hor_line_length = hypot((left_point[0] - right_point[0]), (left_point[1]- right_point[1]))
        
    ratio = (hor_line_length/ver_line_length)
    return ratio

def get_gaze_ratio(eye_points, facial_landmarks, frame, gray):
    eye_region = np.array([(facial_landmarks.part(point).x, facial_landmarks.part(point).y) for point in eye_points], np.int32)
    # Calculate the mask for the eye
    height, width = frame.shape[:2]
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [eye_region], True, 255, 2)
    cv2.fillPoly(mask, [eye_region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)

    # Find the bounding box of the eye
    min_x = np.min(eye_region[:, 0])
    max_x = np.max(eye_region[:, 0])
    min_y = np.min(eye_region[:, 1])
    max_y = np.max(eye_region[:, 1])
    gray_eye = eye[min_y:max_y, min_x:max_x]

    # Threshold to isolate the pupil
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    
    # Calculate the horizontal gaze ratio
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[0:height, 0:int(width / 2)]
    left_side_white = cv2.countNonZero(left_side_threshold)
    right_side_threshold = threshold_eye[0:height, int(width / 2):width]
    right_side_white = cv2.countNonZero(right_side_threshold)
    horizontal_gaze_ratio = left_side_white / (right_side_white + 1e-1)

    # Calculate the vertical gaze ratio
    top_side_threshold = threshold_eye[0:int(height / 2), :]
    top_side_white = cv2.countNonZero(top_side_threshold)
    bottom_side_threshold = threshold_eye[int(height / 2):height, :]
    bottom_side_white = cv2.countNonZero(bottom_side_threshold)
    vertical_gaze_ratio =(bottom_side_white + 1e-1)

    return horizontal_gaze_ratio, vertical_gaze_ratio

if __name__ == '__main__':
    while True:
        _, frame = cap.read()
        new_frame = np.zeros((500, 500, 3), np.uint8)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            landmarks = predictor(gray, face)
        
            # Gaze detection
            horizontal_gaze_ratio_left_eye, vertical_gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks, frame, gray)
            horizontal_gaze_ratio_right_eye, vertical_gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks, frame, gray)
        
            # Average the gaze ratio for both eyes
            horizontal_gaze_ratio = (horizontal_gaze_ratio_left_eye + horizontal_gaze_ratio_right_eye) / 2
            vertical_gaze_ratio = (vertical_gaze_ratio_left_eye + vertical_gaze_ratio_right_eye) / 2
        
            # Detecting direction by comparing the gaze ratio to thresholds
            if horizontal_gaze_ratio < 0.7:
                cv2.putText(frame, "LOOKING RIGHT", (50, 100), font, 2, (0, 0, 255), 3)
            elif 0.7 <= horizontal_gaze_ratio < 1.7:
                cv2.putText(frame, "LOOKING CENTER", (50, 100), font, 2, (0, 0, 255), 3)
            else:
                cv2.putText(frame, "LOOKING LEFT", (50, 100), font, 2, (0, 0, 255), 3)
        
            # Detecting up or down
            
            #print(vertical_gaze_ratio)
            if vertical_gaze_ratio > 110:
                cv2.putText(frame, "LOOKING UP", (50, 150), font, 2, (0, 255, 0), 3)
            elif 60 <= vertical_gaze_ratio < 100:
                # Horizontal center text already present, no need for vertical center text
                pass
            else:
                cv2.putText(frame, "LOOKING DOWN", (50, 200), font, 2, (255, 0, 0), 3)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
