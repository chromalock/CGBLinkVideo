
from util import square
from util.gen_tiles import get_tile_indexes


def to_bw(ndarray, threshold):
    output = b""
    for row in ndarray:
        for pixel in row:
            output += b"\x00" if pixel[0] > threshold else b"\xff"
    return output


def encode_frame_simple(frame):
    if len(frame) != 36 or len(frame[0]) != 40:
        raise "video must be 40x36 for simple encoding"

    result = b""
    for row in get_tile_indexes(frame):
        for col in row:
            result += col.to_bytes(1, "big")

    return result
