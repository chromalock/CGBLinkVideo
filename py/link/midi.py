import time
import numpy
import mido
import py.video.midi2period as midi2period


def link_midi(midi, port):
    try:
        m = mido.MidiFile(midi)
        current = None
        port.write(bytes([0b00000000, 0, 0, 0, 0]))
        time.sleep(1)
        for msg in m.play():
            if msg.type == "note_off":
                continue
            hi, lo = midi2period.period_bytes(msg.note)
            hi2, lo2 = midi2period.period_bytes(msg.note - 7)
            port.write(
                bytes([0b00000000, hi | 0b10000000, lo, hi2 | 0b10000000, lo2]))
    finally:
        port.write(bytes([0b00000000, 0, 0, 0, 0]))
        port.close()
