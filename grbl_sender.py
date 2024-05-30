import serial
import time

def open_grbl(port_name, baudrate):
    s = serial.Serial(port_name, baudrate)

    s.write("\r\n\r\n".encode())
    time.sleep(2)
    s.reset_input_buffer()
    
    return s

def close_grbl(serial_port, file):
    serial_port.close()
    
def send_command(voice_command, vertical_gaze_ratio, horizontal_gaze_ratio, s):
    gcode = 'G21G91G1' + 'X' + str(horizontal_gaze_ratio) + 'Y' + str(vertical_gaze_ratio) + 'Z' + str(voice_command) + 'F10' + '\n'
    s.write(gcode.encode())
    
    
    
    
    