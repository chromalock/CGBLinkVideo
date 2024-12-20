import serial

import encode.video as video
import encode.tile_encode as tile
import argparse
import time
import sys
import os

from gblink import GBLink
from util import chunks
from color import extract_colors, generatePaletteBytes, defaultPaletteBytes

parser = argparse.ArgumentParser("gbstream.py")
parser.add_argument("-p", "--port", required=True)
parser.add_argument("-b", "--baud", default=921600)
parser.add_argument("-e", "--encode",  default="tile",
                    choices=["tile-index", "tile-data"])
parser.add_argument("-s", "--size")
parser.add_argument("-f", "--fps", type=float)
parser.add_argument("-c", "--color", action="store_true")

args = parser.parse_args()

encoding = args.encode

use_color = args.color

target_fps = 30.0 if encoding == "tile-index" else 5
if args.fps:
    target_fps = args.fps

target_delta = 1.0/target_fps


link = GBLink(args.port, args.baud)
link.close()
time.sleep(1)
link.open()
time.sleep(1)


size = None if args.size is None else tuple(
    [int(x) for x in args.size.split('x')])

width = size[0]
height = size[1]


buffer_size = 360 if encoding == "tile-index" else width*height*16

buffer_size = buffer_size + (8 if use_color else 0)

parameters = (True, buffer_size, 2)

print(f"{width = }, {height =}, {encoding =}, {target_fps =}")

print("setting parameters", parameters)
link.set_parameters(*parameters)
time.sleep(1)

print('set parameters')

try:
    last_time = time.time()
    toskip = 0
    while True:
        if sys.stdin.closed:
            link.close()
            sys.exit(0)
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
            read_size = width*height*8*8*(3 if use_color else 1)
            data = sys.stdin.buffer.read(read_size)
            if use_color:
                # rgb -> color_idx
                extractedPalette = extract_colors(data, read_size)
                # color_idx -> rgb
                palette = {v: k for k, v in extractedPalette.items()}
                for i in range(4):
                    if i not in palette:
                        palette[i] = (0, 0, 0)
                framePalette = [palette[0], palette[1],
                                palette[2], palette[3]]
                rgbw = [(0xff, 0x00, 0x00), (0x00, 0xff, 0x00),
                        (0x00, 0x00, 0xff), (0xff, 0xff, 0x00)]

                paletteBytes = generatePaletteBytes(framePalette)
                encoded = bytearray(
                    list(tile.get_color_buffer_tile_data(data, width*height, width, height, extractedPalette)))
                encoded = paletteBytes + encoded
            else:
                encoded = bytearray(
                    list(tile.get_buffer_tile_data(data, width*height, width, height)))

            link.send_frame(encoded)
        elif encoding == "tile-index":
            data = sys.stdin.buffer.read(width*height)
            img = list(chunks([[px, px, px] for px in data], 40))
            encoded = tile.encode_frame_simple(img)
            link.send_frame(encoded)

        last_time = current_time
except Exception as e:
    print('exiting')
    print(e)
    link.close()
    time.sleep(1)
    sys.exit(0)
