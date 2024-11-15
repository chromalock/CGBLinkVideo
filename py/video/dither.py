import cv2
from .util import cv2pil
import numpy as np
from PIL import Image


def get_new_val(old_val, nc):
    """
       Get the "closest" colour to old_val in the range [0,1] per channel divided
       into nc values.

       """

    return np.round(old_val * (nc - 1)) / (nc - 1)


def fs_dither(img, nc, w, h):
    """
    Floyd-Steinberg dither the image img into a palette with nc colours per
    channel.

    """

    arr = np.array(img, dtype=float) / 255

    for ir in range(h):
        for ic in range(w):
            # NB need to copy here for RGB arrays otherwise err will be (0,0,0)!
            old_val = arr[ir, ic].copy()
            new_val = get_new_val(old_val, nc)
            arr[ir, ic] = new_val
            err = old_val - new_val
            # In this simple example, we will just ignore the border pixels.
            if ic < w - 1:
                arr[ir, ic+1] += err * 3/16
            if ir < h - 1:
                if ic > 0:
                    arr[ir+1, ic-1] += err * 5/16
                arr[ir+1, ic] += err * 7/16
                if ic < w - 1:
                    arr[ir+1, ic+1] += err / 16

    carr = np.array(arr/np.max(arr, axis=(0, 1)) * 255, dtype=np.uint8)
    return Image.fromarray(carr)


def palette_reduce(img, nc):
    """Simple palette reduction without dithering."""
    arr = np.array(img, dtype=float) / 255
    arr = get_new_val(arr, nc)

    mags = np.max(arr)

    carr = np.array(arr/np.max(arr) * 255 if mags > 0 else arr, dtype=np.uint8)
    return Image.fromarray(carr)


def floyd_steinberg(pil_img, nc, just_palette=False):
    GREYSCALE = True
    # Read in the image, convert to greyscale.
    if GREYSCALE:
        pil_img = pil_img.convert('L')
    w, h = pil_img.size
    if just_palette:
        return palette_reduce(pil_img, nc)
    else:
        return palette_reduce(fs_dither(pil_img, nc, w, h), nc)


def cv2_floyd_steinberg(cvimg, nc, p=False):
    pil_image = cv2pil(cvimg)
    dithered = floyd_steinberg(pil_image, nc, p)
    return cv2.cvtColor(np.array(dithered), cv2.COLOR_RGB2BGR)
