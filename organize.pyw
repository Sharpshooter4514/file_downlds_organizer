import os
import shutil

# Path to your downloads folder
downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

def organize_downloads():
    for item in os.listdir(downloads_path):
        item_path = os.path.join(downloads_path, item)
        if os.path.isfile(item_path):
            extension = item.split('.')[-1].lower()
            if not extension: continue  # Skip files without an extension
            folder_name = os.path.join(downloads_path, extension)
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            shutil.move(item_path, folder_name)

if __name__ == "__main__":
    while True:
        organize_downloads()
        print("Files organized. Waiting to check again...")
        time.sleep(600)  # Waits for 10 minutes before the next check
