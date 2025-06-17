# import pyperclip

# pyperclip.copy('''ffmpeg -hwaccel cuda -hwaccel_output_format cuda -c:v h264_cuvid -i input.mp4 -vf "select='eq(t,30)+eq(t,60)+eq(t,90)+eq(t,120)+eq(t,150)',hwdownload,format=nv12" -vsync 0 -q:v 1 frame_%02d.png
# '''.split(' '))
