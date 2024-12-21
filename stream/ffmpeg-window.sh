ffmpeg -hide_banner \
  -f x11grab \
  -video_size 1920x1200\
  -framerate 5 \
  -i :0.0+0,0 \
  -i palette.png \
  -filter_complex "[0:v]scale=1080x720[v0];[v0][1:v]paletteuse[out]" \
  -map [out] -f image2pipe -pix_fmt gray8 -s 1080x720 -r 5 -vcodec rawvideo - \
  | python ./scripts/gbwindow.py