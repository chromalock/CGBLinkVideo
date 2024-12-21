ffmpeg -hide_banner \
  -f x11grab \
  -video_size 1280x1152 \
  -framerate 8 \
  -i :0.0+300,0 \
  -i palette.png \
  -filter_complex "[0:v]scale=160x144[v0];[v0][1:v]paletteuse[out]" \
  -map [out] -f image2pipe -pix_fmt gray8 -s 160x144 -r 8 -vcodec rawvideo - \
  | python ./scripts/gbstream.py -p /dev/ttyACM0 -e tile-data --size 20x18 --fps 8