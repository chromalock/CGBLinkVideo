from pySerialTransfer import pySerialTransfer as transfer
import time
import struct

from util import chunks


def encode_parameters(preserve_front: bool, buffer_size: int, buffer_type: int):
    if buffer_type not in range(0, 3):
        raise Exception(
            f"expected buffer_type to be 0, 1, or 2, got {buffer_type}")
    if buffer_size > 2**16 - 1:
        raise Exception(f"max buffer_size is 65335 bytes, got {buffer_size}")
    return struct.pack("BBBB", preserve_front, buffer_size & 0xff, (buffer_size >> 8) & 0xff, buffer_type)


class GBLink(object):
    def __init__(self, port, baud):
        self.link = transfer.SerialTransfer(port, baud)

    def open(self):
        self.link.open()

    def clear(self):
        self.link.send(0, 2)

    def set_parameters(self, preserve_front: bool, buffer_size: int, buffer_type: int):
        encoded = encode_parameters(preserve_front, buffer_size, buffer_type)
        to_send = self.link.tx_struct_obj(encoded)
        self.link.send(to_send, 0)

    def send_frame(self, buffer: bytearray | bytes):
        max_buffer = transfer.MAX_PACKET_SIZE - 2
        for chunk in chunks(buffer, max_buffer):
            to_send = self.link.tx_struct_obj(chunk)
            self.link.send(to_send, 1)

    def close(self):
        self.link.close()


if __name__ == "__main__":
    print('opening link')
    gblink = GBLink("/dev/ttyACM0", 921600)
    gblink.open()
    time.sleep(1)

    try:
        print('setting parameters')
        gblink.set_parameters(True, 360, 0)
        time.sleep(1)
        while True:
            gblink.send_frame(bytearray(360 * [0x00]))
            gblink.send_frame(bytearray(360 * [0xff]))
    finally:
        gblink.close()
