import math as mt

def get_original_position(filename='position.txt'):
    file = open(filename, 'r')
    data = file.read()
    data = data.split(',')
    x, y = data[0:2]
    x_limits = data[2:4]
    x_limits = [int(i) for i in x_limits]
    y_limits = data[4:6]
    y_limits = [int(i) for i in y_limits]
    file.close()
    return float(x), float(y), x_limits, y_limits

def save_position(x, y, x_limits, y_limits, filename='position.txt'):
    x_limits = [str(i) for i in x_limits]
    y_limits = [str(i) for i in y_limits]
    data = ','.join([str(x), str(y)]) + ',' + ','.join(x_limits) + ',' + ','.join(y_limits)
    file = open(filename, 'w')
    file.write(data)
    file.close()

def get_angles(x, y, l1=10.0, l2=10.0):
    cos_theta2 = (x**2 + y**2 - (l1**2 + l2**2)) / (2 * l1 * l2)
    cos_theta2 = min(max(cos_theta2, -1), 1)
    theta2 = mt.acos(cos_theta2)
    theta1 = mt.atan(x / y) - mt.atan((l2 * mt.sin(theta2)) / (l1 + l2 * mt.cos(theta2)))
    theta2 = (-1) * theta2
    theta1 = (mt.pi / 2) - theta1
    return theta1, theta2
    
def inverse_kin(x, y, x_limits, y_limits, horizontal_gaze_ratio, vertical_gaze_ratio, theta1tosteps=(1/(1.8 * (mt.pi/180))), theta2tosteps=(1/(1.8 * (mt.pi/180))), l1=10.0, l2=10.0):
    new_x = x + horizontal_gaze_ratio
    new_y = y + vertical_gaze_ratio
    if int(x) < x_limits[0] or int(x) > x_limits[1]:
        new_x = x
    if int(y) < y_limits[0] or int(y) > y_limits[1]:
        new_y = y
    theta1, theta2 = get_angles(x, y)
    new_theta1, new_theta2 = get_angles(new_x, new_y)
    diff_theta1 = new_theta1 - theta1
    diff_theta2 = new_theta2 - theta2
    num_steps1 = (int(diff_theta1 * theta1tosteps * 1000)/1000) / 250
    num_steps2 = (int(diff_theta2 * theta2tosteps * 1000)/1000) / 250
    return num_steps1, num_steps2, new_x, new_y

if __name__ == '__main__':
    save_position(10.0, 10.0, [0, 20], [0, 20])
