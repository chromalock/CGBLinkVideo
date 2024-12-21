ffmpeg -hide_banner \
  -i $1 \
  -framerate 30 \
  -i palette.png \
  -filter_complex "[0:v]scale=160x144[v0];[v0][1:v]paletteuse[out]" \
  -map [out] -f image2pipe -r 30 -pix_fmt gray8 -s 40x36 -vcodec rawvideo - \
  | python ./scripts/gbstream.py -p $2 -e tile-index -s 40x36 --fps 30