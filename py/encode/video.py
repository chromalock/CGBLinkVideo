import av


def video_info(content):
    with av.open(content) as container:
        format = container.streams.video[0].format
        extra = dict()
        extra["frames"] = container.streams.video[0].frames
        extra['fps'] = 0
        return (format, extra)


def video_frames(content):
    with av.open(content) as container:
        stream = container.streams.video[0]
        stream.codec_context.skip_frame = "NONKEY"
        for video in container.decode(stream):
            yield video.to_rgb()
