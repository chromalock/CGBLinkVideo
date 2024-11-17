import math
import numpy as np
from util import permutations


def generate_tiles(color_index: int, tile_width: int):
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
