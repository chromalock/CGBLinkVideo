import serial

import encode.video as video
import encode.tile_encode as tile
import argparse
import time
import sys

from util import chunks

command = ["ffmpeg",
           '-ss', '0:02:27',
           '-i', 'videos/wifigb.mov',
           '-i', 'palette.png',
           '-filter_complex', '[0:v]crop=1200:1080:360:0,scale=160x144[v0];[v0][1:v]paletteuse[out]',
           '-map', '[out]',
           '-f', 'image2pipe',
           '-pix_fmt', 'gray8',
           '-s', '160x144',
           '-r', '20',
           '-vcodec', 'rawvideo', '-']

print(" ".join(command))

parser = argparse.ArgumentParser("gbstream.py")
parser.add_argument("-p", "--port", required=True)
parser.add_argument("-b", "--baud", default=921600)
parser.add_argument("-i", "--input", default="-")
parser.add_argument("-e", "--encode",  default="tile",
                    choices=["tile", "tile-data", "tile-attr"])

args = parser.parse_args()

port = serial.Serial(args.port, baudrate=args.baud)
port.flush()

encoding = args.encode

ZERO_BUFFER = b"\0"*360


def stdin_buffer(size):
    while True:
        yield sys.stdin.buffer.read(size)


if args.input == "-":
    print('pipe input')
    while True:
        if encoding == "tile-data":
            data = sys.stdin.buffer.read(128*128)
            encoded = bytearray(list(tile.get_buffer_tile_data(data, 256)))
            port.write(encoded)
        elif encoding == "tile":
            data = sys.stdin.buffer.read(40*36)
            img = list(chunks([[px, px, px] for px in data], 40))
            encoded = tile.encode_frame_simple(img)
            port.write(encoded)
else:
    format, extra = video.video_info(args.input)
    width = format.width
    height = format.height
    frames = extra['frames']
    info = f"{args.input} {width}x{height}"

    current_frame = 0
    last_time = time.time()
    toskip = 0
    for frame in video.video_frames(args.input):
        current_time = time.time()
        diff = current_time - last_time
        if toskip > 1:
            toskip -= 1
            continue
        elif toskip == 1:
            last_time = time.time()
            toskip = 0
        if time.time() - last_time > 1.0/30.0:
            toskip = int((time.time() - last_time)/(1.0/30.0))
            continue
        frame_array = frame.to_ndarray()
        if encoding == "tile-data":
            encoded = bytearray(list(tile.tile_data(frame_array, 256)))
            port.write(encoded)
        elif encoding == "tile":
            encoded = tile.encode_frame_simple(frame_array)
            port.write(encoded)
            port.write(encoded)
            # port.write(b"\xaa" + 358 * b"\x00" + b"\xff")
        elif encoding == "tile-attr":
            encoded = tile.encode_frame_simple(frame_array)
            port.write(encoded)
            port.write(ZERO_BUFFER)
            port.write(encoded)
            port.write(ZERO_BUFFER)
        else:
            raise Exception("unknown encoding " + encoding)

        last_time = current_time
        print(
            f"{current_frame}/{frames} | {info} | {round(1/(diff + 0.00000000000001), 2)}fps")

        current_frame += 1
