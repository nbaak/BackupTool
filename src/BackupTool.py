#!/usr/bin/env python3

import argparse
import pathlib
import os
import config
import jsonio
import backupTool as but
from datetime import datetime 
import time

THIS_PATH = pathlib.Path(__file__).parent.resolve()
CFG_FILE = os.path.join(THIS_PATH, "config.ini")
CFG_SECTION = "backuptool"
FILE_TABLE = os.path.join(THIS_PATH, "files.json")
BACKUP_ARCHIVE = os.path.join(THIS_PATH, "archive")

config.create(CFG_FILE, CFG_SECTION, {'backup_root': f"{THIS_PATH}/archive", 'number': 5}) # initial
config_data = config.read(CFG_FILE, CFG_SECTION)

def is_dir(path) -> bool:
    return os.path.isdir(path)
    
def is_file(path) -> bool:
    return os.path.isfile(path)

def convert_bytes(size):
    """ Convert bytes to KB, or MB or GB"""
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0        
    return size

import random
import string

def get_random_string(length):
    # https://pynative.com/python-generate-random-string/
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    #print("Random string of length", length, "is:", result_str)
    return result_str

def find_in_dict(dictionary, search_key, seach_value) -> str:
    for label,data in dictionary.items():
        for key, value in data.items():
            if key==search_key and value==seach_value:
                return label
    
    return None # found nothing

def show_tool(details=False):
    file_list = jsonio.read(FILE_TABLE)
    if not file_list:
        print("No Backups found")
        exit()
        
    for label, data in file_list.items():
        if details:
            entry = f"{label}: {data['path']} ({convert_bytes(data['last_backup_size'])}) - {data['last_backup']}" 
        else:
            entry = f"{label}: {data['path']}" 
        print(entry)
    
def add_tool(target, alias=None):
    # get current files
    file_list = jsonio.read(FILE_TABLE)
    if not file_list:
        file_list = {}
    
    path = pathlib.Path(target).resolve()
    if not (is_dir(path) or is_file(path)): 
        print("ERROR: '{target}' is no valid path")
        exit()
        
    # check if path is already in backup system
    if label:=find_in_dict(file_list, "path", str(path)):
        print(f"{path} is already in the backup sytem as {label}")
        exit()
    
    if not alias:
        # create alias
        alias = get_random_string(5)
        while alias in file_list:
            alias = get_random_string(5)        
    
    if not alias in file_list:
        file_list[alias] = {"path": str(path), "last_backup": None, "last_backup_size": None}
        jsonio.write(FILE_TABLE, file_list)       
        print(f"added {path} to the backup system as {alias}")
    
def remove_tool(alias):
    # get current files
    file_list = jsonio.read(FILE_TABLE)
    if not file_list:
        exit()
    
    # check if alias exists, if it exists, remove
    if alias in file_list:
        del file_list[alias]
        jsonio.write(FILE_TABLE, file_list) 
        print(f"removed {alias} from backup") 

def backup_tool(run, alias=None):
    if not alias:
        run_for_all = True
    else:
        run_for_all = False
        
    # ensure direcotry
    but.make_dir(BACKUP_ARCHIVE)
    
    if not run:
        backup_dry_run(run_for_all, alias)
    
    if run:    
        backup_run(run_for_all, alias)
    
def backup_dry_run(run_for_all=True, alias=None):
    print("dry run, no Backups will be created!")
    file_list = jsonio.read(FILE_TABLE)
    if not file_list:
        exit()
    
    for label, data in file_list.items():
        if run_for_all or label==alias:
            print(f"Create Backup for {label}")
     
