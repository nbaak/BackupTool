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
    base = os.path.basename(destination)
    name = base.split('.')[0]
    format_ = base.split('.')[1]
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    shutil.make_archive(name, format_, archive_from, archive_to)
    shutil.move('%s.%s'%(name,format_), destination)
    
    
def unpack(archive, destination):
    with zipfile.ZipFile(archive, 'r') as zip_obj:
        zip_obj.extractall(destination)
        #zip_obj.extract(member='test_data',path=destination)
        
        # lst = zip_obj.namelist()
        #
        # for n in lst:
        #     print("-", n)
        #     zip_obj.extract(n, destination)

if __name__ == "__main__":
    pass