from os import walk, path as os_path, getcwd
from typing import List
from django.conf import settings

repo_root = os_path.join(getcwd(), settings.REPO_CLONE_PATH)

def filter_valid_filenames(filename_list, extension_allowed=None, root=None, with_root_path=False):
    allowed_filenames = filename_list

    if extension_allowed:
        allowed_filenames = filter(
            lambda file: file.endswith(extension_allowed),
            filename_list
        )

    if with_root_path:
        filenames = map(
            lambda file: os_path.join(root, file),
            allowed_filenames
        )
        return list(filenames)

    return list(allowed_filenames)


def extract_all_files_from_path(path: str, **kwargs) -> List[str]:
    ignore_paths = kwargs.pop('ignore_paths', None)
    extension_allowed = kwargs.pop('extension_allowed', "py")

    file_list = []
    next_directories = []
    walk_path = f"{repo_root}/{path}"
    walk_path = walk(walk_path)


    for root, directories, files in walk_path:
        # Collect files at the current level of original path
        file_routes = filter_valid_filenames(
            filename_list=files,
            extension_allowed=extension_allowed,
            root=path,
            with_root_path=True
        )
        file_list = file_routes

        if len(directories) > 0:
            next_directories = directories
        # Escape the walk loop
        break

    # Collect files from child directories
    for directory in next_directories:
        next_path = os_path.join(path, directory)

        # Skip if path is ignored
        if ignore_paths and next_path in ignore_paths:
            continue

        file_list += extract_all_files_from_path(path=next_path, **kwargs)

    return file_list