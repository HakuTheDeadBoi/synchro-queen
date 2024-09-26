import os

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
            else:
                filepaths.append(full_path)
    except IOError as e:
        raise IOError from e

    return filepaths, dirpaths

if __name__ == '__main__':
    files, dirs = get_file_dir_list("C:/testsrc")
    for file in files:
        print(file)
    for direc in dirs:
        print(direc)