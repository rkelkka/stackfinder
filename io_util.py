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
    return [f for f in file_list if os.path.isfile(f) if os.path.splitext(f)[1].lower() in file_extensions]

def copy_stack(stack, get_file_path_from_stack_item_fn, get_stack_label_fn, dest_base_dir, dry_run):
    stack_label = get_stack_label_fn(stack)
    stack_output_root = dest_base_dir + "/" + stack_label
    input_files = [get_file_path_from_stack_item_fn(s) for s in stack]
    if not dry_run:
        logger.info("Copy stack to %s", stack_output_root)
        Path(stack_output_root).mkdir(parents=True, exist_ok=True)
        for filename in input_files:
            logger.debug("> Copy file %s to %s", filename, stack_output_root)
            shutil.copy(filename, stack_output_root)
    else:
        logger.info("(dry-run) Copy stack to %s", stack_output_root)
        for filename in input_files:
            logger.debug("(dry-run) > Copy file %s to %s", filename, stack_output_root)

