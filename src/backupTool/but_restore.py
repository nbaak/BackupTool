
import os
from backupTool import jsonio
from backupTool.but_zip import unpack
from backupTool.but_folder import remove_dir, move
from backupTool.but_ownership import chown
from backupTool.but_file import is_dir, is_file


def restore(backup_archive_path, tmp_archive_path, file_table_path, alias):
    print("restoring", alias, '...')
    
    file_list = jsonio.read(file_table_path)
    if not file_list:
        exit()
    
    if alias in file_list:
        if date:=file_list[alias]['last_backup']:
            backup_path = file_list[alias]['path']
            backup_name = os.path.basename(backup_path)
            zip_path = os.path.join(backup_archive_path, alias, f"{alias}_{date}.zip")

            unzip_path = os.path.join(tmp_archive_path, alias)
            unpack(zip_path, unzip_path)            
            tmp_path = os.path.join(unzip_path, f"{alias}_{date}", backup_name)
            
            if is_dir(backup_path):
                restore_folder(tmp_path, backup_path)
            elif is_file(backup_path):
                restore_file(tmp_path, backup_path)
            else:
                print("ERROR")
                exit()
            
            print(f"restored: {alias}")    
            remove_dir(unzip_path)
            
            # ownership
            uid = file_list[alias]['uid']
            gid = file_list[alias]['gid']
            if uid != 0 and gid != 0:
                chown(backup_path, uid, gid)
            
        else:
            print("no backups so far")
            
def restore_file(src, dst):
    move(src, dst)

def restore_folder(src, dst):
    remove_dir(dst)
    move(os.path.join(src), dst)
    
    
    