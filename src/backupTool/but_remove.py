from backupTool import jsonio


def remove(files=None, alias=None):
    # get current files
    file_list = jsonio.read(files)
    if not file_list:
        exit()
    
    # check if alias exists, if it exists, remove
    if alias in file_list:
        del file_list[alias]
        jsonio.write(files, file_list) 
        print(f"removed {alias} from backup")