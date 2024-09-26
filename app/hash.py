import hashlib
import os

from app.files import get_file_dir_list

def hash_file(filepath):
    print(filepath)
    print(os.path.isfile(filepath))
    hash = hashlib.md5()
    try:
        with open(filepath, "rb") as FILE:
            for chunk in iter(lambda: FILE.read(4096), b""):
                hash.update(chunk)
    except IOError as e:
        print(f"Error reading file {filepath}: {e}.\nHalting...")
    return hash.hexdigest()

def hash_dir_content(dirpath):
    hash = hashlib.md5()
    file_list, dir_list = get_file_dir_list(dirpath)

    for file in sorted(file_list):
        hash.update(hash_file(file).encode("utf-8"))
        hash.update(file.replace(dirpath, "ROOT").encode("utf-8"))
    for directory in sorted(dir_list):
        hash.update(directory.replace(dirpath, "ROOT").encode("utf-8"))
    
    return hash.hexdigest()


if __name__ == '__main__':
    copy = hash_dir_content("./test")
    same = hash_dir_content("./dif_loc/test_same")
    dir_added  = hash_dir_content("./dif_loc/test_diradd")
    dir_removed = hash_dir_content("./dif_loc/test_dirrem")
    file_added = hash_dir_content("./dif_loc/test_fileadd")
    file_removed = hash_dir_content("./dif_loc/test_filerem")

    print(copy, same, copy == same, sep="-----\n", end="#####\n")
    print(copy, dir_added, copy == dir_added, sep="-----\n", end="#####\n")
    print(copy, dir_removed, copy == dir_removed, sep="-----\n", end="#####\n")
    print(copy, file_added, copy == file_added, sep="-----\n", end="#####\n")
    print(copy, file_removed, copy == file_removed, sep="-----\n", end="#####\n")