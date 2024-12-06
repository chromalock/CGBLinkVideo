
def getRGB24Pixel(img):
    pass


def convertToPalette(colors):
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
