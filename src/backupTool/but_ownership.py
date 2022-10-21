import os
import sys

def change_owner(path, uid, gid):
    os.chown(path, uid, gid)
    
def show_owner(path):
    print(f"user: {os.stat(path).st_uid} group: {os.stat(path).st_gid}")
    return os.stat(path).st_uid, os.stat(path).st_gid