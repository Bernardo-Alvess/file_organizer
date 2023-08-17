import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PATH = 'C:/Users/berna/Downloads/'

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.is_directory:
            filepath = event.src_path
            extension = os.path.splitext(filepath)[1]
            print(extension)
            if extension != '.tmp':
                destination_folder = os.path.join(PATH, extension)  # Remove the leading dot from the extension
                print(destination_folder)
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)  # Create the directory if it doesn't exist
                try:
                    shutil.move(filepath, destination_folder)
                    print(f"Moved {filepath} to {destination_folder}")
                except Exception as e:
                    print(f"Error moving {filepath}: {e}, tried moving to {destination_folder}")

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, PATH, recursive=True)
    observer.start()

    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()