
from .jsonio import read
import os
import pathlib

def convert_bytes(size):
    """ Convert bytes to KB, or MB or GB"""
    if size:
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0        
        return size
    else:
        return '?'

def show(config, json_file=None, details=False, alias=None):
    if not json_file:
        exit()
        
    file_list = read(json_file)
    if not file_list:
        print("No Backups found")
        exit()
        
    if alias and alias in file_list:
        show_backups_for_alias(config, alias)
        
    else:
        if details:
            entry = f"alias: path (size) - last backup timestamp" 
        else:
            entry = f"alias: path"
        print(entry)
            
        for label, data in file_list.items():
            if details:
                entry = f"{label}: {data['path']} ({convert_bytes(data['last_backup_size'])}) - {data['last_backup']}" 
            else:
                entry = f"{label}: {data['path']}" 
            print(entry)
            

def get_list_of_files(path, filter='**/*.zip'):
    root = pathlib.Path(path)    
    
    # files = list(root.resolve().glob(filter)).sort(key=os.path.getctime)
    files = sorted(root.resolve().glob(filter), key=os.path.getmtime, reverse=True)
    return files

    #files.sort(key=os.path.getctime)
    
    
def show_backups_for_alias(config, alias):
    root = config['backup_root']
    path = os.path.join(root, alias)
    backups = get_list_of_files(path)
    alias_nr = 0
    
    for backup in backups:
        print(alias_nr, backup)
        alias_nr += 1    
    