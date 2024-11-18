from PIL import Image
import cv2


def cv2pil(cv):
    # Notice the COLOR_BGR2RGB which means that the color is
    # converted from BGR to RGB
    color_coverted = cv2.cvtColor(cv, cv2.COLOR_BGR2RGB)
    # Displaying the converted image
    pil_image = Image.fromarray(color_coverted)
    return pil_image


def video_frames(path):
    vidcap = cv2.VideoCapture(path)
    success, image = vidcap.read()
    while success:
        yield image
        success, image = vidcap.read()


def video_fps(path):
    vidcap = cv2.VideoCapture(path)
    return float(vidcap.get(cv2.CAP_PROP_FPS))


def dict_get(d, k):
    try:
        return d[k]
    except KeyError:
        return None
