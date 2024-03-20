# pip install watchdog

import os
import time
import shutil

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Path to your downloads folder
downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

class DownloadFolderHandler(FileSystemEventHandler):
    def on_created(self, event):
        # This function is called when a file is created
        if not event.is_directory:
            organize_file(event.src_path)

def organize_file(path):
    filename = os.path.basename(path)
    extension = filename.split('.')[-1].lower()
    if not extension: return  # Skip files without an extension
    
    folder_name = os.path.join(downloads_path, extension)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    shutil.move(path, folder_name)
    print(f"Moved: {filename} -> {folder_name}/")

if __name__ == "__main__":
    event_handler = DownloadFolderHandler()
    observer = Observer()
    observer.schedule(event_handler, downloads_path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
