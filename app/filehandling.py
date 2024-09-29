import logging
import os
import shutil

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

def push_changes(changes: dict[str, str], source_root: str, replica_root: str) -> None:
    action = {
        "added": lambda path: (os.makedirs(os.path.dirname(path.replace(source_root, replica_root)), exist_ok=True), shutil.copy2(path, path.replace(source_root, replica_root))),
        "deleted": lambda path: os.remove(path),
        "changed": lambda path: shutil.copy2(path, path.replace(source_root, replica_root)),
        "folder added": lambda path: shutil.copytree(path, path.replace(source_root, replica_root)),
        "folder deleted": lambda path: os.rmdir(path)
    }

    for path, change in changes.items():
        logging.info(f"{path} -> {change}")
        action[change](path)