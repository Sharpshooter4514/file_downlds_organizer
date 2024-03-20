import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

def is_file_stable(filepath, wait_time=2, check_interval=0.5):
    """Check if the file has stopped growing and exists, indicating download completion."""
    last_size = -1
    current_size = os.path.getsize(filepath)
    while current_size != last_size:
        time.sleep(check_interval)
        if not os.path.exists(filepath):
            return False
        last_size = current_size
        current_size = os.path.getsize(filepath)
    time.sleep(wait_time)  # Additional wait to ensure the file is not in a temporary state.
    return os.path.exists(filepath)

class DownloadFolderHandler(FileSystemEventHandler):
    def process(self, filepath):
        """Process the file if it's stable and not a temporary file."""
        filename = os.path.basename(filepath)
        # Skip temporary or incomplete files
        if filename.lower().endswith('.tmp') or filename.lower().startswith('crdownload') or filename.lower().endswith('crdownload'):
            print(f"Skipping temporary or incomplete file: {filename}")
            return
        while True:
            if not os.path.exists(filepath):
                print('File not available yet, waiting...')
                time.sleep(0.25)
                return True
            else:
                if is_file_stable(filepath):
                    self.organize_file(filepath)
                else:
                    print(f"File is not stable or was removed: {filename}")
                return False

    def on_created(self, event):
        if not event.is_directory:
            self.process(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self.process(event.dest_path)

    def organize_file(self, path):
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
