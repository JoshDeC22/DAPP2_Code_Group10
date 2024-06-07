import serial
import time

def open_grbl(port_name, baudrate=115200):
    s = serial.Serial(port_name, baudrate)
    s.write("\r\n\r\n".encode())
    time.sleep(2)
    s.reset_input_buffer()
    
    return s

def close_grbl(serial_port):
    serial_port.reset_input_buffer()
    serial_port.close()
    
def send_command(voice_command, vertical_gaze_ratio, horizontal_gaze_ratio, s, is_moving):
    if is_moving == True:
        gcode = 'G21G91G1' + 'X' + str(horizontal_gaze_ratio) + 'Y' + str(vertical_gaze_ratio) + 'Z' + str(voice_command) + 'F100' + '\n'
        s.write(gcode.encode())
        #print(gcode)

if __name__ == '__main__':
    port = open_grbl('COM9', 115200)

    send_command(1, 1, 1, port, True)

    close_grbl(port)
