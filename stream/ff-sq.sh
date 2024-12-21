ffmpeg -hide_banner \
  -f x11grab \
  -video_size 1152x1152 \
  -framerate 30 \
  -i :0.0+300,0 \
  -i palette.png \
  -filter_complex "[0:v]scale=88x88[v0];[v0][1:v]paletteuse[out]" \
  -map [out] -f image2pipe -pix_fmt gray8 -s 88x88 -r 8 -vcodec rawvideo - \
  | python ./scripts/gbstream.py -p /dev/ttyACM0 -e tile-data --size 11x11 --fps 30