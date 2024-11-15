# Converts an image into a tilemap and tiles

import py.video.util as util
import sys
import os
import cv2
import numpy as np
import copy

path = sys.argv[1]
output = sys.argv[2]

if path is None:
    print("No path supplied")
    exit(1)

if output is None:
    print("No output provided")
    exit(1)


os.makedirs(output, exist_ok=True)
os.makedirs(output + "/tiles", exist_ok=True)
os.makedirs(output + "/frames", exist_ok=True)


def clamp(f: float, s: int) -> int:
    return round(f * s)


tile_size = 2
tile_n = 0
tile_output = dict()

tiles = dict()


def tile_to_image(tile_data):
    result = copy.deepcopy(tile_data)
    for (yi, y) in enumerate(tile_data):
        for (xi, x) in enumerate(y):
            result[yi][xi] = [x/1*255 for _ in range(0, 3)]
    result = np.array(result)
    return cv2.resize(result, (8, 8), interpolation=cv2.INTER_NEAREST_EXACT)


def bits_to_byte(s: list[int]) -> int:
    return int("".join([str(x) for x in s]), 2)


def tile_to_2bpp(tile_image):
    grey = cv2.cvtColor(np.uint8(tile_image), cv2.COLOR_RGB2GRAY)//85
    lo = np.bitwise_and(1, np.copy(grey))
    hi = np.right_shift(np.bitwise_and(0b10, np.copy(grey)), 1)
    output = []
    for i in range(0, 8):
        output.append(bits_to_byte(hi[i]))
        output.append(bits_to_byte(lo[i]))

    return bytes(output)


def get_tile_no(tile_data: list[list[int]]) -> int:
    global tile_n
    k = tuple([x for y in tile_data for x in y])
    if k in tile_output:
        return tile_output[k]
    else:
        tile_output[k] = tile_n
        tile_n += 1
        return tile_n - 1


total_file = f"{output}/video.hex"
tiles_file = f"{output}/tiles.2bpp"

tile_bpp = dict()

with open(total_file, "w+") as totalf:
    for (iframe, frame) in enumerate(util.video_frames(path)):
        img = frame/255
        y = len(img)
        x = len(img[0])
        tile_x = x//tile_size
        tile_y = y//tile_size

        if y % tile_size or x % tile_size:
            print(
                f"error: image dimensions are not integer multiples of tile factor: {tile_size =} {x =} {y =}")
            exit(1)

        tile_map = [[0 for _ in range(0, tile_x)] for _ in range(0, tile_y)]

        print(iframe)
        for yi in range(0, tile_y):
            for xi in range(0, tile_x):
                tile = [[clamp(sum(p)/3, 1) for p in ytile[(xi * tile_size):((xi + 1) * tile_size)]]
                        for ytile in img[(yi * tile_size):((yi + 1) * tile_size)]]
                tile_number = get_tile_no(tile)
                tile_map[yi][xi] = tile_number

                outpath = output + f"/tiles/{tile_number}.png"
                if not os.path.exists(outpath):
                    output_tile_img = tile_to_image(tile)
                    bpp2 = tile_to_2bpp(output_tile_img)
                    tile_bpp[tile_number] = bpp2
                    cv2.imwrite(outpath, output_tile_img)

        for y in tile_map:
            for x in y:
                totalf.write(str(x) + " ")


print("tiles generated:", tile_n)

with open(tiles_file, "wb") as fff:
    for i in range(0, tile_n):
        fff.write(tile_bpp[i])
