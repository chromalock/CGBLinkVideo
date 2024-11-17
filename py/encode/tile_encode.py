def bits_to_byte(s: list[int]) -> int:
    return int("".join([str(x) for x in s]), 2)


def get_color_index(rgb, ncolors: int):
    return 3 - int(round((sum(rgb)/(ncolors - 1))/255 * (ncolors - 1)))


def get_2bpp_bytes(pixels: list[int] | bytearray | bytes):
    a = 0x00
    b = 0x00
    for i in range(0, 8):
        a |= (((pixels[i] & 0x40) << 1) >> i)
        b |= ((pixels[i] & 0x80) >> i)
    return [a, b]


def tile_index_to_xy(tile_idx):
    x = tile_idx % 20
    y = tile_idx // 20

    real_x = x * 8
    real_y = y * 8

    return (real_x, real_y)


def get_tile(image, tile_idx):
    x, y = tile_index_to_xy(tile_idx)
    for row in range(0, 8):
        yield from get_2bpp_bytes(image[y + row][x:x+8])


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
