# ffmpeg -i input.mp4 -vf "fps=16,scale=160:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=32:reserve_transparent=0[p];[s1][p]paletteuse" -loop 0 output.gif

ffmpeg -hide_banner \
  -i $1 \
  -filter_complex '[0:v]crop=ih/144*160:ih,scale=160x144,eq=saturation=1.4,split[v0][v1];[v0]palettegen=max_colors=4:stats_mode=single:reserve_transparent=0[p];[v1][p]paletteuse' \
  $2