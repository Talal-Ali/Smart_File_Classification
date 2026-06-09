import time
import os
import shutil
import sqlite3 as sq
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

def get_types(f="datatypes.db"):
    if not os.path.exists(f):
        print("Error, datatypes file not found")
        exit()
    con = sq.connect(f)
    cursor = con.cursor()
    cursor.execute("""
        SELECT dt.Type, c.Category
        FROM DataTypes dt
        JOIN Categories c ON dt.Category_ID = c.Category_ID
    """)
    types_dict = {row[0]: row[1] for row in cursor}
    con.close()
    return types_dict

class FileHandler(FileSystemEventHandler):
    def __init__(self, target_dir, types_dict):
        super().__init__()
        self.target_directory = target_dir
        self.types_dict = types_dict

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
            category = self.types_dic.get(ext)
            if category is None:
                category = 'Other'
            dest = os.path.join(self.target_directory, category)
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
    TYPES_DICT = get_types()
    if not WATCH_DIRECTORY or not TARGET_DIRECTORY:
        print("either no watch directoy or target directory, or both DNE")
        exit(1)
        
    os.makedirs(WATCH_DIRECTORY, exist_ok=True)
    os.makedirs(TARGET_DIRECTORY, exist_ok=True)

    event_handler = FileHandler(TARGET_DIRECTORY,TYPES_DICT)
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