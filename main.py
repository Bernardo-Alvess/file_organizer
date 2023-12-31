import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def get_download_path():
    ##Returns the default downloads path for linux or windows
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')
    
PATH = "C:/Users/berna/Documents/teste script/"

def checkFile(file, path):
    count = 0
    while os.path.exists(os.path.join(path, file)):
        count += 1
        file_name, file_extension = os.path.splitext(file)
        file = f"{file_name}_{count}{file_extension}"
    return file

def moveFiles():
    no_folder_extensions = ['.tmp', '.crdownload', '.opdownload', '.ini']
    for file in os.listdir(PATH):
        file_path = f'{PATH}{file}'
        if os.path.isfile(file_path):
            extension = os.path.splitext(file)[1]
            folder_path = os.path.join(PATH, extension)
            if extension not in no_folder_extensions:
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    print(f'Created folder {folder_path}')
                try:
                    new_file_name = checkFile(file, folder_path)
                    new_file_path = os.path.join(folder_path, new_file_name)
                    shutil.move(file_path, new_file_path)
                except Exception as e:
                    print(e)
                

moveFiles()

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.is_directory:
            moveFiles()
while True:
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
    time.sleep(300)
