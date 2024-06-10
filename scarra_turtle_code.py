from dapp_eyetracker import *
from GUI import *
from tensorflow.keras import models
from recording_helper import record_audio, terminate
from tf_helper import preprocess_audiobuffer
from turtle_helper import move
import turtle

def predict_mic():
    audio = record_audio()
    spec = preprocess_audiobuffer(audio)
    prediction = loaded_model(spec)
    label_pred = np.argmax(prediction, axis = 1)
    command = commands[label_pred[0]]
    return command

def get_limits(filename):
    file = open(filename, 'r')
    data = file.read()
    file.close()
    limits = list(data.split(","))
    return tuple([float(i) for i in limits])

if __name__ == '__main__':
    data = file_opener()
    main_gui(data[0], data[1], data[2], data[3], data[4])
    
    lower_horizontal, upper_horizontal, lower_vertical, upper_vertical, mouth_threshold = get_limits('limits.txt')
        
    commands = ['down', 'go', 'stop', 'up']
    loaded_model = models.load_model('saved_model_final')

    is_moving = False
    mouth_status = "CLOSED"
    
    s = turtle.getscreen()

    t = turtle.Turtle()

    size = t.turtlesize()

    increase = (2*num for num in size)

    t.turtlesize(*increase)

    t.pensize(5)
    t.shapesize()
    t.pencolor('blue')
    
    while True:  
        _, frame = cap.read()
        new_frame = np.zeros((500, 500, 3), np.uint8)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        
        for face in faces:
            landmarks = predictor(gray, face)
            
            horizontal_gaze_ratio_left_eye, vertical_gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks, frame, gray)
            horizontal_gaze_ratio_right_eye, vertical_gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks, frame, gray)
        
            average_horizontal_gaze_ratio = (horizontal_gaze_ratio_left_eye + horizontal_gaze_ratio_right_eye) / 2
            average_vertical_gaze_ratio = (vertical_gaze_ratio_left_eye + vertical_gaze_ratio_right_eye) / 2
            
            if average_horizontal_gaze_ratio < lower_horizontal:
                horizontal_gaze_ratio = 1
            elif average_horizontal_gaze_ratio > upper_horizontal:
                horizontal_gaze_ratio = -1
            else:
                horizontal_gaze_ratio = 0
                
            if average_vertical_gaze_ratio > upper_vertical:
                vertical_gaze_ratio = 1
            elif average_vertical_gaze_ratio < lower_vertical:
                vertical_gaze_ratio = -1
            else:
                vertical_gaze_ratio = 0
                  
        mouth_open_ratio = get_mouth_open_ratio(63, 67, landmarks)
        
        if mouth_open_ratio > mouth_threshold:
            mouth_status = "OPEN"
        if mouth_status == "OPEN":
            command = predict_mic()
            if command ==  'up':
                t.penup()
            elif command == 'down':
                t.pendown()
            elif command == 'go':
                is_moving = True
            else:
                is_moving = False
        mouth_status = 'CLOSED'
        
        move(horizontal_gaze_ratio, vertical_gaze_ratio, t, is_moving)
    
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break

    
    terminate()
    cap.release()
    cv2.destroyAllWindows()                 