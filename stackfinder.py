import os
import sys
import logging
import argparse
import focus_stack
import config
from io_util import get_file_list
from cache import with_cache
from pyexif_wrapper import read_metadatas

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
    args = parser.parse_args()
    input_dir = os.path.abspath(args.input)
    if (args.output is None):
        output_dir = input_dir

    logger.debug("Using input dir: %s", input_dir)
    logger.debug("Using output dir: %s", output_dir)

    file_list = get_file_list(input_dir, config.FILE_EXTS)
    logger.info("Found %s %s files in %s", len(file_list), config.FILE_EXTS, input_dir)
    if (len(file_list) == 0):
        logger.warning("No input files found in %s. Exiting.", input_dir)
        sys.exit()

    metadatas = []
    if (args.disable_cache):
        logger.warning("Cache disabled - reading metadatas may take several seconds.")
        metadatas = read_metadatas(file_list)
    else:
        metadatas = with_cache(file_list, read_metadatas)

    stacks = focus_stack.search(metadatas, config.FOCUS_STACK)
    logger.info("Found %s stacks:\n> %s", len(stacks), "\n> ".join([focus_stack.get_stack_label(s) for s in stacks]))
    for s in stacks:
        consistent_evs = focus_stack.verify_consistent_ev(s)
        if (consistent_evs == False):
            logger.warning("*** Stack %s has inconsistent EVs ***", focus_stack.get_stack_label(s))

    #no:stacking
    #if not dry--run
    # io: write stacks
    # what if already exists? ask overwrite?

if __name__ == "__main__":
    main()
