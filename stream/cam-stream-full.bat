ffmpeg -hide_banner ^
  -f dshow ^
  -i video="OBS Virtual Camera" ^
  -pix_fmt yuv420p ^
  -video_size 160x144 ^
  -r 8 ^
  -framerate 8 ^
  -i "palette.png" ^
  -filter_complex "[0:v]scale=160x144[v0];[v0][1:v]paletteuse[out]" ^
  -map [out] -f image2pipe -pix_fmt gray8 -s 160x144 -r 8 -vcodec rawvideo - ^
  | python ./scripts/gbstream.py -p %1 -e tile-data -s 20x18 --fps 8