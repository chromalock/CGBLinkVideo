
def to_bw(ndarray, threshold):
    output = b""
    for row in ndarray:
        for pixel in row:
            output += b"\x01" if pixel[0] > threshold else b"\x00"
    return output
