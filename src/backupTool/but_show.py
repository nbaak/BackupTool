
from .jsonio import read

def convert_bytes(size):
    """ Convert bytes to KB, or MB or GB"""
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0        
    return size

def show(json_file=None, details=False):
    if not json_file:
        exit()
    file_list = read(json_file)
    if not file_list:
        print("No Backups found")
        exit()
        
    for label, data in file_list.items():
        if details:
            entry = f"{label}: {data['path']} ({convert_bytes(data['last_backup_size'])}) - {data['last_backup']}" 
        else:
            entry = f"{label}: {data['path']}" 
        print(entry)