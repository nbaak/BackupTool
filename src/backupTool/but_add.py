
from .jsonio import read, write
import pathlib
import string
import random

from .but_file import is_dir, is_file


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

def add(files=None, target=None, alias=None):
    # get current files
    file_list = read(files)
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
        write(files, file_list)       
        print(f"added {path} to the backup system as {alias}")