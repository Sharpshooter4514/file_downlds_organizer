import os
import shutil

def organize_file(path):
    filename = os.path.basename(path)
    extension = filename.split('.')[-1].lower()
    folder_name = os.path.join(downloads_path, extension)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    destination_path = os.path.join(folder_name, filename)
    # Check if the file still exists before attempting to move
    if os.path.exists(path):
        shutil.move(path, destination_path)
        print(f"Moved: {filename} -> {destination_path}")
    else:
        print(f"File no longer exists: {filename}")

downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

# Iterate through everything in the directory more efficiently
with os.scandir(downloads_path) as entries:
    for entry in entries:
        if entry.is_file():
            # print(f"File: {entry.path}")
            organize_file(entry.path)
