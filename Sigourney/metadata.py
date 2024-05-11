import os
import json
import sys

def sort_files(files):
    """
    Sort files based on numeric prefix in filename.
    """
    valid_files = [file for file in files if file.startswith(tuple(str(i) for i in range(10)))]

    return sorted(valid_files, key=lambda x: int(x.split('_')[0]))

def generate_metadata(directory):
    """
    Generate metadata.json based on files in the directory.
    """
    metadata = []
    
    files = os.listdir(directory)
    
    sorted_files = sort_files(files)
    
    for file in sorted_files:
        title_parts = file.split('_')[1:]
        part_with_extension = title_parts[-1]
        part_without_extension = part_with_extension.split('.')[0]
        title_parts = title_parts[:-1]
        title_parts.append(part_without_extension)
        title = " ".join(title_parts)
        src = file
        metadata.append({
            'title': title,
            'src': src
        })
    
    with open(os.path.join(directory, 'metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    generate_metadata(directory)
