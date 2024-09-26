import os
from pathlib import Path

from app.hash import hash_dir_content, hash_file

def are_hashes_equal(src_path, replica_path):
    return hash_dir_content(src_path) == hash_dir_content(replica_path)

def get_changes(src_path, replica_path):
    pass
        

if __name__ == '__main__':
    pass
