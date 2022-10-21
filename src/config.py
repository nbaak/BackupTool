from configparser import ConfigParser
import os 
# https://docs.python.org/3/library/configparser.html
# Get the configparser object
config_object = ConfigParser()

def sections(file):
    config_object.read(file)
    print("SECTIONS", config_object.sections())

def create(file, section, inital_data:dict=None):
    if not os.path.exists(file):
        config_object[section] = {}
        with open(file, 'w') as f:
            config_object.write(f)
        
        if inital_data:
            update(file, section, inital_data)
        
    else:
        #print(f"File: '{file}' already exists")
        pass

def update(file, section, data_dict:dict):
    config_object.read(file)
    data = config_object[section]
    
    for key, value in data_dict.items():
        data[key] = str(value)
    
    with open(file, 'w') as f:
        config_object.write(f)
        
def read(file, section=None):
    if not section:
        return config_object.read(file)
    else:
       config_object.read(file)
       return config_object[section]