def backup_run(run_for_all=True, alias=None):
    # get current files
    file_list = jsonio.read(FILE_TABLE)
    if not file_list:
        exit()
        
    cfg = config.read(CFG_FILE, CFG_SECTION)
    
    for label, data in file_list.items():
        if run_for_all or label==alias:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            path = data["path"]
            data["last_backup"] = timestamp
            
            print(f"Create Backup for {label} at {timestamp}")
            label_path = os.path.join(BACKUP_ARCHIVE, label)        
            but.make_dir(label_path) # ensure direcotry
            
            tmp_copy = f"{label_path}/{label}_{timestamp}"
            but.copy(path, tmp_copy) # create temporary copy
            
            new_zip_path = os.path.join(label_path, f"{label}_{timestamp}.zip")
            but.make_archive(tmp_copy, new_zip_path) # zip    
            but.clean_up(label_path, max_files=int(cfg['number']))   # clean up archive
            
            time.sleep(1) # maybe longer?
            but.remove_dir(tmp_copy) # clean up tmp            
            
            file_size = os.path.getsize(new_zip_path)
            data["last_backup_size"] = file_size
            
            jsonio.write(FILE_TABLE, file_list)
           
def restore_tool(alias):
    print("RESTORE", alias)

def config_update(key, value):
    if key == "backup_root":
        path = pathlib.Path(value).resolve()
        
        if not is_dir(path):
            print(f"ERROR: '{path}' is not valid")
            exit()
        else:
            value = path

    if key and value:
        data = {str(key): str(value)}
        config.update(CFG_FILE, CFG_SECTION, data)
   
def config_show():
    data = config.read(CFG_FILE, CFG_SECTION)
    print(f"[{CFG_SECTION}]")
    for k,v in data.items():
        print(f"{k}: {v}")
            
def config_reset():
    data = {
            "backup_root": f"{THIS_PATH}/archive",
            "number": 5
           }           
    config.update(CFG_FILE, CFG_SECTION, data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='BackupTool', description='Backup Tool')
    subparsers = parser.add_subparsers(dest="subparser")

    parser_show = subparsers.add_parser("show", help="Show Files/Folders in Backup", description="Show Files/Folders in Backup")
    parser_show.add_argument('-a', '--all', action=argparse.BooleanOptionalAction, help='also show size and datae of last backup file')


    parser_add = subparsers.add_parser("add", help="Add a Files/Folders to the Backup System")
    parser_add.add_argument('path', metavar='path', type=str, help="Path to File/Folder")
    parser_add.add_argument('-a', '--alias', default=None, help='Alias for the Backup System')


    parser_remove = subparsers.add_parser("remove", help="Remove a File/Folder from the Backup System")
    parser_remove.add_argument('alias', metavar='alias', type=str, help="Alias for Path/Folder")


    parser_backup = subparsers.add_parser("backup", help="Backup Files/Folders")
    parser_backup.add_argument('-r', '--run', action=argparse.BooleanOptionalAction, help='run backup for all')
    parser_backup.add_argument('-a', '--alias', help='run for specific Alias')

    parser_restore = subparsers.add_parser("restore", help="Restore Files/Folders")
    parser_restore.add_argument('-a', '--alias', help='Restore Backup for Alias from the Backup System')
    
    # no idea if this is a good idea :D
    parser_config = subparsers.add_parser("config", help="Configuration")
    dest = config_data['backup_root']
    number = config_data['number']
    parser_config.add_argument('-b', '--backup_root', default=None, help=f"Location for all the Backups. Default {THIS_PATH}/archive, Current {dest}")
    parser_config.add_argument('-n', '--number', type=int, default=None, help=f"Maximum Backups for Alias. Default 5, Current {number}.")
    parser_config.add_argument('-s', '--show', action=argparse.BooleanOptionalAction, help='Show all Coanfigurations')
    parser_config.add_argument('--reset', action=argparse.BooleanOptionalAction, help='Reset Config to Default')

    args = parser.parse_args()

    try:        
        if args.subparser:
            sub = args.subparser
            
            if sub == "show":
                show_tool(args.all)
            
            elif sub == "add":
                add_tool(target=args.path, alias=args.alias)
                
            elif sub == "remove":
                remove_tool(alias=args.alias)
                
            elif sub == "backup":
                backup_tool(run=args.run, alias=args.alias)
                
            elif sub == "restore":
                restore_tool(alias=args.alias)
                
            elif sub == "config":
                if args.reset:
                    config_reset()
                    
                if args.backup_root:
                    config_update("backup_root", args.backup_root)
                
                if args.number:
                    config_update("number", args.number)
                    
                if args.show:
                    config_show()
                    
        else:
            parser.print_help()
        
        
    except Exception as e:
        print(e)
        
