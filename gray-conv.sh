ffmpeg \
  -ss 0:00:00 \
  -i $1 -i palette.png \
  -filter_complex "[0:v]scale=40x36[v0];[v0][1:v]paletteuse[out]" \
  -map [out] $2