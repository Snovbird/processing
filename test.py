import subprocess
result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE)
print(result.stdout.decode())
