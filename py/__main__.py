import encode.audio as audio
import encode.video as video


def to_onebit(ndarray, threshold):
    output = b""
    for row in ndarray:
        for pixel in row:
            output += b"\x01" if pixel[0] > threshold else b"\x00"
            print(pixel)


if __name__ == "__main__":
    for frame in video.video_frames("badapple/bad-apple-18x20-stretch.mov"):
        a = frame.to_ndarray()
        onebit = to_onebit(a, 128)
        print(len(a), len(a[0]))
