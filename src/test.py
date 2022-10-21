#!/usr/bin/env python3

import os
import time
from datetime import datetime

def go_through(root, folders=None):
    folders = folders if folders else []
    
    for root, _, files in os.walk(root):
        folders.append(root)
        for file in files:
            folders.append(f"{root}/{file}")

    return folders
    
    
def backup2(folder, unique_name):
    import backupTool as but
    root = but.get_abspath(folder)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")    
    print(f"Backup for: {root} ({timestamp})")
    
    but.copy(root, f"tmp/{unique_name}_{timestamp}")  # copy dir
    but.make_dir(f"archive/{unique_name}")
    
    but.make_archive(f"tmp/{unique_name}_{timestamp}", f"archive/{unique_name}/{unique_name}_{timestamp}.zip") # zip    
    but.clean_up(f"archive/{unique_name}")   # clean up archive
    
    time.sleep(1) # maybe longer?
    but.remove_dir(f"tmp/{unique_name}_{timestamp}") # clean up tmp

if __name__ == "__main__":   
    backup2("test_data", "tstdata")
