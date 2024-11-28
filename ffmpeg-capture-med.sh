ffmpeg -hide_banner \
  -f x11grab \
  -video_size 1320x1200 \
  -framerate 30 \
  -i :0.0+300,0 \
  -i palette.png \
  -filter_complex "[0:v]scale=40x36[v0];[v0][1:v]paletteuse[out]" \
  -map [out] -f image2pipe -pix_fmt gray8 -s 40x36 -r 30 -vcodec rawvideo - \
  | python ./scripts/gbstream.py -p /dev/ttyACM0 -e tile-index -s 40x36