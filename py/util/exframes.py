# Extracts frames from a video and writes them into a folder as png files

import cv2
import sys
import os

video = sys.argv[1]
frames = sys.argv[2]

if video is None:
    print("error: no video provided")
    exit(1)

if frames is None:
    print("error: no output supplied")
    exit(1)

os.makedirs(frames, exist_ok=True)

vidcap = cv2.VideoCapture(video)

success, image = vidcap.read()
count = 0

while success:
    cv2.imwrite(frames + "/%d.png" % count, image)

    if count % 100 == 0:
        print(count, "/", int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)))

    success, image = vidcap.read()
    count += 1

print(count, "/", int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)))

print("extracted", count, "frames")
