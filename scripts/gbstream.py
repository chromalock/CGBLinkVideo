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
parser.add_argument("-e", "--encode",  default="tile",
                    choices=["tile-index", "tile-data"])
parser.add_argument("-s", "--size")
parser.add_argument("-f", "--fps", type=float)

args = parser.parse_args()

link = GBLink(args.port, args.baud)
link.close()
time.sleep(2)
link.open()
time.sleep(1)

encoding = args.encode

size = None if args.size is None else tuple(
    [int(x) for x in args.size.split('x')])

width = size[0]
height = size[1]

target_fps = 30.0 if encoding == "tile-index" else 5
if args.fps:
    target_fps = args.fps

target_delta = 1.0/target_fps

buffer_size = 360 if encoding == "tile-index" else width*height*16

parameters = (True, buffer_size, 2)

print(f"{width = }, {height =}, {encoding =}, {target_fps =}")

print("setting parameters", parameters)
link.set_parameters(*parameters)
time.sleep(1)

last_time = time.time()
toskip = 0
while True:
    current_time = time.time()
    diff = current_time - last_time

    # skip any frames that have been missed since the last
    if toskip > 1:
        toskip -= 1
        continue
    elif toskip == 1:
        last_time = time.time()
        toskip = 0
    elif time.time() - last_time > target_delta:
        toskip = int((time.time() - last_time)/target_delta)
        continue

    if encoding == "tile-data":
        data = sys.stdin.buffer.read(width*height*8*8)
        encoded = bytearray(
            list(tile.get_buffer_tile_data(data, width*height, width, height)))
        link.send_frame(encoded)
    elif encoding == "tile-index":
        data = sys.stdin.buffer.read(40*36)
        img = list(chunks([[px, px, px] for px in data], 40))
        encoded = tile.encode_frame_simple(img)
        link.send_frame(encoded)

    last_time = current_time
