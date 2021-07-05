#!/usr/bin/env python

import sys, argparse

# ==============================================================================


arg = argparse.ArgumentParser()
arg.add_argument ('-f', '--file', required=True, help='input file name (required)')
arg.add_argument ('-o', '--output_file', default='', help='output_file = output file name (if not specified, it will return the code generated)')
arg.add_argument ('-x', '--move_x', default=0, help='move_x = X offset in mm')
arg.add_argument ('-y', '--move_y', default=0, help='move_y = B offset in mm')
arg.add_argument ('-r', '--rotate', default=0, help='rotate = rotate angle (times 90)')
arg.add_argument ('-m', '--mirror', default=0, help='mirror = axis mirroring (axis name)')
arg.add_argument ('-s', '--scale', default=0, help='scale = percentage scale, negative is supported')
arg.add_argument ('-c', '--combine', default=0, help='combine = combine code (example 2x3x10 or 1x2x8 ... where the first number on X is the second number on Y is the third indent) ')
arg.add_argument ('-rd', '--round', default=-1, help='round X and Y value, can be combined with another operation or used alone')
arg.parse_args()


input_file = arg.parse_args().file
output_file = arg.parse_args().output_file
move_x = int(arg.parse_args().move_x)
move_y = int(arg.parse_args().move_y)
rotate = int(arg.parse_args().rotate)
mirror = arg.parse_args().mirror
scale = int(arg.parse_args().scale)
combine = arg.parse_args().combine
roundIt = int(arg.parse_args().round)

# ==============================================================================


with open(input_file) as file:
    comma = ';'
    data = file.read()
    if comma in data:
        data = data.replace(';','')
    else:
        comma = ''

# ==============================================================================


def roundUp(x):
    if roundIt > -1:
        return round(x,roundIt)
    return x

def sizes(i_data):
    max_x = max_y = min_x = min_y = 0

    for row in data.split('\n'):
        for b in row.split():
            if b.find('X') != -1:
                x = float(b.replace('X', ''))
                if x > max_x:
                    max_x = x
                if x < min_x:
                    min_x = x
            if b.find('Y') != -1:
                y = float(b.replace('Y', ''))
                if y > max_y:
                    max_y = y
                if y < min_y:
                    min_y = y
        size_x = max_x - min_x
        size_y = max_y - min_y
    return [max_x, max_y, min_x, min_y, size_x, size_y]

# ==============================================================================


def rotate_data(i_data):
    n_data = ''
    for row in i_data.split('\n'):
        n_row = []
        for b in row.split():
            if b.find('X') != -1:
                n_val = roundUp(-float(b.replace('X', ''))+g_size[4])
                n_b = '{axis}{val}'.format(axis='Y', val=n_val)
            elif b.find('Y') != -1:
                val = b.replace('Y', '')
                n_b = '{axis}{val}'.format(axis='X', val=roundUp(float(val)))
            else:
                n_b = b
            n_row.append(n_b)
        n_data += "{n_r}\n".format(n_r=' '.join(n_row))

    return n_data


if rotate != 0:
    if rotate == -90:
        rotate = 270
    for i in range(int(rotate / 90)):
        g_size = sizes(data)
        data = rotate_data(data)

# ==============================================================================


def mirror_xy(i_data, xy):
    n_data = ''
    for row in i_data.split('\n'):
        n_row = []
        for b in row.split():
            if b.find('X') != -1:
                if xy == 'X':
                    n_val = roundUp(-float(b.replace('X', ''))+g_size[4])
                    n_b = 'X{val}'.format(val=n_val)
            elif b.find('Y') != -1:
                if xy == 'Y':
                    n_val = roundUp(-float(b.replace('Y', ''))+g_size[5])
                    n_b = 'Y{val}'.format(val=n_val)
            else:
                n_b = b
            n_row.append(n_b)
        n_data += "{n_r}\n".format(n_r=' '.join(n_row))

    return n_data


if mirror != 0:
    g_size = sizes(data)
    data = mirror_xy(data, mirror)

# ==============================================================================


def scale_code(i_data, rate):
    rate = float(rate / 100)
    n_data = ''
    for row in i_data.split('\n'):
        n_row = []
        for b in row.split():
            if b.find('X') != -1:
                x = float(b.replace('X', ''))
                n_b = 'X{n_x}'.format(n_x=roundUp((x - g_size[2]) * rate + x))
            elif b.find('Y') != -1:
                y = float(b.replace('Y', ''))
                n_b = 'Y{n_y}'.format(n_y=roundUp((y - g_size[3]) * rate + y))
            else:
                n_b = b
            n_row.append(n_b)
        n_data += "{n_r}\n".format(n_r=' '.join(n_row))
    return n_data


if scale != 0:
    g_size = sizes(data)
    data = scale_code(data, scale)

# ==============================================================================


def move_xy(i_data, x, y):
    n_data = ''
    for row in i_data.split('\n'):
        n_row = []
        for b in row.split():
            if b.find('X') != -1:
                n_b = 'X{v}'.format(v=roundUp(float(b.replace('X', ''))+x))
            elif b.find('Y') != -1:
                n_b = 'Y{v}'.format(v=roundUp(float(b.replace('Y', ''))+y))
            else:
                n_b = b
            n_row.append(n_b)
        n_data += "{n_r}\n".format(n_r=' '.join(n_row))
    return n_data

if move_x != 0 or move_y != 0:
    data = move_xy(data, move_x, move_y)

# ==============================================================================


def combine_gcode(i_data, x, y, offset):
    out_data = ""
    g_size = sizes(data)
    for i in range(int(x)):
        for j in range(int(y)):
            m_x = int((g_size[4] + int(offset)) * i)
            m_y = int((g_size[5] + int(offset)) * j)
            out_data += move_xy(i_data, m_x, m_y)
    if move_x != 0 or move_y != 0:
        out_data = move_xy(data, move_x, move_y)
    return out_data


if combine != 0:
    params=combine.split('x')
    data = combine_gcode(data, params[0], params[1], params[2])


# ==============================================================================

def roundUpOnly(i_data):
    n_data = ''
    for row in i_data.split('\n'):
        n_row = []
        for b in row.split():
            if b.find('X') != -1:
                x = float(b.replace('X', ''))
                n_b = 'X{n_x}'.format(n_x=round(x, roundIt))
            elif b.find('Y') != -1:
                y = float(b.replace('Y', ''))
                n_b = 'Y{n_y}'.format(n_y=round(y, roundIt))
            else:
                n_b = b
            n_row.append(n_b)
        n_data += "{n_r}\n".format(n_r=' '.join(n_row))
    return n_data


if roundIt > -1 and not any(i != 0 for i in [move_x, move_y, rotate, mirror, scale, combine]):
    data = roundUpOnly(data)

# ==============================================================================


if comma:
    data = data.replace('\n', f"{comma}\n").replace('\n;','')
if not output_file:
    print(data)
else:
    with open(output_file, 'w') as file:
        file.write(data)
