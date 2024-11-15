from . import midi2period
import ctypes
import numpy as np

# https://stackoverflow.com/questions/142812/does-python-have-a-bitfield-type


class AudioStatus_bits(ctypes.LittleEndianStructure):
    _fields_ = [
        ('unused', ctypes.c_uint8, 4),
        ('ch4', ctypes.c_uint8, 1),
        ('ch3', ctypes.c_uint8, 1),
        ('ch2', ctypes.c_uint8, 1),
        ('ch1', ctypes.c_uint8, 1)
    ]


class AudioStatus(ctypes.Union):
    _fields = [("b", AudioStatus_bits), ('asbyte', ctypes.c_uint8)]


class Frame:
    def __init__(self, width=40, height=36, channels=3):
        self.channels = [None] * channels
        self.video = np.zeros((height, width))

    def set_channel(self, ch, midi):
        self.channels[ch] = midi2period.note_to_period(
            midi) if midi > 0 else (-1, -1)

    def set_video(self, data):
        self.video = data

    def __audio_bytes(self) -> bytes:
        status_bits = 0
        channel_bytes = bytearray()
        for (i, channel) in enumerate(self.channels):
            active = channel != None
            status_bits |= ((1 if active else 0) << i)
            channel_bytes += bytes([channel[0], channel[1]]
                                   ) if active else bytes([0, 0])

        return bytes([status_bits]) + channel_bytes

    def to_bytes(self, audio=True) -> bytearray:
        result = bytearray()
        for y in self.video:
            for x in y:
                result += bytes([x])
        if audio:
            result += self.__audio_bytes()
        return result
