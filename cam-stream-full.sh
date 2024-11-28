ffmpeg -hide_banner \
  -f v4l2 \
  -video_size 160x144 \
  -framerate 8 \
  -i $1 \
  -i palette.png \
  -filter_complex "[0:v]scale=160x144[v0];[v0][1:v]paletteuse[out]" \
  -map [out] -f image2pipe -pix_fmt gray8 -s 160x144 -r 8 -vcodec rawvideo - | python ./scripts/gbstream.py -p /dev/ttyACM0 -i - -e tile-data-full