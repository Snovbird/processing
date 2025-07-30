import os
import re

for content in os.listdir():
    if os.path.isdir(content) and content != ".git":
        try:
            # Count items in the directory
            item_count = len([item for item in os.listdir(content) if os.path.isfile(os.path.join(content, item))])
            
            # Check if folder name already has a count pattern (e.g., "folder (5)")
            count_pattern = r'\s*\(\d+\)$'
            match = re.search(count_pattern, content)
            
            if match:
                # Extract the current count from the folder name
                current_count_str = re.search(r'\((\d+)\)', content).group(1)
                current_count = int(current_count_str)
                
                # Only rename if the count has changed
                if current_count != item_count:
                    # Remove the old count pattern and add the new one
                    base_name = re.sub(count_pattern, '', content)
                    new_name = f"{base_name} ({item_count})"
                    try:
                        os.rename(content, new_name)
                        print(f"Updated '{content}' to '{new_name}' (count changed from {current_count} to {item_count})")
                    except OSError as e:
                        print(f"Error renaming '{content}': {e}")
                else:
                    print(f"Skipped '{content}' - count is already correct ({item_count})")
            else:
                # No count pattern exists, add one
                new_name = f"{content} ({item_count})"
                try:
                    os.rename(content, new_name)
                    print(f"Added count to '{content}' -> '{new_name}'")
                except OSError as e:
                    print(f"Error renaming '{content}': {e}")
                    
        except (OSError, PermissionError) as e:
            print(f"Error accessing directory '{content}': {e}")
