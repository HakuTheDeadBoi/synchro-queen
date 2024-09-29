import hashlib
import os

from app.filehandling import get_file_dir_list

def hash_file(filepath: str) -> str:
    hash = hashlib.md5()
    try:
        with open(filepath, "rb") as FILE:
            for chunk in iter(lambda: FILE.read(4096), b""):
                hash.update(chunk)
    except IOError as e:
        raise IOError from e
    return hash.hexdigest()

def hash_dir_content(dirpath: str) -> str:
    hash = hashlib.md5()
    file_list, dir_list = get_file_dir_list(dirpath)

    for file in sorted(file_list):
        hash.update(hash_file(file).encode("utf-8"))
        hash.update(file.replace(dirpath, "ROOT").encode("utf-8"))
    for directory in sorted(dir_list):
        hash.update(directory.replace(dirpath, "ROOT").encode("utf-8"))
    
    return hash.hexdigest()