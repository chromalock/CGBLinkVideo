import argparse
import math
import numpy as np

from py.util import permutations


def get_color_index(rgb, ncolors):
    return int(round((sum(rgb)/(ncolors - 1))/255 * (ncolors - 1)))


def get_tile_indexes(frame):
    # tile_index = bottom_right + bottom_left*4 + top_right*16 + top_left*64
    indexes = [[0 for _ in range(20)] for _ in range(18)]
    for y in range(len(frame)//2):
        for x in range(len(frame[0])//2):
            tl = get_color_index(frame[y*2][x*2], 4)
            tr = get_color_index(frame[y*2][x*2+1], 4)
            bl = get_color_index(frame[y*2+1][x*2], 4)
            br = get_color_index(frame[y*2+1][x*2+1], 4)
            tile_index = br + bl * 4 + tr * 16 + tl * 64
            indexes[y][x] = tile_index
    return indexes


def gentiles(color_index: int, tile_width: int):
    ntiles = color_index**(tile_width*tile_width)

    tile_w = 16
    tile_h = 16

    output_height = int(8 * math.sqrt(ntiles))
    output_width = int(8 * math.sqrt(ntiles))
    output_tiles = np.zeros((output_width, output_height, 3), np.uint8)

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

            for (pixel_x, pixel_y) in np.square(real_x, real_y, 4, 4):
                output_tiles[pixel_y][pixel_x] = color3

    return output_tiles
