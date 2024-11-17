import serial

import encode.video as video
import encode.tile_encode as tile
import argparse
import time

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

if args.input == "-":
    print('pipe input')
else:
    format, extra = video.video_info(args.input)
    width = format.width
    height = format.height
    frames = extra['frames']
    info = f"{args.input} {width}x{height}"

    current_frame = 0
    last_time = time.time()
    for frame in video.video_frames(args.input):
        frame_array = frame.to_ndarray()
        if encoding == "tile-data":
            print(len(list(tile.extract_tiles(frame_array))))
        elif encoding == "tile":
            encoded = tile.encode_frame_simple(frame_array)
            port.write(encoded)
            port.write(encoded)
            # port.write(b"\xaa" + 358 * b"\x00" + b"\xff")
        else:
            raise Exception("unknown encoding " + encoding)

        current_time = time.time()
        diff = current_time - last_time
        last_time = current_time
        print(f"{current_frame}/{frames} | {info} | {1/(diff + 0.00000000000001)}")

        current_frame += 1
