import copy
import numpy as np
import random
from PIL import Image

INFERNO_X = 29
INFERNO_Y = 28
IMG_SCALE_FACTOR = 80

PILLAR_COLOUR = (0, 0, 0)
BAT_COLOUR = (0, 100, 0)
BLOB_COLOUR = (157, 29, 173)
MELEE_COLOUR = (200, 0, 0)
RANGE_COLOUR = (0, 220, 0)
MAGE_COLOUR = (0, 0, 220)

# Colour, size
BAT = (BAT_COLOUR, 2)
BLOB = (BLOB_COLOUR, 3)
MELEE = (MELEE_COLOUR, 4)
RANGER = (RANGE_COLOUR, 3)
MAGER = (MAGE_COLOUR, 4)

INFERNO_BG_GREYSCALE = 75
INFERNO_GRID_COLOUR = (60, 60, 60)

# Pillar coordiantes
pillars = [
    (0, 9),
    (17, 7),
    (10, 21)
]

# Spawn coordinates
spawns = [
    (1, 5),
    (22, 5),
    (3, 11),
    (23, 12),
    (16, 17),
    (5, 21),
    (23, 23),
    (1, 26),
    (15, 26)
]

inferno_grid = np.zeros((INFERNO_X, INFERNO_Y, 3))


def colour_inferno_cell(x, y, rgb, arr):
    x_start = x * IMG_SCALE_FACTOR
    y_start = y * IMG_SCALE_FACTOR
    for _x in range(IMG_SCALE_FACTOR):
        for _y in range(IMG_SCALE_FACTOR):
            arr[y_start + _y][x_start + _x] = rgb


def colour_inferno_cells(x, y, size, rgb, arr):
    """
    :param x: SW x of square
    :param y: SW y of square
    :param size: size of square
    """
    for _x in range(size):
        for _y in range(size):
            colour_inferno_cell(x + _x, y - _y, rgb, arr)


def draw_inferno_cell_top_border(x, y, rgb, thickness, arr):
    for _x in range(IMG_SCALE_FACTOR):
        for _y in range(thickness):
            arr[y * IMG_SCALE_FACTOR + _y][x * IMG_SCALE_FACTOR + _x] = rgb


def draw_inferno_cell_bottom_border(x, y, rgb, thickness, arr):
    for _x in range(IMG_SCALE_FACTOR):
        for _y in range(thickness):
            arr[y * IMG_SCALE_FACTOR + IMG_SCALE_FACTOR - _y - 1][x * IMG_SCALE_FACTOR + _x] = rgb


def draw_inferno_cell_left_border(x, y, rgb, thickness, arr):
    for _x in range(thickness):
        for _y in range(IMG_SCALE_FACTOR):
            arr[y * IMG_SCALE_FACTOR + _y][x * IMG_SCALE_FACTOR + _x] = rgb


def draw_inferno_cell_right_border(x, y, rgb, thickness, arr):
    for _x in range(thickness):
        for _y in range(IMG_SCALE_FACTOR):
            arr[y * IMG_SCALE_FACTOR + _y][x * IMG_SCALE_FACTOR + IMG_SCALE_FACTOR - _x - 1] = rgb


def outline_inferno_cells(x, y, size, rgb, thickness, arr):
    """
    :param x: SW x of square
    :param y: SW y of square
    :param size: size of square
    """
    for _x in range(size):
        draw_inferno_cell_top_border(x + _x, y - size + 1, rgb, thickness, arr)
        draw_inferno_cell_bottom_border(x + _x, y, rgb, thickness, arr)

    for _y in range(size):
        draw_inferno_cell_left_border(x, y - _y, rgb, thickness, arr)
        draw_inferno_cell_right_border(x + size - 1, y - _y, rgb, thickness, arr)


def draw_pillars(pillar_coordinates, arr):
    for coord in pillar_coordinates:
        _x, _y = coord
        colour_inferno_cells(_x, _y, 3, PILLAR_COLOUR, arr)


def draw_grid(arr):
    for x in range(INFERNO_X):
        for y in range(INFERNO_Y):
            outline_inferno_cells(x, y, 1, INFERNO_GRID_COLOUR, 5, arr)


def draw_spawns(spawns, arr):
    for spawn in spawns:
        print(spawn)
        x, y = spawn
        outline_inferno_cells(x, y, 4, (255, 0, 0), 5, arr)


def get_wave_npcs(wave):
    if wave > 66 or wave < 1:
        return []
    current_npc_counts = [0, 0, 0, 0, 1]
    return_npc_counts = [0, 0, 0, 0, 1]
    nibbler_wave = False
    for i in range(1, wave):
        if nibbler_wave:
            nibbler_wave = False
            return_npc_counts = copy.deepcopy(current_npc_counts)
            continue
        if 2 in current_npc_counts:
            idx = current_npc_counts.index(2)
            current_npc_counts[idx - 1] += 1
            current_npc_counts[idx] = 0
            if 1 not in return_npc_counts:
                nibbler_wave = True
                return_npc_counts = [0, 0, 0, 0, 0]
                continue
        else:
            current_npc_counts[4] += 1
        return_npc_counts = copy.deepcopy(current_npc_counts)

    npc_list = []
    for i in range(return_npc_counts[4]):
        npc_list.append(BAT)
    for i in range(return_npc_counts[3]):
        npc_list.append(BLOB)
    for i in range(return_npc_counts[2]):
        npc_list.append(MELEE)
    for i in range(return_npc_counts[1]):
        npc_list.append(RANGER)
    for i in range(return_npc_counts[0]):
        npc_list.append(MAGER)

    return npc_list


base_gridded_image = np.zeros((INFERNO_Y * IMG_SCALE_FACTOR, INFERNO_X * IMG_SCALE_FACTOR, 3),
                              dtype=np.uint8) + INFERNO_BG_GREYSCALE
draw_grid(base_gridded_image)
draw_pillars(pillars, base_gridded_image)


def create_image(wave):
    data = copy.deepcopy(base_gridded_image)
    these_spawns = list(range(9))
    random.shuffle(these_spawns)
    npcs = get_wave_npcs(wave)

    for i, npc in enumerate(npcs):
        x, y = spawns[these_spawns[i]]
        colour, size = npc
        colour_inferno_cells(x, y, size, colour, data)

    draw_spawns(spawns, data)

    img = Image.fromarray(data, "RGB")
    del data
    return img
