import serial
import time

import encode.audio as audio
import encode.video as video
import encode.tile_encode as tile
import argparse

parser = argparse.ArgumentParser("gbstream.py")
parser.add_argument("-p", "--port", required=True)
parser.add_argument("-b", "--baud", default=921600)
parser.add_argument("-i", "--input", default="-")
parser.add_argument("-e", "--encode",  default=False, action="store_true")

args = parser.parse_args()

port = serial.Serial(args.port, baudrate=args.baud)
port.flush()

if args.input == "-":
    print('pipe input')
else:
    format, extra = video.video_info(args.input)
    width = format.width
    height = format.height
    frames = extra['frames']
    fps = extra['fps']
    info = f"{args.input} {width}x{height} @ {fps}fps"
    current_frame = 0
    for frame in video.video_frames(args.input):
        print(f"{current_frame}/{frames} | {info}")
        a = frame.to_ndarray()
        if args.encode:
            encoded = tile.encode_frame_simple(a)
            port.write(encoded)
            port.write(encoded)
        else:
            onebit = tile.to_bw(a, 128)
            # 30fps
            port.write(onebit)
            port.write(onebit)
            # port.write(b"\xaa" + 358 * b"\x00" + b"\xff")
        current_frame += 1
