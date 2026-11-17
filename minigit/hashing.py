import hashlib
import os 
import json

def read_file(file_path):
    if os.path.isdir(file_path):
        raise IsADirectoryError
          
    with open(file_path,"r",encoding="utf-8") as file:
        content=file.read()
            
    return content 

def generate_hash(content):
    hash_content=hashlib.sha1(content.encode("utf-8")).hexdigest()
    return hash_content 

def store_object(content):
    hash_value=generate_hash(content)
    object_path=os.path.join(".minigit","objects",hash_value)

    if not os.path.exists(object_path):
        with open(object_path,"w",encoding="utf-8") as file:
            file.write(content)
    return hash_value

def load_index():
    if os.path.exists(".minigit/index.json"):       
        with open(".minigit/index.json","r",encoding="utf-8") as file:
            return json.load(file)            
    else:
        return {}

def save_index(data):
    with open(".minigit/index.json","w",encoding="utf-8") as file:
        json.dump(data,file,indent=4)

def add_file(path):
    loaded_index=load_index() 
    file_content=read_file(path)
    object_hash=store_object(file_content)
    loaded_index[path]=object_hash
    save_index(loaded_index)
    