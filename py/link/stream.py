import time
import cv2
import os
import numpy as np
import serial


def link_stream(video, port):
    vidcap = cv2.VideoCapture(video)

    print("fps:", vidcap.get(cv2.CAP_PROP_FPS))

    frames = "frames"
    os.makedirs(frames, exist_ok=True)

    limit = None

    port = serial.Serial(port, baudrate=250000)
    if not port.is_open:
        port.open()

    success, image = vidcap.read()
    count = 0
    print("Y=", len(image))
    print("X=", len(image[0]))
    try:
        while success:
            if limit and count > limit:
                break

            image = np.around(image/255)

            cv2.imwrite("frames/%d.png" % count, image*255)
            port.write(b"\x03")
            for y in range(0, len(image)):
                for x in range(0, len(image[0])):
                    if image[y][x][0] >= 0.5:
                        port.write(b"\x01")
                    else:
                        port.write(b"\x00")

            time.sleep(0.016 * 2)

            if count % 100 == 0:
                print(count, "/", limit or int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)))

            success, image = vidcap.read()
            count += 1

            print(count)
    finally:
        port.close()
