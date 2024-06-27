from math import pi, sin, cos
import numpy as np

FRAME_X = 100
FRAME_Y = 100

# def scale(x, y, scale_param):
#     x *= scale_param
#     y *= scale_param
#     return round(x), round(y)


def convers(arg):
    return arg * pi / 180


def rotateX(x, y, z, angle):
    angle = convers(angle)
    y = cos(angle) * y - sin(angle) * z
    return x, y


def rotateY(x, y, z, angle):
    angle = convers(angle)
    x = cos(angle) * x - sin(angle) * z
    return x, y


def rotateZ(x, y, z, angle):
    angle = convers(angle)
    buf = x
    x = cos(angle) * x - sin(angle) * y
    y = cos(angle) * y + sin(angle) * buf
    return x, y


def get_scale_param_and_mid(x_min, x_max, x_step, func, z_min, z_max, z_step, angles, width, height):
    width -= FRAME_X
    height -= FRAME_Y
    res_x_min = float('inf')
    res_x_max = -float('inf')
    res_y_min = float('inf')
    res_y_max = -float('inf')

    for z in np.arange(z_max, z_min, -z_step):
        for x in np.arange(x_min, x_max, x_step):
            y = func(x, z)
            x, y = rotateX(x, y, z, angles[0])
            x, y = rotateY(x, y, z, angles[1])
            x, y = rotateZ(x, y, z, angles[2])

            res_x_min = x if x < res_x_min else res_x_min
            res_x_max = x if x > res_x_max else res_x_max
            res_y_min = y if y < res_y_min else res_y_min
            res_y_max = y if y > res_y_max else res_y_max
    print('res: ', res_x_min, res_x_max, res_y_min, res_y_max)

    scale_param = min(width / (res_x_max - res_x_min), height / (res_y_max - res_y_min))
    x_mid = res_x_min * scale_param
    y_mid = res_y_min * scale_param
    x_mid -= FRAME_X // 2 + (width - (res_x_max - res_x_min) * scale_param) // 2
    y_mid -= FRAME_Y // 2 + (height - (res_y_max - res_y_min) * scale_param) // 2


    # x_mid = min(0, res_x_min)
    # y_mid = min(0, res_y_min)

    print('border x:', res_x_min, res_x_max)
    print('border y:', res_y_min, res_y_max)
    print('scale_param: ', scale_param)
    print('(x_mid, y_mid)', (x_mid, y_mid))
    # print('border z:', res_z_min, res_z_max)
    return scale_param, (x_mid, y_mid)


def transform(x, y, z, angles, scale_param, mid, width, height):
    x, y = rotateX(x, y, z, angles[0])
    x, y = rotateY(x, y, z, angles[1])
    x, y = rotateZ(x, y, z, angles[2])
    tx = x * scale_param - mid[0]
    ty = y * scale_param - mid[1]
    # tx += (width - FRAME_X) // 2
    # ty += (height - FRAME_Y) // 2
    # tx -= mid[0] * scale_param
    # ty -= mid[1] * scale_param
    # print(f'transform: {(x, y)} --> {(tx, ty)}')
    return round(tx), round(ty)

