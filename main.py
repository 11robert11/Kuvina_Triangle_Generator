import colorsys
import random

import pygame
from pygame import Rect


###
# Kuvina Triangle - Kuvina Saydaki
# Demos from How I made my own Fractal - Kuvina Saydaki
# To play with settings scroll to the bottom of the code.
# To see compute function options look bellow "define cell calculation functions"
###

def pos_to_index(x, y):
    if y > cellHeight or y < 0:
        return -1
    if x > cellWidth or x < 0:
        return -1
    return (y * cellHeight) + x


def run():
    cell_display_width = displayWidth / cellWidth
    cell_display_height = displayHeight / cellHeight

    cells: list[int] = list()  # Continues center and everything nto the right

    pygame.init()
    display = pygame.display.set_mode((displayWidth, displayHeight))

    display.fill((0, 0, 0))

    # initialize cells
    for i in range(cellWidth * cellHeight):
        cells.append(defaultFill)

    # seed cell
    cells[seedIndex] = nucleationValue

    # compute
    for y in range(cellHeight):
        for x in range(cellWidth):
            cells[pos_to_index(x, y)] += compute_function(x, y, cells)

    # draw
    for rowNum in range(cellHeight):
        for colNum in range(cellWidth):
            workingIndex = (rowNum * cellWidth) + colNum
            val = cells[workingIndex]
            if val > 0:
                color = colorsys.hsv_to_rgb((val + hue_offset - 1) / (mod - 1), saturation, 255)
            else:
                color = background_color

            # color = colorsys.hls_to_rgb((val % mod) / mod, 255, 1)
            # colorI = (int(color[0]), int(color[1]), int(color[2]))

            pygame.draw.rect(display,
                             color,
                             Rect(cell_display_width * colNum,
                                  cell_display_height * rowNum,
                                  displayWidth,
                                  displayHeight))

    while True:
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


# define cell calculation functions
def compute_random(rowNum, colNum, cells) -> int:
    return 1 + random.random() * mod


def compute_standard(x, y, cells: list[int]) -> int:
    v = 0
    a = pos_to_index(x - 1, y - 1)
    b = pos_to_index(x, y - 1)
    c = pos_to_index(x + 1, y - 1)
    if a >= 0:
        v += cells[a]
    if b >= 0:
        v += cells[b]
    if c >= 0:
        v += cells[c]
    return v % mod


def compute_shadow(x, y, cells: list[int]) -> int:
    v = 0
    a = pos_to_index(x - 1, y - 1)
    b = pos_to_index(x, y - 1)
    c = pos_to_index(x + 1, y - 1)
    if a >= 0:
        v += cells[a]
    if b >= 0:
        v -= cells[b]
    if c >= 0:
        v += cells[c]
    return v % mod


def compute_bi(x, y, cells: list[int]) -> int:
    v = 0
    a = pos_to_index(x - 1, y - 1)
    c = pos_to_index(x + 1, y - 1)
    if a >= 0:
        v += cells[a]
    if c >= 0:
        v += cells[c]
    return v % mod


def compute_bi_skew_l(x, y, cells: list[int]) -> int:
    v = 0
    a = pos_to_index(x - 1, y - 1)
    b = pos_to_index(x, y - 1)
    if a >= 0:
        v += cells[a]
    if b >= 0:
        v += cells[b]
    return v % mod


def compute_bi_skew_r(x, y, cells: list[int]) -> int:
    v = 0
    b = pos_to_index(x, y - 1)
    c = pos_to_index(x + 1, y - 1)
    if b >= 0:
        v += cells[b]
    if c >= 0:
        v += cells[c]
    return v % mod


def compute_standard_psych(x, y, cells: list[int]) -> int:
    v = 1
    a = pos_to_index(x - 1, y - 1)
    b = pos_to_index(x, y - 1)
    c = pos_to_index(x + 1, y - 1)
    if a >= 0:
        v += cells[a]
    if b >= 0:
        v += cells[b]
    if c >= 0:
        v += cells[c]
    return v % mod

def compute_robert_1(x, y, cells: list[int]) -> int:
    v = 0
    a = pos_to_index(x - 1, y - 1)
    b = pos_to_index(x, y - 1)
    c = pos_to_index(x + 1, y - 1)
    d = pos_to_index(x, y - 2)
    if a >= 0:
        v += cells[a]
    if b >= 0:
        v += cells[b]
    if c >= 0:
        v += cells[c]
    if d >= 0:
        v += cells[d]
    return v % mod

def compute_robert_2(x, y, cells: list[int]) -> int:
    v = 0
    a = pos_to_index(x - 1, y - 1)
    b = pos_to_index(x, y - 1)
    c = pos_to_index(x + 1, y - 1)
    d = pos_to_index(x, y - 2)
    e = pos_to_index(x + 2, y - 2)

    if a >= 0:
        v += cells[a]*2
    if b >= 0:
        v += cells[b]
    if c >= 0:
        v += cells[c]
    if d >= 0:
        v += cells[d]
    if e >= 0:
        v += cells[e]*2
    v //= 2
    return v % mod

# configurables
#########
displayWidth = 900  # Display Width
displayHeight = 900  # Display Height
cellWidth = 100  # 2D array of cell's width
cellHeight = 100  # 2D array of cell's height
mod = 3  # modulo
nucleationValue = 1  # Value of nucleation cell
defaultFill = 0  # Default Cell Value
seedIndex = cellWidth // 2  # Index of nucleation cell, default is center of first row
background_color = (25, 25, 25)
saturation = 1.0
hue_offset = 0.0
compute_function = compute_standard
#########

run()
