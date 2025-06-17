import pyperclip

# pyperclip.copy('''ffmpeg -hwaccel cuda -hwaccel_output_format cuda -c:v h264_cuvid -i input.mp4 -vf "select='eq(t,30)+eq(t,60)+eq(t,90)+eq(t,120)+eq(t,150)',hwdownload,format=nv12" -vsync 0 -q:v 1 frame_%02d.png
# '''.split(' '))

# a = 18
# d = [18]
# for i in range(6):
#     for b in [40,80,150]:
#         a += (b+40)
#         d.append(a)
# pyperclip.copy(".".join([f'{ a//60}{str(a % 60).zfill(2)}' for a in d]))