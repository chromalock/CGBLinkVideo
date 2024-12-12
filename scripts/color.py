

defaultPalette = [
    (0x00, 0x00),               # black
    (0b11001110, 0b00111001),   # lighter black
    (0b11010110, 0b01011010),   # lighter-lighter black
    (0xff, 0xff)                # white
]

defaultPaletteBytes = b"".join([bytearray([a, b]) for a, b in defaultPalette])


def extract_colors(data, read_size):
    palette = {}
    cur_color = 0
    for i in range(0, read_size, 3):
        pixel = (data[i], data[i+1], data[i+2])
        if pixel not in palette:
            palette[pixel] = cur_color
            cur_color = cur_color + 1
        if cur_color == 4:
            break
    return palette


def reversebinary(n):
    return int('{:08b}'.format(n)[::-1], 2)


def generatePaletteBytes(colors):
    return b"".join([bytearray(toGBCColor(*color)) for color in colors])


def toGBCColor5(r, g, b):
    b_lo = 0xff & (r | g >> 5)
    b_hi = 0xff & (g << 3 | b >> 2)
    return (reversebinary(b_lo), reversebinary(b_hi))


def toGBCColor(r, g, b):
    r = int(r / 255.0 * 0b11111) & 0b11111
    g = int(g / 255.0 * 0b11111) & 0b11111
    b = int(b / 255.0 * 0b11111) & 0b11111
    return toGBCColor5(r, g, b)


def getRGB24Pixel(img):
    pass


def convertToPaletteByte(colors):
    pass


def getPalette(img):
    color0 = getRGB24Pixel(img, 160)
    color1 = getRGB24Pixel(img, 161)
    color2 = getRGB24Pixel(img, 162)
    color3 = getRGB24Pixel(img, 163)
    resultDict = dict()

    resultDict[color0] = 0b00
    resultDict[color1] = 0b01
    resultDict[color2] = 0b10
    resultDict[color3] = 0b11

    return resultDict
