import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def load_config(p="config.txt"):
    config = {}
    if not os.path.exists(p):
        print("Config file not found exiting...")
        exit()
    
    with open(p, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = os.path.expanduser(value.strip())
    return config


class FileHandler(FileSystemEventHandler):
    def __init__(self, target_dir):
        super().__init__()
        self.target_directory = target_dir

    def on_created(self, event):
        if event.is_directory:
            return
        fpath = event.src_path
        fname = os.path.basename(fpath)

        if fname.startswith('.'):
            return

        print(f"New file detected {fname}")
        time.sleep(1)
        self.process_file(fpath, fname)

    def process_file(self, fpath, fname):
        try:
            _, ext = os.path.splitext(fname)
            ext = ext.lower()

            if ext in ['.py', '.js', '.html', '.css']:
                dest = os.path.join(self.target_directory, "Developer")
            elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp']:
                dest = os.path.join(self.target_directory, "Pictures_n_GIFS")
            elif ext in ['.pdf', '.doc', '.docx', '.pptx']:
                dest = os.path.join(self.target_directory, "Documents")
            elif ext in ['.mp4', '.avi']:
                dest = os.path.join(self.target_directory, "Video")
            else:
                dest = os.path.join(self.target_directory, "Other")
                
            os.makedirs(dest, exist_ok=True)
            shutil.move(fpath, os.path.join(dest, fname))
            print(f"Moved {fname} to folder {dest}")

        except Exception as e:
            print(f"Exception {e} occured, couldn't move file")
        
    def organize_existing(self, watch_dir):
        print("Organizing existing files...")
        for fname in os.listdir(watch_dir):
            fpath = os.path.join(watch_dir, fname)
            if os.path.isfile(fpath) and not fname.startswith('.'):
                self.process_file(fpath, fname)
        print("Done organizing existing files.")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.txt")
    
    CONFIG = load_config(config_path)
    WATCH_DIRECTORY = CONFIG.get("WATCH_DIRECTORY")
    TARGET_DIRECTORY = CONFIG.get("TARGET_DIRECTORY")

    if not WATCH_DIRECTORY or not TARGET_DIRECTORY:
        print("either no watch directoy or target directory, or both DNE")
        exit(1)
        
    os.makedirs(WATCH_DIRECTORY, exist_ok=True)
    os.makedirs(TARGET_DIRECTORY, exist_ok=True)

    event_handler = FileHandler(TARGET_DIRECTORY)
    event_handler.organize_existing(WATCH_DIRECTORY)
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIRECTORY, recursive=False)

    observer.start()
    print(f"Base Organizer Started!")
    print(f"Watching: {WATCH_DIRECTORY}")
    print(f"Routing to: {TARGET_DIRECTORY}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nKeyboard Interruption, stopping....")
        observer.stop()
    observer.join()