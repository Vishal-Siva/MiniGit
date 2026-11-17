import os 
import datetime 
import json 
from minigit.hashing import load_index,save_index,read_file,generate_hash

def generate_commit_id(filepath):
    commits = os.listdir(filepath)
    numbers = []
    for filename in commits:
        if filename.endswith(".json"):
            number = int(filename.split("_")[1].split(".")[0])
            numbers.append(number)

    highest = max(numbers, default=0)
    next_number = highest + 1

    return f"COMMIT_{next_number:03d}"

def get_timestamp():
    time=datetime.datetime.now()
    s_time=time.strftime("%Y-%m-%d %H:%M:%S")
    return s_time

def create_commit(message):
    if not message.strip():
        print("Commit message cant be empty")
        return
    files=load_index()
    if not files:
        print("Nothing to commit")
        return 
    commit_id=generate_commit_id(".minigit/commit")
    time_stamp=get_timestamp()
    commit_data={
        "commit_id":commit_id,
        "message":message,
        "timestamp": time_stamp,
        "files":files
    }
    save_commit(commit_data)
    update_branch_pointer(commit_id)
    return commit_id
def save_commit(commit_data):
    commit_id=commit_data["commit_id"]
    path=os.path.join(".minigit","commit",commit_id +".json")

    with open(path,"w",encoding="utf-8") as file:
        json.dump(commit_data,file,indent=4)

    print(f"Commit {commit_id} created successfully!")


def show_history():
    commit_files=sorted(os.listdir(".minigit/commit"),reverse=True)
    if not commit_files:
        print("No commits found.")
        return
    for filename in commit_files:
        commit_path=os.path.join(".minigit","commit",filename)
        with open(commit_path,"r",encoding="utf-8") as file:
            commit_data=json.load(file)

        print("----------------------------------------")
        print("Commit ID: ",commit_data["commit_id"])
        print("Message: ",commit_data["message"])
        print("Timestamp: ",commit_data["timestamp"])
        print("----------------------------------------")



def load_commit(commit_id):
    path=os.path.join(".minigit","commit",commit_id+".json")
    with open(path,"r",encoding="utf-8") as file:
        commit_data=json.load(file)
    return commit_data

def restore_file(commit_id,filename):
    try:
        commit_data=load_commit(commit_id)
    except FileNotFoundError:
        print("Commit Not Found")
        return
    except json.JSONDecodeError:
        print("The commit file contains invalid JSON")
        return

    if filename not in commit_data["files"]:
        print("File not found in this commit.")
        return
    file_hash=commit_data["files"][filename]
    object_path=os.path.join(".minigit","objects",file_hash)
    if not os.path.exists(object_path):
        print("Object not found. Cannot restore this file.")
        return
    try:
        with open(object_path,"r",encoding="utf-8") as file:
            restored_content=file.read()
    except PermissionError:
        print("The permission is denied for reading this file")
        return
    parent_dir = os.path.dirname(filename)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
    try:
        with open(filename,"w",encoding="utf-8") as file:
            file.write(restored_content)
    except PermissionError:
        print("The permission is denied while restoring this file")
        return
    print("Successfully File restored!")

def create_branch(branch_name):
    if not branch_name or branch_name in (".", ".."):
        print("Invalid branch name.")
        return

    if "/" in branch_name or "\\" in branch_name:
        print("Branch name cannot contain path separators.")
        return
    branch_path=os.path.join(".minigit","branches",branch_name)
    if os.path.exists(branch_path):
        print("the branch already exists")
    else:
        with open(".minigit/HEAD","r",encoding="utf-8") as file:
            current_branch=file.read().strip()

        current_branch_path=os.path.join(".minigit","branches",current_branch)
        with open(current_branch_path,"r",encoding="utf-8") as file:
                    current_commit_id=file.read().strip()

        if not current_commit_id:
            print("we cannot create the branch before the first commit")
            return
        with open(branch_path,"w",encoding="utf-8") as file:
            file.write(current_commit_id)

def update_branch_pointer(commit_id):
    with open(".minigit/HEAD","r",encoding="utf-8") as file:
        branch_name=file.read().strip()

    branch_file_path=os.path.join(".minigit","branches",branch_name)

    with open(branch_file_path,"w",encoding="utf-8") as file:
        file.write(commit_id)

