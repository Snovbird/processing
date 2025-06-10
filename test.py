import os
import subprocess
# directory_path = './dir/subdir/'

# # Extract the folder name
# folder_name = os.path.basename(os.path.dirname(directory_path))
# print(os.path.dirname(directory_path))
# print(folder_name)
# print(os.path.basename(directory_path))

# print(os.listdir(r'C:\Users\Labo Samaha\Desktop\.LabGym\z_misc_DONOTTOUCH\shortcuts'))

def clear_gpu_memory():
    try:
        # Reset GPU clocks temporarily to help clear memory
        subprocess.run(["nvidia-smi", "-lgc", "0,0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["nvidia-smi", "-rgc"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("GPU memory cleanup attempted")
        return True
    except Exception as e:
        print(f"GPU memory cleanup failed: {e}")
        return False
clear_gpu_memory()