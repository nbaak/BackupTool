#!/usr/bin/env python3

import argparse
import pathlib
import os
import backupTool as but
from backupTool.but_file import is_file

def init_cfg(root_path, cfg_file, cfg_section):
    but.config_reset(root_path, cfg_file, cfg_section)
    #config.create(CFG_FILE, CFG_SECTION, {'backup_root': f"{root_path}/archive", 'number': 5}) # initial

if __name__ == '__main__':
    THIS_PATH = pathlib.Path(__file__).parent.resolve()
    CFG_FILE = os.path.join(THIS_PATH, "config.ini")
    CFG_SECTION = "backuptool"
    
    if not is_file(CFG_FILE):
        init_cfg(THIS_PATH, CFG_FILE, CFG_SECTION)
        
    config = but.read_config(CFG_FILE, CFG_SECTION)
    
    FILE_TABLE = os.path.join(THIS_PATH, "files.json")
    BACKUP_ARCHIVE = config['backup_root']
    TMP_ARCHIVE = os.path.join(THIS_PATH, "tmp")
    
    #config = config.read(CFG_FILE, CFG_SECTION)
    
    parser = argparse.ArgumentParser(prog='BackupTool', description='Backup Tool')
    subparsers = parser.add_subparsers(dest="subparser")

    parser_show = subparsers.add_parser("show", help="Show Files/Folders in Backup", description="Show Files/Folders in Backup")
    parser_show.add_argument('-d', '--details', action=argparse.BooleanOptionalAction, help='show more details')
    parser_show.add_argument('-a', '--alias', type=str, default=None, help='show details for specific alias')


    parser_add = subparsers.add_parser("add", help="Add a Files/Folders to the Backup System")
    parser_add.add_argument('path', metavar='path', type=str, help="Path to File/Folder")
    parser_add.add_argument('-a', '--alias', default=None, help='Alias for the Backup System')


    parser_remove = subparsers.add_parser("remove", help="Remove a File/Folder from the Backup System")
    parser_remove.add_argument('alias', metavar='alias', type=str, help="Alias for Path/Folder")


    parser_backup = subparsers.add_parser("backup", help="Backup Files/Folders")
    parser_backup.add_argument('-r', '--run', action=argparse.BooleanOptionalAction, help='run backup for all')
    parser_backup.add_argument('-a', '--alias', help='run for specific Alias')

    parser_restore = subparsers.add_parser("restore", help="Restore Files/Folders")
    #parser_restore.add_argument('-a', '--alias', help='Restore Backup for Alias from the Backup System')
    parser_restore.add_argument('alias', metavar='alias', type=str, help="Restore Backup for Alias from the Backup System")
    parser_restore.add_argument('-r', '--run', action=argparse.BooleanOptionalAction, help='run restore for alias')
    parser_restore.add_argument('-v', '--version', default=0, type=int, help='Nummber of Backup you want to restore, default 0.')
    
    # no idea if this is a good idea :D
    parser_config = subparsers.add_parser("config", help="Configuration")
    dest = config['backup_root']
    number = config['number']
    parser_config.add_argument('-b', '--backup_root', default=None, help=f"Location for all the Backups. Default {THIS_PATH}/archive, Current {dest}")
    parser_config.add_argument('-n', '--number', type=int, default=None, help=f"Maximum Backups for Alias. Default 5, Current {number}.")
    parser_config.add_argument('-s', '--show', action=argparse.BooleanOptionalAction, help='Show all Coanfigurations')
    parser_config.add_argument('--reset', action=argparse.BooleanOptionalAction, help='Reset Config to Default')

    args = parser.parse_args()

    try:        
        if args.subparser:
            sub = args.subparser
            
            if sub == "show":
                but.show(config, FILE_TABLE, args.details, args.alias)
            
            elif sub == "add":
                but.add(FILE_TABLE, target=args.path, alias=args.alias)
                
            elif sub == "remove":
                but.remove(FILE_TABLE, alias=args.alias)
                
            elif sub == "backup":
                but.backup(config, FILE_TABLE, BACKUP_ARCHIVE, run=args.run, alias=args.alias)
                
            elif sub == "restore":
                but.restore(BACKUP_ARCHIVE, TMP_ARCHIVE, FILE_TABLE, alias=args.alias, run=args.run, version=args.version)
                
            elif sub == "config":
                if args.reset:
                    but.config_reset(THIS_PATH, CFG_FILE, CFG_SECTION)
                    
                if args.backup_root:
                    but.config_update(CFG_FILE, CFG_SECTION, "backup_root", args.backup_root)
                
                if args.number:
                    but.config_update(CFG_FILE, CFG_SECTION, "number", args.number)
                    
                if args.show:
                    but.config_show(CFG_FILE, CFG_SECTION)
                    
        else:
            parser.print_help()
        
        
    except Exception as e:
        print(e)
        
