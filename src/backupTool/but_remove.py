from backupTool import jsonio
import os
from backupTool.but_file import is_dir
from backupTool.but_folder import remove_dir


def remove(config=None, files=None, alias=None, confirm=False):
    # get current files
    file_list = jsonio.read(files)
    if not file_list:
        exit()
    
    # check if alias exists, if it exists, remove
    if alias in file_list:
        del file_list[alias]
        jsonio.write(files, file_list) 
        print(f"removed {alias} from backup system")
        
    # todo check if backup folder exists and remove
    alias_root = os.path.join(config['backup_root'], alias)
    
    if is_dir(alias_root) and confirm:
        print(f"DELETE: {alias_root}")
        remove_dir(alias_root)
    
    elif is_dir(alias_root) and not confirm:
        print(f"There are still backups saved at: {alias_root}")
        
    elif not is_dir(alias_root) and confirm:
        # no data to delete, nothing to do, yet
        pass
    
    else:
        # noting to do, yet
        pass
    