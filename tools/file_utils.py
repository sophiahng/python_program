import os


__all__ = ['path_check', 'path_exist']


def path_check(file_path):
    if os.path.isdir(file_path):
        file_subdir = file_path
    else:
        file_subdir = os.path.dirname(file_path)
    if not os.path.exists(file_subdir):
        os.mkdir(file_subdir)


def path_exist(file_path):
    if os.path.exists(file_path):
        return True
    return False






