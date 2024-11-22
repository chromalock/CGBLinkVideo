import argparse
import sys

from encode.tile_encode import encode_frame_simple, get_buffer_tile_data
from encode.video import video_frames
from encode import VideoInput
from util import chunks
import av
import cv2
import ffmpeg

parser = argparse.ArgumentParser("gbencode.py")
parser.add_argument("-i", "--input", default="-")
parser.add_argument("-e", "--encode",  default="tile",
                    choices=["tile", "tile-data", "tile-attr", "tile-data-full"])
parser.add_argument("-o", "--out", default="-")

args = parser.parse_args()
