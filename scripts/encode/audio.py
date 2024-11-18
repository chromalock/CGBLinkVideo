import av


def audio_frames(content):
    with av.open(content) as container:
        stream = container.streams.audio[0]
        stream.codec_context.skip_frame = "NONKEY"
        for audio in container.decode(stream):
            yield audio
