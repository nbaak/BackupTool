import os
import shutil
import tarfile

def create(folder, filename):
    try:
        with tarfile.TarFile(filename, 'w') as target:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    shard = os.path.join(root, file)
                    print(f"adding: ", shard, file)
                    target.add(file)
    
    except Exception as e:
        print(e)

def create2(input, output):
    with tarfile.TarFile(output, 'w') as f:
        f.add(input)


def unpack(archive, destination):
    with tarfile.TarFile(archive, 'r:gz') as zip_obj:
        zip_obj.extractall(destination)
        
if __name__ == "__main__":
    pass