import cv2
import py.video.dither as gbd
import py.util as gbu
import numpy as np
import sys

input = sys.argv[1]
output = sys.argv[2]

fps = gbu.video_fps(input)
w, h = 144, 104
ow, oh = w*10, h*10

result = cv2.VideoWriter(
    f"{output}.avi", cv2.VideoWriter_fourcc(*'MJPG'), fps, (ow, oh))

for (i, f) in enumerate(gbu.video_frames(input)):
    print(i)
    # dithered = (np.round(f/255.0)*255).astype(np.uint8)
    dithered = gbd.cv2_floyd_steinberg(f, 4, True)
    w, h, *rest = np.shape(dithered)
    result.write(cv2.resize(dithered, (ow, oh),
                            interpolation=cv2.INTER_NEAREST_EXACT, fx=0, fy=0))

result.release()
print("done.")
