import PySimpleGUI as sg
import cv2
import numpy as np
from math import hypot
from dapp_eyetracker import *

# Define ASCII arrows
arrows = {
    "up": "^",
    "down": "v",
    "left": "<",
    "right": ">"
}

# Define highlighted ASCII arrows
highlighted_arrows = {
    "up": "^",
    "down": "v",
    "left": "<",
    "right": ">"
}

# Function to overlay ASCII arrows
def overlay_arrows_and_mouth_indicator(frame, direction, mouth_open):
    h, w, _ = frame.shape

    # Define positions for ASCII arrows, adjusting to the left
    positions = {
        "up": (int(w / 2) - 20, 50),
        "down": (int(w / 2) - 20, h - 50),
        "left": (50, int(h / 2)),
        "right": (w - 100, int(h / 2)),
    }

    # Overlay ASCII arrows on the frame
    for dir, pos in positions.items():
        if dir == direction:
            cv2.putText(frame, highlighted_arrows[dir], pos, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3, cv2.LINE_AA)
        else:
            cv2.putText(frame, arrows[dir], pos, cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)

    # Overlay mouth open indicator, adjusting to the left
    if mouth_open:
        cv2.circle(frame, (int(w / 2) , int(h / 2)), 50, (0, 0, 255), -1)  # Red filled circle

    return frame

# Function to detect gaze and mouth open ratio
def detect_gaze_and_mouth(upper_vert, lower_vert, upper_horizontal, lower_horizontal, mouth_sensitivity):
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    direction = "center"
    mouth_open = False
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
            direction = "right"
        elif lower_horizontal <= horizontal_gaze_ratio < upper_horizontal:
            direction = "center"
        else:
            direction = "left"
        
        if vertical_gaze_ratio > upper_vert:
            direction = "up"
        elif lower_vert <= vertical_gaze_ratio < upper_vert:
            pass  # Horizontal center text already present, no need for vertical center text
        else:
            direction = "down"

        # Mouth open detection
        upper_lip = (landmarks.part(62).x, landmarks.part(62).y)
        lower_lip = (landmarks.part(66).x, landmarks.part(66).y)
        mouth_open_ratio = hypot((upper_lip[0] - lower_lip[0]), (upper_lip[1] - lower_lip[1]))
        
        if mouth_open_ratio > mouth_sensitivity:
            mouth_open = True

    return frame, direction, mouth_open

# Function to reconstruct data from a string
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

# Function to open and read the file containing limits
def file_opener():
    default_data = '0.3,1.7,30.0,170.0,25'
    try:
        with open('limits.txt', 'r') as file:
            data = file.read()
            if data.strip() == '':
                data = default_data
    except FileNotFoundError:
        with open('limits.txt', 'w') as file:
            file.write(default_data)
        data = default_data

    data_list = data_reconstructor(data)
    
    # Ensure data_list has the correct number of elements
    if len(data_list) != 5:
        data_list = data_reconstructor(default_data)
    
    return data_list

# Function to save the current limits to a file
def file_saver(horizontal_ratios, vertical_ratios, mouth_sensitivity):
    ratios = horizontal_ratios + vertical_ratios + [mouth_sensitivity]
    ratios = [str(i) for i in ratios]
    data = ','.join(ratios)
    with open('limits.txt', 'w') as file:
        file.write(data)

# Main GUI function
def main_gui(lower_h, upper_h, lower_v, upper_v, mouth_sensitivity):
    default_values = [0.3, 1.7, 30.0, 170.0, 25]
    sg.theme('DarkBlue17')

    starting_horizontal_ratios_string = [str((lower_h / default_values[0]) * 100), str((upper_h / default_values[1]) * 100)]
    starting_vertical_ratios_string = [str((lower_v / default_values[2]) * 100), str((upper_v / default_values[3]) * 100)]
    starting_mouth_sensitivity_string = str((mouth_sensitivity / default_values[4]) * 100)

    horizontal_ratios = [lower_h, upper_h]
    vertical_ratios = [lower_v, upper_v]

    layout = [
        [sg.Text('Eye Tracking Calibration', size=(30, 1), justification='center', font=("Helvetica", 25))],
        [sg.Image(filename='', key='-IMAGE-')],
        [sg.Column([
            [sg.Text('Horizontal Limits', font=("Helvetica", 15))],
            [sg.Text('Left limit:', size=(10, 1)), sg.InputText(starting_horizontal_ratios_string[0], key='-IHLOWER-', size=(10, 1))],
            [sg.Text('Right limit:', size=(10, 1)), sg.InputText(starting_horizontal_ratios_string[1], key='-IHUPPER-', size=(10, 1))]
        ]), 
        sg.VSeparator(), 
        sg.Column([
            [sg.Text('Vertical Limits', font=("Helvetica", 15))],
            [sg.Text('Down limit:', size=(10, 1)), sg.InputText(starting_vertical_ratios_string[0], key='-IVLOWER-', size=(10, 1))],
            [sg.Text('Up limit:', size=(10, 1)), sg.InputText(starting_vertical_ratios_string[1], key='-IVUPPER-', size=(10, 1))]
        ]),
        sg.VSeparator(),
        sg.Column([
            [sg.Text('Mouth Sensitivity', font=("Helvetica", 15))],
            [sg.Text('Sensitivity:', size=(10, 1)), sg.InputText(starting_mouth_sensitivity_string, key='-MOUTH-', size=(10, 1))]
        ])],
        [sg.Button('Save', size=(10, 1)), sg.Button('Exit', size=(10, 1))]
    ]

    window = sg.Window("Calibration Interface", layout, size=(800, 700), element_justification='center')

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
            mouth_sensitivity = default_values[4] * (float(values['-MOUTH-']) / 100)
            file_saver(horizontal_ratios, vertical_ratios, mouth_sensitivity)
        
        # Webcam feed update
        frame, direction, mouth_open = detect_gaze_and_mouth(vertical_ratios[1], vertical_ratios[0], horizontal_ratios[1], horizontal_ratios[0], mouth_sensitivity)
        frame = overlay_arrows_and_mouth_indicator(frame, direction, mouth_open)
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)

    window.close()

if __name__ == '__main__':
    data = file_opener()
    main_gui(data[0], data[1], data[2], data[3], data[4])
