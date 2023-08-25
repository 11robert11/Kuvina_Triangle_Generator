import cProfile
import colorsys
import random
import time

import numpy

import png


###
# Kuvina Triangle - Kuvina Saydaki
# Demos from How I made my own Fractal - Kuvina Saydaki
# To play with settings scroll to the bottom of the code.
# To see compute function options look bellow "define cell calculation functions"
###

def run():
    # Initilize cells
    row_holder = defaultFill * numpy.ones((cellHeight, cellWidth))

    # seed cell
    row_holder[0][seedIndex] = nucleationValue

    # compute
    precomp = time.time_ns()
    for y in range(cellHeight):
        for x in range(cellWidth):
            # val = row_holder[y][x]
            # val += compute_function(x, y, row_holder)
            # row_holder[y][x] = val % mod

            row_holder[y][x] += compute_function(x, y, row_holder)
            row_holder[y][x] %= mod

    print((time.time_ns() - precomp) / 1000000000)
    # HSV conversion cache
    val_color_table: dict[int: tuple[int, int, int]] = dict()
    for i in range(-mod, mod):
        color = colorsys.hsv_to_rgb((i - hue_offset) / (mod - hue_offset), saturation, 255)
        val_color_table[i] = (int(color[0]), int(color[1]), int(color[2]))

    # Generate Pixel Buffer
    # pixel_buffer: list[list[int]] = list()
    pixel_buffer = numpy.ndarray((cellHeight, cellWidth * 3), dtype=int)

    for working_row_index in range(cellHeight):
        g = 0
        for working_col_index in range(cellWidth):
            val = row_holder[working_row_index][working_col_index]
            if val > 0:
                color = val_color_table.get(val)
            else:
                color = background_color

            pixel_buffer[working_row_index][g] = color[0]
            g += 1
            pixel_buffer[working_row_index][g] = color[1]
            g += 1
            pixel_buffer[working_row_index][g] = color[2]
            g += 1

    f = open(output_file, 'wb')
    w = png.Writer(width=cellWidth, height=cellHeight, greyscale=False)
    w.write(f, pixel_buffer.tolist())
    f.close()


def wrap_around(x, width) -> int:
    if x > width:
        return -x + width
    return x


# define cell calculation functions
def compute_random(x, y, row_holder) -> int:
    return int(1 + random.random() * 254)


def compute_standard(x, y, row_holder: list[list[int]]) -> int:
    v = psychedelic_offset
    if y - 1 >= 0:
        prev_row = row_holder[y - 1]
        if x - 1 >= 0:
            v += prev_row[x - 1]
        if x >= 0:
            v += prev_row[x]
        if x + 1 < cellWidth:
            v += prev_row[x + 1]
    return v % mod
    # return v


def compute_standard_cylidner_space(x, y, row_holder: list[list[int]]) -> int:
    v = psychedelic_offset

    prev_row = row_holder[y - 1]
    v += prev_row[x - 1]
    v += prev_row[x]
    v += prev_row[wrap_around(x + 1, cellWidth - 1)]
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
cellWidth = 256 * 6  # 2D array of cell's width
cellHeight = 256 * 4  # 2D array of cell's height
mod = 5  # modulo
psychedelic_offset = 1
nucleationValue = 1  # Value of nucleation cell
defaultFill = 0  # Default Cell Value
seedIndex = cellWidth // 2  # Index of nucleation cell, default is center of first row
background_color = (50, 50, 50)  # (0-255, 0-255, 0-255)
saturation = 1  # 0.0-1.0
hue_offset = .9  # 0.0, 1.0
compute_function = compute_shadow
output_file = "fractal.png"
#########

# cProfile.run("run()", "my_func_stats")

# p = pstats.Stats("my_func_stats")
# p.sort_stats("cumulative").print_stats()

run()
