from dapp_eyetracker import *
from GUI import *
from tensorflow.keras import models
from recording_helper import record_audio, terminate
from tf_helper import preprocess_audiobuffer
from grbl_sender import *
from inverse_kinematics import *

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

    serial_port = open_grbl('COM9', 115200)

    is_moving = True
    mouth_status = "CLOSED"
    x, y, x_limits, y_limits = get_original_position()
    
    while True:
        voice_command = 'stop'
        
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
                horizontal_gaze_ratio = 0.1
            elif average_horizontal_gaze_ratio > upper_horizontal:
                horizontal_gaze_ratio = -0.1
            else:
                horizontal_gaze_ratio = 0

            if x < x_limits[0] or x > x_limits[1]:
                horizontal_gaze_ratio = 0
                
            if average_vertical_gaze_ratio > upper_vertical:
                vertical_gaze_ratio = 0.1
            elif average_vertical_gaze_ratio < lower_vertical:
                vertical_gaze_ratio = -0.1
            else:
                vertical_gaze_ratio = 0

            if y < y_limits[0] or y > y_limits[1]:
                vertical_gaze_ratio = 0
                  
        mouth_open_ratio = get_mouth_open_ratio(63, 67, landmarks)
        
        if mouth_open_ratio > mouth_threshold:
            mouth_status = "OPEN"
        if mouth_status == "OPEN":
            command = predict_mic()
            if command ==  'up':
                send_command(1, 0, 0, serial_port, is_moving)
            elif command == 'down':
                send_command(-1, 0, 0, serial_port, is_moving)
            elif command == 'go':
                is_moving = True
            else:
                is_moving = False
        mouth_status = 'CLOSED'
        
        stepsY, stepsX, x, y = inverse_kin(x, y, horizontal_gaze_ratio, vertical_gaze_ratio)
        send_command(0, stepsY, stepsX, serial_port, is_moving)
    
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
            
    save_position(x, y, x_limits, y_limits) 
    close_grbl(serial_port)
    cap.release()
    cv2.destroyAllWindows()                 
