import py.video.dither as gbd
import py.util as gbu
import cv2
import sys

input = sys.argv[1]
output = sys.argv[2]

image = gbd.floyd_steinberg(gbu.cv2pil(
    cv2.imread(input)), 4)

image.save(f"{output}.png", "PNG")