def switch_branch(branch_name):

    target_branch_path=os.path.join(".minigit","branches",branch_name)

    if not os.path.exists(target_branch_path):
        print("Branch Not Found")
        return
    try:
        with open(".minigit/HEAD","r",encoding="utf-8") as file:
            current_branch=file.read().strip()
            if not current_branch:
                print("HEAD file is empty. Repository configuration is invalid.")
                return
    except FileNotFoundError:
        print("Repository HEAD file not found. Initialize the repository.")
        return

    if current_branch==branch_name:
        print("Already on branch:",branch_name)
        return
    try:
        current_branch_path = os.path.join(".minigit", "branches",current_branch)

        with open(current_branch_path, "r", encoding="utf-8") as file:
            current_commit_id = file.read().strip()
    except FileNotFoundError:
        print("Current branch pointer not found.")
        return 

    if not current_commit_id:
        print("current branch has no commits")
        return 
    try:
        current_commit_data=load_commit(current_commit_id)
    except FileNotFoundError:
        print("The file is not found")
        return 
    except json.JSONDecodeError:
        print("current branch commit contains the invalid json")
        return


    if has_uncommitted_changes(current_commit_data):
        print("Commit before switching")
        return
    try:
        with open(target_branch_path,"r",encoding="utf-8") as file:
            target_commit_id=file.read().strip()
    except FileNotFoundError:
        print("Target Branch Pointer is not found ")
        return

    if not target_commit_id:
        print("there target branch has no commits")
        return
    
    try:
        target_commit_data=load_commit(target_commit_id)
    except FileNotFoundError:
        print("The target branch commit is not found")
        return 
    except json.JSONDecodeError:
        print("The target branch commit contains the invalid json")
        return 

    
    current_branch_files=set(current_commit_data["files"].keys())
    target_branch_files=set(target_commit_data["files"].keys())
    verified_object={}
    for filename,file_hash in target_commit_data["files"].items():
        object_path=os.path.join(".minigit","objects",file_hash)
        if not os.path.exists(object_path):
            print("The Object is missing:",filename)
            return
        try:
            with open(object_path, "r", encoding="utf-8") as file:
              object_content = file.read()
        except FileNotFoundError:
            print("The Object is not Found")
            return
        except PermissionError:
            print("The permission is denied")
            return
        actual_hash = generate_hash(object_content)

        if actual_hash != file_hash:
            print("Object is corrupted:", filename)
            return
        verified_object[filename]=object_content

    excess_files=current_branch_files-target_branch_files

    if excess_files:
        try:
            for filename in excess_files:
                os.remove(filename)
        except FileNotFoundError:
            print("The File is not Found")
            return
        except PermissionError:
            print("The permission is denied")
            return
    
    for filename,file_hash in target_commit_data["files"].items():

        restored_content=verified_object[filename]

        parent_dir=os.path.dirname(filename)
        if parent_dir:
            os.makedirs(parent_dir,exist_ok=True)
        try:
            with open(filename,"w",encoding="utf-8") as file:
                file.write(restored_content)
        except FileNotFoundError:
            print("The File is not Found")
            return
        except PermissionError:
            print("The Permission is denied")
            return  

    save_index(target_commit_data["files"])
    with open(".minigit/HEAD","w",encoding="utf-8") as file:
        file.write(branch_name)
    print("The Branch is Switched!")


def check_file_changes(current_hash, commit_hash):
    return current_hash!=commit_hash

def has_uncommitted_changes(commit_data):

    working_files = os.walk(".")
    tracked_files = set(commit_data["files"].keys())

    ignored_files = {".minigit", "minigit", "tests",".git", "__pycache__", ".venv"}
    for root,dirs,files in working_files:
        dirs[:]=[d for d in dirs if d not in ignored_files]

        for filename in files:
         file_path = os.path.join(root, filename)
         relative_path = os.path.relpath(file_path, ".")
         relative_path = relative_path.replace(os.sep, "/")

         if relative_path not in tracked_files:
            print("Untracked File:",relative_path)
            return True
        
    for filename, commit_hash in commit_data["files"].items():

        if not os.path.exists(filename):
            print("Missing File name:",filename)
            return True
      
        current_file=read_file(filename)
        current_hash=generate_hash(current_file)

        if commit_hash != current_hash:
            print("Modified File:",filename)
            return True
        
    return False
    