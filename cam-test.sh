ffmpeg -hide_banner \
  -f v4l2 \
  -video_size 160x144 \
  -framerate 30 \
  -input_format mjpeg \
  -i /dev/video0 \
  out.mkv