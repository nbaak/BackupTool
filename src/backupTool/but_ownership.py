import os
import sys

def change_owner(path, uid, gid):
    os.chown(path, uid, gid)
    
def chown(folder, uid, gid):
    change_owner(folder, uid, gid)
    for root, folders, files in os.walk(folder):
        for folder in folders:
            path = os.path.join(root, folder)
            change_owner(path, uid, gid)
        
        for file in files:
            path = os.path.join(root, file)
            change_owner(path, uid, gid)
    
def get_owner(path, verbose=False):
    if verbose:
        print(f"user: {os.stat(path).st_uid} group: {os.stat(path).st_gid}")
    return os.stat(path).st_uid, os.stat(path).st_gid