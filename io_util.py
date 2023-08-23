import os

def _absolute_file_paths(directory):
    path = os.path.abspath(directory)
    return [entry.path for entry in os.scandir(path) if entry.is_file()]

def get_file_list(input_dir, file_extensions):
    file_list = _absolute_file_paths(input_dir)
    return [f for f in file_list if os.path.isfile(f) if os.path.splitext(f)[1].lower() in file_extensions]
