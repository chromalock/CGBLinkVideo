import cv2
import numpy as np
import copy

from py.util import bits_to_byte, clamp


def chunks(lst: list, n: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


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


def square(x: int, y: int, w: int, h: int):
    for xi in range(0, w):
        for yi in range(0, h):
            yield (x + xi, y + yi)


def clamp(f: float, s: int) -> int:
    return round(f * s)


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


def tile_to_image(tile_data):
    result = copy.deepcopy(tile_data)
    for (yi, y) in enumerate(tile_data):
        for (xi, x) in enumerate(y):
            result[yi][xi] = [x/1*255 for _ in range(0, 3)]
    result = np.array(result)
    return cv2.resize(result, (8, 8), interpolation=cv2.INTER_NEAREST_EXACT)
