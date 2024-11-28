ffmpeg \
  -ss 0:00:00 \
  -i videos/wifigb.mov -i palette.png \
  -filter_complex "[0:v]crop=128:128:360:0,scale=128x128[v0];[v0][1:v]paletteuse[out]" \
  -map [out] -f image2pipe -pix_fmt gray8 -s 128x128 -r 30 -vcodec rawvideo - \
  | python ./scripts/gbstream.py -p /dev/ttyACM0 -e tile-data