import os
import logging
from pathlib import Path
import shutil

logger = logging.getLogger('main')

def _absolute_file_paths(directory):
    path = os.path.abspath(directory)
    return [entry.path for entry in os.scandir(path) if entry.is_file()]

def get_file_list(input_dir, file_extensions):
    file_list = _absolute_file_paths(input_dir)
    logger.debug("file_list: %s", file_list)
    return  [f for f in file_list if f.lower().endswith(tuple(file_extensions))]

def do_file_action_on_stack(stack, get_file_path_from_stack_item_fn, get_stack_label_fn, dest_base_dir, file_action, include_xmp_sidecars, dry_run):
    stack_label = get_stack_label_fn(stack)
    stack_output_root = os.path.join(dest_base_dir, stack_label)
    input_files = [get_file_path_from_stack_item_fn(img) for img in stack]
    if include_xmp_sidecars:
        xmp_files = [with_xmp_extension(f) for f in input_files]
        files = [val for pair in zip(input_files, xmp_files) for val in pair]
    else:
        files = input_files
    do_file_action_on_files(files, stack_output_root, file_action, dry_run)

def do_file_action_on_files(files_to_copy, dest_dir, file_action, dry_run):
    if not dry_run:
        logger.debug("Copy / move stack to %s", dest_dir)
        Path(dest_dir).mkdir(parents=True, exist_ok=True)
        for filename in files_to_copy:
            match file_action:
                case "copy":
                    logger.debug("> Copy file %s to %s", filename, dest_dir)
                    shutil.copy(filename, dest_dir)
                case "move":
                    logger.debug("> Move file %s to %s", filename, dest_dir)
                    shutil.move(filename, dest_dir)
    else:
        logger.debug("(dry-run) Copy / move stack to %s", dest_dir)
        for filename in files_to_copy:
            logger.debug("(dry-run) > Copy / move file %s to %s", filename, dest_dir)


def with_xmp_extension(file):
    return os.path.splitext(file)[0]+'.xmp'