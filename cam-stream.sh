ffmpeg -hide_banner \
  -f v4l2 \
  -video_size 40x36 \
  -framerate 30 \
  -i $1 \
  -i palette.png \
  -filter_complex "[0:v]scale=40x36[v0];[v0][1:v]paletteuse[out]" \
  -map [out] -f image2pipe -pix_fmt gray8 -s 40x36 -r 30 -vcodec rawvideo - | python ./scripts/gbstream.py -p /dev/ttyACM0 -i - -e tile