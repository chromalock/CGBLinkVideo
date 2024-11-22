import serial

import encode.video as video
import encode.tile_encode as tile
import argparse
import time
import sys
import pyautogui

from util import chunks

parser = argparse.ArgumentParser("gbstream.py")
parser.add_argument("-p", "--port", required=True)
parser.add_argument("-b", "--baud", default=921600)
parser.add_argument("-i", "--input", default="-")
parser.add_argument("-e", "--encode",  default="tile",
                    choices=["tile", "tile-data", "tile-attr", "tile-data-full", "raw"])
parser.add_argument('-s', '--size')
parser.add_argument('-f', "--fps", default=30)

args = parser.parse_args()
