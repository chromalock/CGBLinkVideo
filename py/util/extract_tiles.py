# Converts an image into a tilemap and tiles

import video.util as util
from util import clamp, tile_to_2bpp, tile_to_image


def extract_tiles_from_video(path: str, tile_n: int):
    tile_bpp = dict()

    tile_size = 2
    tile_output = dict()

    def get_tile_no(tile_data: list[list[int]]) -> int:
        k = tuple([x for y in tile_data for x in y])
        if k in tile_output:
            return tile_output[k]
        else:
            tile_output[k] = tile_n
            tile_n += 1
            return tile_n - 1

    for (iframe, frame) in enumerate(util.video_frames(path)):
        img = frame/255
        y = len(img)
        x = len(img[0])
        tile_x = x//tile_size
        tile_y = y//tile_size

        if y % tile_size or x % tile_size:
            raise f"error: image dimensions are not integer multiples of tile factor: {tile_size =} {x =} {y =}"

        tile_map = [[0 for _ in range(0, tile_x)] for _ in range(0, tile_y)]

        for yi in range(0, tile_y):
            for xi in range(0, tile_x):
                tile = [[clamp(sum(p)/3, 1) for p in ytile[(xi * tile_size):((xi + 1) * tile_size)]]
                        for ytile in img[(yi * tile_size):((yi + 1) * tile_size)]]
                tile_number = get_tile_no(tile)
                tile_map[yi][xi] = tile_number

                output_tile_img = tile_to_image(tile)
                bpp2 = tile_to_2bpp(output_tile_img)
                # the tile_bpp array holds all the tiles
                tile_bpp[tile_number] = bpp2
                yield output_tile_img
