import os
import shutil
import zipfile

def create(folder, filename, compress=zipfile.ZIP_DEFLATED):
    try:
        with zipfile.ZipFile(filename + '.zip', 'w', compress) as target:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    add = os.path.join(root, file)
                    target.write(add)
                    print(add)
    
    except Exception as e:
        print(e)
        
        
def mkarchive(source, destination):
    # this one is to check how shutil.make_archive mighe work..
    base = os.path.basename(destination)
    name = base.split('.')[0]
    format_ = base.split('.')[1]
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source):
            for file in files:
                try:
                    print(file)
                    a = os.path.join(root, file)
                    b = os.path.relpath(a, source)
                    print(a)
                    print(b)
                    zf.write(b)
                except Exception as e:
                    print(e)
    

def make_archive(source, destination):
    base = os.path.basename(destination)
    name = base.split('.')[0]
    format_ = base.split('.')[1]
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    shutil.make_archive(name, format_, archive_from, archive_to)
    shutil.move(f'{name}.{format_}', destination)
    
    # print("__INFO__")
    # print(archive_from)
    # print(archive_to)
    # print('abs', os.path.abspath(f'{name}.{format_}'))
    # print('mv', f'{name}.{format_}', 'to', destination)
    
    
def unpack(archive, destination):
    with zipfile.ZipFile(archive, 'r') as zip_obj:
        zip_obj.extractall(destination)

if __name__ == "__main__":
    pass