import mido


def get_track_tempo(track):
    tempo = None
    for evt in track:
        if evt.type == "set_tempo":
            tempo = evt.tempo
    return tempo


def monofy(midi: mido.MidiFile) -> mido.MidiFile:
    """
      Takes each track in a midi file and converts each track into
      one thats more friendly for systems that can only play one
      note at once (always prioritizes most recent note)
    """
    result = mido.MidiFile()
    result.ticks_per_beat = midi.ticks_per_beat

    for track in midi.tracks:
        result_track: mido.MidiTrack = track.copy()
        result_track.clear()
        current_ticks = 0

        result.tracks.append(result_track)

        currently_playing = None

        for evt in track:
            e: mido.Message = evt.copy()
            print(e)
            current_ticks += e.time
            last_time = 0
            if e.type == "note_on":
                if currently_playing != None:
                    result_track.append(mido.Message(
                        "note_off", velocity=127, note=currently_playing, time=current_ticks - last_time))
                    last_time = current_ticks
                currently_playing = e.note
                e.time = current_ticks - last_time
                result_track.append(e)
                last_time = current_ticks
            elif e.type == "note_off":
                if e.note == currently_playing:
                    currently_playing = None
                    e.time = current_ticks - last_time
                    result_track.append(e)
                    last_time = current_ticks
            else:
                # this could cause issues but whatever
                result_track.append(e)

    return result
