# converts a video + midi file to a format later used by

import argparse
import py.util as util
import py.video.Frame as gbf
import json


def get_color_index(rgb, ncolors):
    return int(round((sum(rgb)/3.0)/255 * (ncolors - 1)))


def get_tile_indexes(frame):
    # tile_index = bottom_right + bottom_left*4 + top_right*16 + top_left*64
    indexes = [[0 for _ in range(20)] for _ in range(18)]
    for y in range(len(frame)//2):
        for x in range(len(frame[0])//2):
            tl = get_color_index(frame[y*2][x*2], 4)
            tr = get_color_index(frame[y*2][x*2+1], 4)
            bl = get_color_index(frame[y*2+1][x*2], 4)
            br = get_color_index(frame[y*2+1][x*2+1], 4)
            tile_index = br + bl * 4 + tr * 16 + tl * 64
            indexes[y][x] = tile_index
    return indexes


def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("midiframes")
    parser.add_argument("out")

    args = parser.parse_args()

    v = args.video
    m = args.midiframes
    o = args.out

    midi_frames = None
    with open(m, "r") as midi_file:
        midi_frames = json.load(midi_file)

    with open(o, "wb") as out_file:
        for (frame_no, frame) in enumerate(util.video_frames(v)):
            frame_data = gbf.Frame(channels=0)
            # midi_data = util.dict_get(midi_frames['events'], str(frame_no))
            # # todo need to check if id has changed to handle same channel being retriggered
            # if midi_data != None:
            #     if midi_data == "off":
            #         frame_data.set_channel(0, -1)
            #     else:
            #         frame_data.set_channel(0, midi_data["midi"])
            # video data
            tiles = get_tile_indexes(frame)
            frame_data.set_video(tiles)
            bs = frame_data.to_bytes(audio=False)
            out_file.write(bs)
            print(frame_no, len(bs))


if __name__ == "__main__":
    __main__()
