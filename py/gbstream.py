import serial
import os
import time

import encode.audio as audio
import encode.video as video
import encode.tile_encode as tile
import argparse


parser = argparse.ArgumentParser("gbstream.py")
parser.add_argument("-p", "--port", required=True)
parser.add_argument("-b", "--baud", default=921600)
parser.add_argument("-i", "--input", default="-")

args = parser.parse_args()


port = serial.Serial(args.port, baudrate=args.baud)

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
        onebit = tile.to_bw(a, 128)
        port.write(onebit[1:] + b"\x00")
        time.sleep(1.0/30.0)
        current_frame += 1
