def chunks(lst: list, n: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def permutations(color_depth: int, length: int):
    if length <= 0:
        return []
    elif length == 1:
        return [[x] for x in range(0, color_depth)]
    outputs = []
    for i in range(0, color_depth):
        for child_perm in permutations(color_depth, length - 1):
            outputs.append([i] + child_perm)

    return outputs


def square(start_x: int, start_y: int, width: int, height: int):
    for xi in range(0, width):
        for yi in range(0, height):
            yield (start_x + xi, start_y + yi)


def clamp(f: float, s: int) -> int:
    return round(f * s)


def rotate(l, n):
    return l[-n:] + l[:-n]
