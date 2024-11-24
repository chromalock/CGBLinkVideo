import serial

import encode.video as video
import encode.tile_encode as tile
import argparse
import time
import sys

from gblink import GBLink
from util import chunks

parser = argparse.ArgumentParser("gbstream.py")
parser.add_argument("-p", "--port", required=True)
parser.add_argument("-b", "--baud", default=921600)
parser.add_argument("-i", "--input", default="-")
parser.add_argument("-e", "--encode",  default="tile",
                    choices=["tile", "tile-data", "tile-attr", "tile-data-full"])

args = parser.parse_args()

link = GBLink(args.port, args.baud)
link.open()
time.sleep(1)

encoding = args.encode

ZERO_BUFFER = b"\0"*360


parameters = {
    'tile': (False, 360, 2),
    'tile-attr': (False, 720, 2),
    'tile-data': (False, 4096, 2),
    'tile-data-full': (False, 5760, 2),
}[encoding]

print("setting parameters", parameters)
link.set_parameters(*parameters)
time.sleep(1)

if args.input == "-":
    print('pipe input')
    last_time = time.time()
    toskip = 0
    while True:
        current_time = time.time()
        diff = current_time - last_time

        if toskip > 1:
            toskip -= 1
            continue
        elif toskip == 1:
            last_time = time.time()
            toskip = 0
        elif time.time() - last_time > 1.0/30.0:
            toskip = int((time.time() - last_time)/(1.0/40.0))
            continue

        if encoding == "tile-data":
            data = sys.stdin.buffer.read(128*128)
            encoded = bytearray(
                list(tile.get_buffer_tile_data(data, 256, 16, 16)))
            link.send_frame(encoded)
        elif encoding == "tile-data-full":
            data = sys.stdin.buffer.read(160*144)
            encoded = bytearray(
                list(tile.get_buffer_tile_data(data, 360, 20, 18)))
            link.send_frame(encoded)
        elif encoding == "tile":
            data = sys.stdin.buffer.read(40*36)
            img = list(chunks([[px, px, px] for px in data], 40))
            encoded = tile.encode_frame_simple(img)
            link.send_frame(encoded)
            link.send_frame(encoded)

        last_time = current_time

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
            encoded = bytearray(list(tile.tile_data(frame_array, 256, 16, 16)))
            link.send_frame(encoded)
        elif encoding == "tile-data-full":
            encoded = bytearray(list(tile.tile_data(frame_array, 360, 20, 18)))
            link.send_frame(encoded)
        elif encoding == "tile":
            encoded = tile.encode_frame_simple(frame_array)
            link.send_frame(encoded)
            link.send_frame(encoded)
            # port.write(b"\xaa" + 358 * b"\x00" + b"\xff")
        elif encoding == "tile-attr":
            encoded = tile.encode_frame_simple(frame_array)
            link.send_frame(encoded)
            link.send_frame(ZERO_BUFFER)
            link.send_frame(encoded)
            link.send_frame(ZERO_BUFFER)
        else:
            raise Exception("unknown encoding " + encoding)

        last_time = current_time
        print(
            f"{current_frame}/{frames} | {info} | {round(1/(diff + 0.00000000000001), 2)}fps")

        current_frame += 1
