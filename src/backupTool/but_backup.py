
import os
from backupTool import jsonio
from .but_folder import make_dir, copy
from .but_zip import make_archive
from .but_ownership import get_owner
from datetime import datetime
from backupTool.but_folder import clean_up, remove_dir
import time


def backup(config, files_table_path, archive_path, run, alias=None):
    if not alias:
        run_for_all = True
    else:
        run_for_all = False
        
    # ensure direcotry
    make_dir(archive_path)
    
    if run:    
        backup_run(config, files_table_path, archive_path, run_for_all, alias)
    else:
        backup_dry_run(files_table_path, run_for_all, alias)
    
    
def backup_dry_run(files_table_path, run_for_all=True, alias=None):
    print("dry run, no Backups will be created!")
    file_list = jsonio.read(files_table_path)
    if not file_list:
        exit()
    
    for label, data in file_list.items():
        if run_for_all or label==alias:
            print(f"Create Backup for {label}")
     

def backup_run(config, files_table_path, archive_path, run_for_all=True, alias=None):
    # get current files
    file_list = jsonio.read(files_table_path)
    if not file_list:
        exit()
        
    cfg = config
    
    for label, data in file_list.items():
        if run_for_all or label==alias:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            path = data["path"]
            uid, gid = get_owner(path, True)
            data["last_backup"] = timestamp
            data["uid"] = uid
            data["gid"] = gid 
                        
            print(f"Create Backup for {label} at {timestamp}")
            label_path = os.path.join(archive_path, label)        
            make_dir(label_path) # ensure direcotry
            
            tmp_copy = f"{label_path}/{label}_{timestamp}"
            copy(path, tmp_copy) # create temporary copy
            
            new_zip_path = os.path.join(label_path, f"{label}_{timestamp}.zip")
            make_archive(tmp_copy, new_zip_path) # zip    
            clean_up(label_path, max_files=int(cfg['number']))   # clean up archive
            
            time.sleep(1) # maybe longer?
            remove_dir(tmp_copy) # clean up tmp            
            
            file_size = os.path.getsize(new_zip_path)
            data["last_backup_size"] = file_size
            
            jsonio.write(files_table_path, file_list)
   