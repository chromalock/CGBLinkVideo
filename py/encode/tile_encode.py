
def to_bw(ndarray, threshold):
    output = b""
    for row in ndarray:
        for pixel in row:
            output += b"\x00" if pixel[0] > threshold else b"\xff"
    return output


def encode_frame(frame, tiles):
    pass
