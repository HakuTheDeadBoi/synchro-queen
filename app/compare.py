import os

from app.filehandling import get_file_dir_list
from app.hash import hash_file

def compare_path_metadata(src_object_path: str, replica_object_path: str) -> bool:
    return (
        os.path.getsize(src_object_path) == os.path.getsize(replica_object_path) and
        os.path.getmtime(src_object_path) == os.path.getmtime(replica_object_path)
    )

# this compare tracks changes to avoid redundancy of the same run
# once discovered source and replica are not the same
def compare_folders(source_root: str, replica_root: str, fast_comparison: bool) -> dict[str, str]:
    src_files, src_empty_dirs = get_file_dir_list(source_root)
    rep_files, rep_empty_dirs = get_file_dir_list(replica_root)

    # format: path - change type
    changes = {}

    for source_file_path in src_files:
        replica_file_path = source_file_path.replace(source_root, replica_root)
        try:
            # check if unchanged
            # if not - track change
            unchanged = compare_path_metadata(source_file_path, replica_file_path) if fast_comparison else (hash_file(source_file_path) == hash_file(replica_file_path))
            if not unchanged:
                changes[source_file_path] = "changed"
            # always delete track to keep only files we haven't check if they are in source or not
            rep_files.remove(replica_file_path)
        except (FileNotFoundError, IOError):
            changes[source_file_path] = "added"

    if rep_files:
        for file in rep_files:
            changes[file] = "deleted"

    for source_folder_path in src_empty_dirs:
        replica_folder_path = source_folder_path.replace(source_root, replica_root)
        if replica_folder_path not in rep_empty_dirs:
            changes[source_folder_path] = "folder added"
        else:
            rep_empty_dirs.remove(replica_folder_path)
    
    if rep_empty_dirs:
        for folder in rep_empty_dirs:
            changes[folder] = "folder deleted"

    return changes

