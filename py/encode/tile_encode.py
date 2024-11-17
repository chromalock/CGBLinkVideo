from util import clamp
import numpy as np
import cv2
import copy


def bits_to_byte(s: list[int]) -> int:
    return int("".join([str(x) for x in s]), 2)


def get_color_index(rgb, ncolors: int):
    return int(round((sum(rgb)/(ncolors - 1))/255 * (ncolors - 1)))


def get_2bpp_bytes(pixels: list[int] | bytearray | bytes):
    a = 0x00
    b = 0x00
    for i in range(0, 8):
        a |= (((pixels[i] & 0x40) << 1) >> i)
        b |= ((pixels[i] & 0x80) >> i)
    return [a, b]


def getTile(i, data):
    x = i % 20
    y = i // 20
    out = []
    for j in range(0, 8):
        start = x*8 + (y*8+j)*160
        out.extend(get_2bpp_bytes(data[start:start+8]))
    return out


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


def tile_to_2bpp(tile_image):
    grey = cv2.cvtColor(np.uint8(tile_image), cv2.COLOR_RGB2GRAY)//85
    lo = np.bitwise_and(1, np.copy(grey))
    hi = np.right_shift(np.bitwise_and(0b10, np.copy(grey)), 1)
    output = b""
    for i in range(0, 8):
        output += bits_to_byte(hi[i]).to_bytes(1, "big") + \
            bits_to_byte(lo[i]).to_bytes(1, "big")

    return output


def tile_to_image(tile_data):
    result = copy.deepcopy(tile_data)
    for (yi, y) in enumerate(tile_data):
        for (xi, x) in enumerate(y):
            result[yi][xi] = [x/1*255 for _ in range(0, 3)]
    result = np.array(result)
    return cv2.resize(result, (8, 8), interpolation=cv2.INTER_NEAREST_EXACT)


def extract_tiles(frame, tile_size=8):
    img = frame/255
    height = len(img)
    width = len(img[0])
    tiles_w = width//tile_size
    tiles_h = height//tile_size

    if height % tile_size or width % tile_size:
        raise Exception(
            f"error: image dimensions are not integer multiples of tile factor: {tile_size =} {width =} {height =}")

    for yi in range(0, tiles_h):
        for xi in range(0, tiles_w):
            tile = [[clamp(sum(p)/3, 1) for p in ytile[(xi * tile_size):((xi + 1) * tile_size)]]
                    for ytile in img[(yi * tile_size):((yi + 1) * tile_size)]]
            output_tile_img = tile_to_image(tile)
            bpp2 = tile_to_2bpp(output_tile_img)
            yield from iter(bpp2)


def to_bw(ndarray, threshold):
    for row in ndarray:
        for pixel in row:
            yield b"\x00" if pixel[0] > threshold else b"\xff"


def to_grey(frame):
    for row in get_tile_indexes(frame):
        for col in row:
            yield bytearray(col.to_bytes(1, "big"))


def encode_frame_simple(frame):
    h = len(frame)
    w = len(frame[0])
    if h == 18 and w == 20:
        return b"".join(to_bw(frame, 128))
    elif h == 36 and w == 40:
        return b"".join(to_grey(frame))
    else:
        raise "video must be 40x36 or 20x18 for simple encoding"
