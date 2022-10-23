import os
import shutil
import pathlib

def get_abspath(target):
    return os.path.abspath(target)

def get_basename(path):
    return os.path.basename(path)

def copy(source, destination):
    make_dir(destination)
    destination = os.path.join(destination, get_basename(source))
    print(source, destination)
    if os.path.isfile(source):
        copy_file(source, destination)
        
    elif os.path.isdir(source):
        copy_fodler(source, destination)
        
def move(source, destination):
    shutil.move(source, destination)

def copy_file(source, destination):
    if os.path.isfile(source):
        shutil.copy(source, destination)

def copy_fodler(source_dir, destination_dir):
    try:
        shutil.copytree(source_dir, destination_dir)
    except Exception as e:
        print(e)
    
def remove_dir(path):
    try:
        shutil.rmtree(path)
        
    except Exception as e:
        print(e)
        
def fild_oldest_file(path):
    root = pathlib.Path(path)
    oldest = min(root.resolve().glob('**/*.zip'), key=os.path.getctime)
    newest = max(root.resolve().glob('**/*.zip'), key=os.path.getctime)
    #print(oldest)
    #print(newest)
    
    return oldest, newest
    
def find_all_zip_files(root):
    files = []
    
    for file in os.listdir(root):
        if file.endswith(".zip"):
            files.append(os.path.join(root, file))
    
    return files
    
def clean_up(path, max_files=5):
    files = find_all_zip_files(path)
    
    while len(files) > max_files:
        oldest, _ = fild_oldest_file(path) # detect
        #print(f"REMOVE: {oldest}")
        os.remove(oldest)   # delete
        files = find_all_zip_files(path)
        
def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    