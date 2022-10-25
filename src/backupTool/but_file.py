
import os

def is_dir(path) -> bool:
    return os.path.isdir(path)
    
def is_file(path) -> bool:
    return os.path.isfile(path)