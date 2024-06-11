import math as mt

def get_original_position(filename='position.txt'):
    file = open(filename, 'r')
    data = file.read()
    data = data.split(',')
    x, y = data[0:2]
    r = data[2]
    theta1_limits = data[3:5]
    theta1_limits = [int(i) for i in theta1_limits]
    theta2_limits = data[5:7]
    theta2_limits = [int(i) for i in theta2_limits]
    file.close()
    return float(x), float(y), r, theta1_limits, theta2_limits

def save_position(x, y, r, theta1_limits, theta2_limits, filename='position.txt'):
    theta1_limits = [str(i) for i in theta1_limits]
    theta2_limits = [str(i) for i in theta2_limits]
    data = ','.join([str(x), str(y)]) + ',' + str(r) + ',' + ','.join(theta1_limits) + ',' + ','.join(theta2_limits)
    file = open(filename, 'w')
    file.write(data)
    file.close()

def get_angles(x, y, l1=210, l2=210):
    cos_theta2 = (x**2 + y**2 - (l1**2 + l2**2)) / (2 * l1 * l2)
    cos_theta2 = min(max(cos_theta2, -1), 1)
    theta2 = mt.acos(cos_theta2)
    theta1 = mt.atan(x / y) - mt.atan((l2 * mt.sin(theta2)) / (l1 + l2 * mt.cos(theta2)))
    theta2 = (-1) * theta2
    theta1 = (mt.pi / 2) - theta1
    return theta1, theta2
    
def inverse_kin(x, y, horizontal_gaze_ratio, vertical_gaze_ratio, theta1tosteps=(100/mt.pi), theta2tosteps=(100/mt.pi)):
    new_x = x + horizontal_gaze_ratio
    new_y = y + vertical_gaze_ratio
    theta1, theta2 = get_angles(x, y)
    new_theta1, new_theta2 = get_angles(new_x, new_y)
    num_steps1 = ((new_theta1 - theta1) * theta1tosteps) / 12.5
    num_steps2 = ((new_theta2 - theta2) * theta2tosteps) / 12.5
    return num_steps1, num_steps2, new_x, new_y

def inverse_kin_angles(theta1, theta1tosteps=(100/mt.pi)):
    num_steps1 = ((theta1) * theta1tosteps) / 12.5
    return num_steps1

if __name__ == '__main__':
    save_position(0, 429, 429, [0, 180], [-35, 35])
