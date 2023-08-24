import os
import sys
import logging
import argparse
import focus_stack
import config
from io_util import get_file_list, copy_stack
from cache import with_cache
from pyexif_wrapper import read_metadatas
from cr3_exif import get_file_name

FORMAT = '[%(asctime)s.%(msecs)03d] %(levelname)8s - %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

def main():
    input_dir = ""
    output_dir = ""

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="directory for input files (defaults current dir)", required=True)
    parser.add_argument("-o", "--output", help="directory for output stacks (defaults to input directory)")
    parser.add_argument("--disable-cache", help="do not write or read cached metadata", action="store_true")
    parser.add_argument("--dry-run", help="do not copy anything, just display results", action="store_true")
    args = parser.parse_args()
    input_dir = os.path.abspath(args.input)
    if (args.output is None):
        output_dir = input_dir
    else:
        output_dir = os.path.abspath(args.output)

    logger.debug("Using input dir: %s", input_dir)
    logger.debug("Using output dir: %s", output_dir)

    conf = config.read()

    file_list = get_file_list(input_dir, conf["IO"]["file_extensions"])
    logger.info("Found %s %s files in %s", len(file_list), conf["IO"]["file_extensions"], input_dir)
    if (len(file_list) == 0):
        logger.warning("No input files found in %s. Exiting.", input_dir)
        sys.exit()

    metadatas = []
    if (args.disable_cache):
        logger.warning("Cache disabled - reading metadatas may take several seconds.")
        metadatas = read_metadatas(file_list)
    else:
        metadatas = with_cache(file_list, read_metadatas)

    stacks = focus_stack.search(metadatas, conf)
    logger.info("Found %s stacks:\n> %s", len(stacks), "\n> ".join([focus_stack.get_stack_label(s) for s in stacks]))
    for s in stacks:
        consistent_evs = focus_stack.verify_consistent_ev(s)
        if (consistent_evs == False):
            logger.warning("*** Stack %s has inconsistent EVs ***", focus_stack.get_stack_label(s))

    def get_abs_stack_file_path(stack) : return input_dir + "/" + get_file_name(stack)
    for s in stacks:
        copy_stack(s, get_abs_stack_file_path, focus_stack.get_stack_label, output_dir, args.dry_run)

if __name__ == "__main__":
    main()
