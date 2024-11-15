def note_to_frequency(note):
    a = 440  # frequency of A (coomon value is 440Hz)
    return (a / 32) * (2 ** ((note - 9) / 12))


def frequency_to_period(freq):
    return round(-131072.0/freq + 2048)


def note_to_period(midi: int) -> int:
    return frequency_to_period(note_to_frequency(midi))


def period_bytes(midi: int) -> tuple[int, int]:
    p = note_to_period(midi)
    hi = (0b00000111_00000000 & p) >> 8
    lo = 0xFF & p
    return (hi, lo)


def period_to_frequency(period: int) -> float:
    return 131072.0/(2048 - (period))
