ffmpeg -hide_banner ^
 -f dshow ^
 -i video="OBS Virtual Camera" ^
 -pix_fmt yuv420p ^
 -video_size 160x144 ^
 -r 8 ^
 -framerate 8 ^
 -i "palette.png" ^
 -filter_complex "[0:v]scale=160x144,eq=saturation=1.5,split[v0][v1];[v0]palettegen=max_colors=4:stats_mode=single:reserve_transparent=0[pal];[v1][pal]paletteuse=new=1[out]" ^
 -map [out] -f image2pipe -pix_fmt rgb24 -s 160x144 -r 8 -vcodec rawvideo - ^
 | python ./scripts/gbstream.py -p %1 -e tile-data -s 20x18 --fps 8 --color