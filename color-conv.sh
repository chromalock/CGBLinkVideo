ffmpeg -hide_banner \
  -i $1 \
  -filter_complex '[0:v]scale=160x144,eq=saturation=1.0,split[v0][v1];color=black:16x128[c];[v1]palettegen=max_colors=4:stats_mode=single:reserve_transparent=false,split[pal][vpal];[vpal][c]vstack[palstack];[v0][pal]paletteuse=new=1[vout];[vout][palstack]hstack[out]' \
  -map "[out]" \
  $2