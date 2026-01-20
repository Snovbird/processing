import os
from common.common import select_folder, get_duration, list_files_ext, msgbox, avg

def main():
    # 1. Select directory
    folder_path = select_folder("Select folder to calculate average frame count")
    if not folder_path:
        return

    # 2. List all mp4 files
    mp4_files = list_files_ext(folder_path, ".mp4")
    if not mp4_files:
        msgbox("No MP4 files found in the selected folder.")
        return

    frame_counts = []
    
    print(f"Processing {len(mp4_files)} files in {folder_path}...")

    # 3. Iterate and get duration
    for filename in mp4_files:
        filepath = os.path.join(folder_path, filename)
        duration_info = get_duration(filepath) # Returns (frames, seconds, formatted_time)
        
        if duration_info:
            frames = duration_info[0]
            frame_counts.append(int(frames))
            print(f"{filename}: {int(frames)} frames")
        else:
            print(f"Could not read duration for {filename}")

    # 4. Calculate average and display
    if frame_counts:
        _, average = avg(frame_counts) # avg returns (Fraction, float)
        msg = f"Processed {len(frame_counts)} videos.\nTotal frames: {int(sum(frame_counts))}\nAverage frames: {average:.2f} or {round(average/15,3)}s\nmin frames: {min(frame_counts)} or {round(min(frame_counts)/15,3)}s\nmax frames: {max(frame_counts)} or {round(max(frame_counts)/15,3)}s"
        print("\n" + msg)
        msgbox(msg, "Average Frame Count")
    else:
        msgbox("No valid video durations could be read.")

if __name__ == "__main__":
    main()
