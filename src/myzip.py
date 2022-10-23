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

def make_archive(source, destination):
    #http://www.seanbehan.com/how-to-use-python-shutil-make_archive-to-zip-up-a-directory-recursively-including-the-root-folder/
    base = os.path.basename(destination)
    name = base.split('.')[0]
    format_ = base.split('.')[1]
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    print(source, destination, archive_from, archive_to)
    shutil.make_archive(name, format_, archive_from, archive_to)
    shutil.move('%s.%s'%(name,format_), destination)

if __name__ == "__main__":
    pass