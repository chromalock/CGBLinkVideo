from util import permutations


def mirror_x(w, h):
    pass


def mirror_y(w, h):
    pass


def mirrors_of(a, b, c, d):
    yield (a, b, c, d)
    yield (b, a, d, c)
    yield (c, d, a, b)
    yield (d, c, b, a)


def palettes_of(a, b, c, d, palette):
    return (palette[a], palette[b], palette[c], palette[d])


def apply_palettes(a, b, c, d, palettes):
    return (palettes_of(a, b, c, d, p) for p in palettes)


palettes = [
    (0, 1, 2, 3),
    (0, 3, 2, 1),
    (0, 2, 3, 1),
    (0, 3, 1, 2),
    (1, 2, 3, 0),
    (2, 3, 0, 1),
    (3, 0, 1, 2),
    (3, 2, 1, 0),
    (2, 1, 0, 3),
    (1, 0, 3, 2),
    (2, 3, 1, 0),
    (3, 1, 0, 2),
    (1, 0, 2, 3),
]

existing = set()

for bw_tile in permutations(3, 4):
    tup = tuple(bw_tile)
    rotations = set(mirrors_of(*tup))
    paletted = set(apply_palettes(*tup, palettes))
    if any([r in existing for r in rotations]):
        continue
    # elif any([r in existing for r in paletted]):
    #     continue
    else:
        existing.add(tup)

print(len(existing), "existing")
