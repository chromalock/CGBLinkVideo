import serial
from py.util import chunks


def link_raw_stream(video, port):
    port = serial.Serial(port, baudrate=500000)
    if not port.is_open:
        port.open()

    count = 0

    frame_data = None
    with open(video, "rb") as vf:
        frame_data = vf.read()

    data_len = len(frame_data)
    frames_len = len(frame_data)/360

    print("Frames to send:", frames_len, "(", data_len, "bytes", ")")
    input()

    try:
        port.read()
        for bc in (chunks(frame_data, 360)):
            port.write(b"\x00")
            response = port.read()
            port.write(b"\x01")
            response = port.read()
            for b in bc:
                port.write(bytes([-b + 0xff]))
            count += 1
            print(count)

            port.write(b"\x30")
            port.read(1)

    finally:
        port.close()
