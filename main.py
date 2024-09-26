import argparse
import hashlib
import os
import re
from datetime import datetime, timedelta

time_unit_table = {
    "s": 1,
    "m": 60,
    "h": 60**2,
    "d": (60**2)*24
}

def is_interval_valid(interval: str) -> bool:
    return re.match(r"^\d+[smhd]{1}$", interval) is not None

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

def get_file_dir_list(root: str) -> tuple[list[str], list[str]]:
    filepaths = []
    dirpaths = []

    try:
        for path in os.listdir(root):
            full_path = os.path.join(root, path)
            if os.path.isdir(full_path):
                files, dirs = get_file_dir_list(full_path)
                filepaths.extend(files)
                dirpaths.extend(dirs)
                if not os.listdir(full_path):
                    dirpaths.append(full_path)
            else:
                filepaths.append(full_path)
    except IOError as e:
        raise IOError from e

    return filepaths, dirpaths

def compare_folders(source: str, replica: str, fast_comparison: bool) -> None:
    return compare_metadata(source, replica) if fast_comparison else compare_hashes(source, replica)




def main():
    # parse args
    argparser = argparse.ArgumentParser()
    argparser.add_argument("source", type=str, help="Source folder you want to backup.")
    argparser.add_argument("replica",type=str, help="Destination folder you want to hold 'source' backup.")
    argparser.add_argument("logfile", type=str, help="Path to log file - created a new one if not exists.")
    argparser.add_argument("-i", "--interval", type=str, dest="interval", help="Check interval in format <number><unit> where unit is (s)econd|(m)inute|(h)our|(d)ay")
    group = argparser.add_mutually_exclusive_group()
    group.add_argument("-f", "--fast", action="store_true", help="Fast comparison, using metadata.")
    group.add_argument("-s", "--strict", action="store_true", help="Strict comparison using content hashing.")

    args = argparser.parse_args()

    # validate args
    if not os.path.isdir(args.source):
        raise Exception("Source path is not a valid folder path.")
    
    if not os.path.isdir(args.replica):
        raise Exception("Replica path is not a valid folder path")
    
    if not os.path.exists(args.logfile):
        file = open(args.logfile, "w")
        file.close()
    elif not os.path.isfile(args.logfile):
        raise Exception("Logfile path isn not a valid file path.")
    
    if not is_interval_valid(args.interval):
        raise Exception("Interval is not in a valid format. Example: for 50 seconds it should be '50s'.")
    else:
        interval_in_secs = int(args.interval[:-1] * time_unit_table[args.interval[-1]])
    
    # setting current time and time delta
    delta = timedelta(seconds=interval_in_secs)
    current_time = datetime.now()

    # initial run




    

if __name__ == '__main__':
    files, dirs = get_file_dir_list(os.getcwd())

    for f in files:
        print(f)

    print("###")

    for d in dirs:
        print(d)