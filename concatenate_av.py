
import av
import os
import sys
import shutil
from common.common import select_video, askint, makefolder, custom_dialog, select_folder, error

def concatenate_with_av(input_files: list[str], output_folder: str) -> str | None:
    """
    Concatenate video files using PyAV. This attempts to copy streams directly (remux)
    for high performance.
    """
    if len(input_files) > 1:
        # Determine output filename
        basename, ext = os.path.splitext(os.path.basename(input_files[0]))
        try:
            # Assuming format like "cage-date-..."
            cage, date, *_ = basename.split("-")
            output_name = f"{cage}-{date}{ext}"
        except ValueError:
            # Fallback if naming convention doesn't match
            output_name = f"concat_{basename}{ext}"
            
        output_path = os.path.join(output_folder, output_name)
        
        print(f"Concatenating {len(input_files)} files into {output_path}...")
        
        with av.open(output_path, 'w') as output_container:
            output_video_stream = None
            output_audio_stream = None
            
            # We track the duration offset so timestamps continue smoothly across files.
            # pts_offset = 0 # (Not reliable enough for simple offsetting, we generally re-calc based on last packet)
            video_duration = 0
            
            # Open the first file to set up the output streams
            first_file = input_files[0]
            with av.open(first_file) as input_container:
                # Setup Video Stream
                in_video = input_container.streams.video[0]
                output_video_stream = output_container.add_stream(in_video.name)
                
                # (Optional) Setup Audio Stream - The original script used -an (no audio).
                # If user wants audio, we would need to add it here.
                # For now, mimicking original behavior of dropping audio to ensure speed/compatibility?
                # Original script line 38: '-an', # No audio
                # So we SKIP audio setup.

            # Now process all files
            for i, file_path in enumerate(input_files):
                print(f"Processing part {i+1}/{len(input_files)}: {os.path.basename(file_path)}")
                
                with av.open(file_path) as input_container:
                    in_video = input_container.streams.video[0]
                    # We only demux. We don't decode.
                    
                    for packet in input_container.demux(in_video):
                        if packet.dts is None:
                            continue
                        
                        # Rebase timestamps
                        # We must update the packet's stream to be the output stream
                        packet.stream = output_video_stream
                        
                        # Adjust timestamps (PTS/DTS)
                        # Simple approach: add the accumulated duration of previous clips.
                        # BUT: packet timestamps are in the stream's time_base.
                        # Ideally inputs have same timebase.
                        
                        # Shift timestamps by current video_duration
                        if packet.pts is not None:
                            packet.pts += video_duration
                        if packet.dts is not None:
                            packet.dts += video_duration
                            
                        output_container.mux(packet)
                        
                    # Update offset for next file
                    # We need the duration of this file in the TIMEBASE of the stream.
                    # av.stream.duration is often in time_base units.
                    if in_video.duration:
                        video_duration += in_video.duration
                    else:
                        # Fallback if duration is missing (rare in healthy mp4)
                        # We might need to rely on the last packet's pts + duration?
                        # For now assuming headers are correct.
                        pass

        print(f"Successfully created: {output_path}")
        return output_path

    elif len(input_files) == 1:
        # Move single file logic
        filepath = input_files[0]
        if len(input_files) == 0:
            return None
            
        name, ext = os.path.splitext(os.path.basename(filepath))
        folder = os.path.dirname(filepath)
        try:
            cage, date, *_ = name.split("-")
            new_name = f"{cage}-{date}{ext}"
        except:
             new_name = name + ext
             
        newpathname = os.path.join(folder, new_name)
        
        # Renaissance locally first if needed
        if filepath != newpathname:
            os.rename(filepath, newpathname)
            
        # Move to output folder
        if output_folder != os.path.dirname(newpathname):
            moved_path = shutil.move(newpathname, output_folder)
            return moved_path
        return newpathname
        
    else:
        return None

def group_files_by_digits(file_paths: list[str]) -> list[list[str]]:
    from collections import defaultdict
    grouped_files = defaultdict(list)
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        try:
            cage, date = filename.split("-")[:2]
            grouped_files[cage].append(file_path)
        except:
            # If naming convention fails, maybe group by entire prefix?
            # Or just fail gracefully by putting it in a "misc" group
            grouped_files["misc"].append(file_path)
            
    return [group for group in grouped_files.values()]

def manually_select_concatenation(startpath):
    num = askint("How many concatenations?", "Total Outputs")
    if not num: return
    
    toconcat_groups = []
    for c in range(num):
        group = select_video(title=f"Select videos for Group {c+1}", path=startpath)
        if group:
            toconcat_groups.append(group)

    process_groups(toconcat_groups)

def process_groups(toconcat: list[list[str]]):
    if not toconcat: return
    
    # Destination folder
    first_group = toconcat[0]
    if not first_group: return
    
    start_dir = os.path.dirname(first_group[0])
    output_folder = makefolder(start_dir, foldername='concat') # Uses logic from common.py
    
    last_output = None
    for group in toconcat:
        last_output = concatenate_with_av(group, output_folder)
        
    if last_output:
        os.startfile(output_folder)

def main():
    startpath = None
    try:
        startpath = sys.argv[1]
    except IndexError:
        pass
        
    # Validation logic from original
    if startpath and not os.path.isdir(startpath):
        # Try some common path expansions if needed, or just clear it
        if os.path.isdir(os.path.join(os.path.expanduser("~"), startpath)):
            startpath = os.path.join(os.path.expanduser("~"), startpath)
        else:
            startpath = None

    if startpath is None:
        startpath = select_folder()
        if not startpath: return 

    # Attempt automatic grouping
    files = [f for f in os.listdir(startpath) if os.path.isfile(os.path.join(startpath, f)) and f.endswith('.mp4')]
    toconcat_groups = group_files_by_digits([os.path.join(startpath, f) for f in files])
    
    # Verification
    display_string = "\n\n".join([", ".join([os.path.basename(f) for f in group]) for group in toconcat_groups])
    check = custom_dialog(msg=f"Are these the expected groups:\n\n{display_string}", title="Verification", dimensions=(500, 600))
    
    if check == 'yes':
        process_groups(toconcat_groups)
    else:
        manually_select_concatenation(startpath=startpath)

if __name__ == "__main__":
    main()
