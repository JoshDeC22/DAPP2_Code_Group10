import PySimpleGUI as sg
import sys
import cv2
from dapp_eyetracker import *

def eyetracking_frame(upper_vert, lower_vert, upper_horizontal, lower_horizontal):
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
        if horizontal_gaze_ratio < lower_horizontal:
            cv2.putText(frame, "LOOKING RIGHT", (50, 100), font, 2, (0, 0, 255), 3)
        elif lower_horizontal <= horizontal_gaze_ratio < upper_horizontal:
            cv2.putText(frame, "LOOKING CENTER", (50, 100), font, 2, (0, 0, 255), 3)
        else:
            cv2.putText(frame, "LOOKING LEFT", (50, 100), font, 2, (0, 0, 255), 3)
        
        # Detecting up or down
            
        #print(vertical_gaze_ratio)
        if vertical_gaze_ratio > upper_vert:
            cv2.putText(frame, "LOOKING UP", (50, 150), font, 2, (0, 255, 0), 3)
        elif lower_vert <= vertical_gaze_ratio < upper_vert:
            # Horizontal center text already present, no need for vertical center text
            pass
        else:
            cv2.putText(frame, "LOOKING DOWN", (50, 200), font, 2, (255, 0, 0), 3)

    imgbytes = cv2.imencode(".png", frame)[1].tobytes()
    return imgbytes

def data_reconstructor(data):
    data_list = []
    while True:
        try:
            index = data.index(',')
            data_list.append(float(data[:index]))
            data = data[index + 1:]
        except ValueError:
            data_list.append(float(data))
            break
    return data_list

def file_opener():
    while True:
        try:
            file = open('limits.txt', 'r')
            data = file.read()
            file.close()
            if data == '':
                file = open('limits.txt', 'w')
                data = '0.3,1.7,30.0,170.0'
                file.write(data)
                file.close()
            break
        except FileNotFoundError:
            file = open('limits.txt', 'a')
            file.close()
            file = open('limits.txt', 'w')
            data = '0.3,1.7,30.0,170.0'
            file.write(data)
            file.close()
            break
    data_list = data_reconstructor(data)
    return data_list

def file_saver(horizontal_ratios, vertical_ratios):
    ratios = horizontal_ratios + vertical_ratios
    ratios = [str(i) for i in ratios]
    data = ','.join(ratios)
    file = open('limits.txt', 'r+')
    file.seek(0)
    file.truncate()
    file.close()
    file = open('limits.txt', 'w')
    file.write(data)
    file.close()

def main_gui(lower_h, upper_h, lower_v, upper_v):
    default_values = [0.3, 1.7, 30.0, 170.0]
    sg.theme('DarkBlack')

    starting_horizontal_ratios_string = [str((lower_h / default_values[0]) * 100), str((upper_h / default_values[1]) * 100)]
    starting_vertical_ratios_string = [str((lower_v / default_values[2]) * 100), str((upper_v / default_values[3]) * 100)]

    horizontal_ratios = [lower_h, upper_h]
    vertical_ratios = [lower_v, upper_v]

    layout = [
        [sg.Image(filename='', key='-IMAGE-')],
        [sg.T('Left limit:', key='-HLOWER-'), sg.I(starting_horizontal_ratios_string[0], key='-IHLOWER-')],
        [sg.T('Right limit:', key='-HUPPER-'), sg.I(starting_horizontal_ratios_string[1], key='-IHUPPER-')],
        [sg.T('Down limit:', key='-VLOWER-'), sg.I(starting_vertical_ratios_string[0], key='-IVLOWER-')],
        [sg.T('Up limit:', key='-VUPPER-'), sg.I(starting_vertical_ratios_string[1], key='-IVUPPER-')],
        [sg.Save(), sg.Exit()]
    ]

    window = sg.Window("Calibration Interface", layout, size=(800, 800))

    cap = cv2.VideoCapture(0)

    while True:
        event, values = window.read(timeout=20)  # Use a small timeout to make the loop run frequently
        if event in ('Exit', sg.WIN_CLOSED):
            break
        elif event == 'Save':
            horizontal_ratios[0] = default_values[0] * (float(values['-IHLOWER-']) / 100)
            horizontal_ratios[1] = default_values[1] * (float(values['-IHUPPER-']) / 100)
            vertical_ratios[0] = default_values[2] * (float(values['-IVLOWER-']) / 100)
            vertical_ratios[1] = default_values[3] * (float(values['-IVUPPER-']) / 100)
            file_saver(horizontal_ratios, vertical_ratios)
        
        # Webcam feed update
        imgbytes = eyetracking_frame(vertical_ratios[1], vertical_ratios[0], horizontal_ratios[1], horizontal_ratios[0])
        window["-IMAGE-"].update(data=imgbytes)

    window.close()

if __name__ == '__main__':
    data = file_opener()
    main_gui(data[0], data[1], data[2], data[3])
