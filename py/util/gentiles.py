import cv2
import argparse
import math
import numpy as np

parser = argparse.ArgumentParser(prog="gentiles.py")
parser.add_argument("-t", default=2, type=int)
parser.add_argument("-c", default=4, type=int)

args = parser.parse_args()

tile_width = 2
color_index = 4

# number of possible tiles:
ntiles = color_index**(tile_width*tile_width)

tile_w = 16
tile_h = 16

output_height = int(8 * math.sqrt(ntiles))
output_width = int(8 * math.sqrt(ntiles))
output_tiles = np.zeros((output_width, output_height, 3), np.uint8)


def permutations(color_depth: int, length: int):
    if length <= 0:
        return []
    elif length == 1:
        return [[x] for x in range(0, color_depth)]
    outputs = []
    for i in range(0, color_depth):
        for child_perm in permutations(color_depth, length - 1):
            outputs.append([i] + child_perm)

    return outputs


def square(x, y, w, h):
    for xi in range(0, w):
        for yi in range(0, h):
            yield (x + xi, y + yi)


for tile_i, tile in enumerate(permutations(color_index, tile_width*tile_width)):
    tile_x = tile_i % tile_w
    tile_y = (tile_i - tile_x) // tile_h

    for data_i, tile_data in enumerate(tile):
        data_x = data_i % tile_width
        data_y = (data_i - data_x) // tile_width

        color = round(tile_data * 255/(color_index - 1))
        color3 = (color, color, color)

        real_x = (tile_x * 8) + (data_x * 4)
        real_y = (tile_y * 8) + (data_y * 4)

        for (pixel_x, pixel_y) in square(real_x, real_y, 4, 4):
            output_tiles[pixel_y][pixel_x] = color3


cv2.imwrite("./tiles.png", output_tiles)
