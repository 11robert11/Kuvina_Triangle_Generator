import colorsys
import random
import time

import numpy as np
import pygame
from pygame import Rect
import png
###
# Kuvina Triangle - Kuvina Saydaki
# Demos from How I made my own Fractal - Kuvina Saydaki
# To play with settings scroll to the bottom of the code.
# To see compute function options look bellow "define cell calculation functions"
###
import png


def run():
    row_holder: list[list[int]] = list()
    for y in range(cellHeight):
        row_holder.append([defaultFill] * cellWidth)

    # seed cell
    row_holder[0][seedIndex] = nucleationValue

    # compute
    for y in range(cellHeight):
        for x in range(cellWidth):
            row_holder[y][x] += compute_function(x, y, row_holder)
            row_holder[y][x] %= mod
            # cells[pos_to_index(x, y)] += compute_function(x, y, cells)
    pixel_buffer = list()
    # Generate Pixel Buffer
    for working_row_index in range(cellHeight):
        pixel_buffer_row = list()
        for working_col_index in range(cellWidth):
            val = row_holder[working_row_index][working_col_index]
            if val > 0:
                color = colorsys.hsv_to_rgb((val - hue_offset) / (mod - hue_offset), saturation, 255)
            else:
                color = background_color
            pixel_buffer_row.append(int(color[0]))
            pixel_buffer_row.append(int(color[1]))
            pixel_buffer_row.append(int(color[2]))

            # color = colorsys.hls_to_rgb((val % mod) / mod, 255, 1)
            # colorI = (int(color[0]), int(color[1]), int(color[2]))
        pixel_buffer.append(pixel_buffer_row)
    f = open('fractal.png', 'wb')
    w = png.Writer(width=cellWidth, height=cellHeight, greyscale=False)
    w.write(f, pixel_buffer)
    f.close()
    post_draw = time.time_ns()


# define cell calculation functions
def compute_random(x, y, row_holder) -> int:
    return int(1 + random.random() * 254)


def compute_standard(x, y, row_holder: list[list[int]]) -> int:
    v = psychedelic_offset
    prev_row = row_holder[y - 1]
    if x - 1 >= 0:
        v += prev_row[x - 1]
    if x >= 0:
        v += prev_row[x]
    if x + 1 < cellWidth:
        v += prev_row[x + 1]
    return v % mod


def compute_test_perimeter(x, y, row_holder: list[list[int]]) -> int:
    if x == 0 or x == cellWidth - 1:
        return 1
    if y == 0 or y == cellHeight - 1:
        return 1
    return 0


def compute_shadow(x, y, row_holder: list[list[int]]) -> int:
    v = psychedelic_offset
    prev_row = row_holder[y - 1]
    if x - 1 >= 0:
        v += prev_row[x - 1]
    if x >= 0:
        v -= prev_row[x]
    if x + 1 < cellWidth:
        v += prev_row[x + 1]
    return v % mod


def compute_bi(x, y, row_holder: list[list[int]]) -> int:
    v = psychedelic_offset
    prev_row = row_holder[y - 1]
    if x - 1 >= 0:
        v += prev_row[x - 1]

    if x + 1 < cellWidth:
        v += prev_row[x + 1]
    return v % mod


def compute_bi_skew_l(x, y, row_holder: list[list[int]]) -> int:
    v = psychedelic_offset
    prev_row = row_holder[y - 1]
    if x - 1 >= 0:
        v += prev_row[x - 1]

    if x < cellWidth:
        v += prev_row[x + 1]
    return v % mod


def compute_bi_skew_r(x, y, row_holder: list[list[int]]) -> int:
    v = psychedelic_offset
    prev_row = row_holder[y - 1]
    if x >= 0:
        v += prev_row[x - 1]

    if x + 1 < cellWidth:
        v += prev_row[x + 1]
    return v % mod


# configurable
#########
cellWidth = 400  # 2D array of cell's width
cellHeight = 500  # 2D array of cell's height
mod = 3  # modulo
psychedelic_offset = 0
nucleationValue = 1  # Value of nucleation cell
defaultFill = 0  # Default Cell Value
seedIndex = cellWidth // 2  # Index of nucleation cell, default is center of first row
background_color = (50, 50, 50)  # (0-255, 0-255, 0-255)
saturation = 1  # 0.0-1.0
hue_offset = 1  # 0.0, 1.0
compute_function = compute_standard
#########

run()
