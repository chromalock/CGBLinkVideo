def bits_to_byte(s: list[int]) -> int:
    return int("".join([str(x) for x in s]), 2)


def get_color_index(rgb, ncolors: int):
    return 3 - int(round((sum(rgb)/(ncolors - 1))/255 * (ncolors - 1)))


def get_2bpp_bytes(pixels):
    a = 0x00
    b = 0x00
    for i in range(0, 8):
        a |= (((pixels[i] & 0x40) << 1) >> i)
        b |= ((pixels[i] & 0x80) >> i)
    result = bytearray([a, b])
    return result


def tile_index_to_xy(tile_idx):
    x = tile_idx % 16
    y = tile_idx // 16

    real_x = x * 8
    real_y = y * 8

    return (int(real_x), int(real_y))


def get_buffer_tile(image, tile_idx, w, h):
    x = tile_idx % w
    y = tile_idx // w
    out = []
    for j in range(0, 8):
        start = x*8 + (y*8+j)*(8 * w)
        out.extend(get_2bpp_bytes(image[start:start+8]))
    return out


def get_tile(image, tile_idx):
    x, y = tile_index_to_xy(tile_idx)
    for row in range(0, 8):
        yield from get_2bpp_bytes([round(sum(x)/3) for x in image[y + row][x:x+8]])


def get_buffer_tile_data(image, n_tiles, w, h):
    for n in range(0, n_tiles):
        yield from get_buffer_tile(image, n, w, h)


def tile_data(image, n_tiles):
    for n in range(0, n_tiles):
        yield from get_tile(image, n)


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
