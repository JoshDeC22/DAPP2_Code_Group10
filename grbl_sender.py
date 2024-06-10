import serial
import time
import inverse_kinematics
import math

def open_grbl(port_name, baudrate=115200):
    s = serial.Serial(port_name, baudrate)
    s.write("\r\n\r\n".encode())
    time.sleep(2)
    s.reset_input_buffer()
    
    return s

def close_grbl(serial_port):
    serial_port.reset_input_buffer()
    serial_port.close()
    
def send_command(horizontal_gaze_ratio, vertical_gaze_ratio, voice_command, s, is_moving):
    if is_moving == True:
        gcode = 'G21G91G1' + 'X' + str(horizontal_gaze_ratio) + 'Y' + str(vertical_gaze_ratio) + 'Z' + str(voice_command) + 'F100' + '\n'
        s.write(gcode.encode())
        #print(gcode)

if __name__ == '__main__':
    port = open_grbl('COM9')

    step = inverse_kinematics.inverse_kin_angles(-math.pi / 4)

    send_command(step, 0, 0, port, True)

    close_grbl(port)
