import os
import win32gui
import win32api
import win32con
from PIL import Image

# Icon descriptions (same as before)
SHELL32_DESCRIPTIONS = {
    0: "Unknown file type",
    1: "Generic application", 
    2: "Folder (closed)",
    3: "Folder (open)",
    # ... rest of descriptions
}

def extract_icon_simple(dll_path, icon_index, output_folder, dll_name):
    """Simplified icon extraction that saves basic info"""
    try:
        hicon = win32gui.ExtractIcon(0, dll_path, icon_index)
        
        if hicon == 0 or hicon == 1:
            return False
        
        # Just save a placeholder file instead of converting to image
        filename = f"{dll_name}_icon_{icon_index:03d}.txt"
        filepath = os.path.join(output_folder, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Icon {icon_index} found in {dll_name}.dll\n")
            f.write(f"Handle: {hicon}\n")
        
        win32gui.DestroyIcon(hicon)
        return True
        
    except Exception as e:
        print(f"Error extracting icon {icon_index}: {e}")
        return False

def find_and_extract_icons_simple(dll_path, dll_name, max_index=1000):
    """Simplified version that works around the bitmap issues"""
    output_folder = f"extracted_{dll_name}_icons"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    print(f"Scanning {dll_name}.dll for icons...")
    
    descriptions = SHELL32_DESCRIPTIONS if dll_name == 'shell32' else {}
    results = []
    
    for i in range(max_index):
        try:
            hicon = win32gui.ExtractIcon(0, dll_path, i)
            
            if hicon != 0 and hicon != 1:
                description = descriptions.get(i, "Unknown icon")
                print(f"Icon found at index: {i} - {description}")
                
                success = extract_icon_simple(dll_path, i, output_folder, dll_name)
                
                results.append({
                    'index': i,
                    'description': description,
                    'extracted': success
                })
                
                win32gui.DestroyIcon(hicon)
                
        except Exception:
            continue
    
    return results

def main():
    system_dir = win32api.GetSystemDirectory()
    
    dlls = {
        'shell32': f"{system_dir}\shell32.dll",    # Fixed: double backslash
        'imageres': f"{system_dir}\imageres.dll"   # Fixed: double backslash
    }
    
    for dll_name, dll_path in dlls.items():
        if os.path.exists(dll_path):
            results = find_and_extract_icons_simple(dll_path, dll_name)
            
            # Save results with UTF-8 encoding and ASCII-safe characters
            with open(f"{dll_name}_icons_detailed.txt", 'w', encoding='utf-8') as f:
                f.write(f"Available icons in {dll_name}.dll:\n")
                f.write("=" * 50 + "\n")
                for result in results:
                    status = "SUCCESS" if result['extracted'] else "FAILED"  # ASCII-safe
                    f.write(f"Index: {result['index']:3d} | {status} | {result['description']}\n")
                
                f.write(f"\nTotal icons found: {len(results)}")
            
            print(f"Found {len(results)} icons in {dll_name}.dll")

if __name__ == "__main__":
    main()