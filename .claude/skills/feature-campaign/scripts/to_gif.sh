#!/usr/bin/env bash
# to_gif.sh IN OUT [crop] [start] [duration]
#   IN: a .webm/.mp4 recording, or a frames dir (f0000.png ...) at 12 fps
#   crop: ffmpeg crop expr (w:h:x:y), e.g. 960:468:320:52 for a canvas region
# Output: 600 px wide GIF, palette per clip, under ~600 KB for email.
set -euo pipefail
in=$1; out=$2; crop=${3:-}; ss=${4:-0}; t=${5:-}
vf="fps=12,scale=600:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle"
[ -n "$crop" ] && vf="crop=$crop,$vf"
if [ -d "$in" ]; then
  ffmpeg -v error -y -framerate 12 -i "$in/f%04d.png" -vf "$vf" "$out"
else
  ffmpeg -v error -y -ss "$ss" ${t:+-t "$t"} -i "$in" -vf "$vf" "$out"
fi
ls -la "$out"
