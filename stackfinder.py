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
#from gooey import Gooey

FORMAT = '[%(asctime)s.%(msecs)03d] %(levelname)8s - %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

#@Gooey
def main():
    input_dir = ""
    output_dir = ""

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="directory for input files (defaults current dir)", required=True)
    parser.add_argument("-o", "--output", help="directory for output stacks (defaults to input directory)")
    parser.add_argument("-t", "--filetypes", help="file extensions", default=[".cr3"])
    parser.add_argument("--threshold", help="seconds between consecutive images to consider as same stack ", default=0.5)
    parser.add_argument("--continuous-drive", help="value for MakerNotes.ContinuousDrive", default=0)
    parser.add_argument("--min-stack-size", help="least amount of images to form a stack", default=2)
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

    input_files = get_file_list(input_dir, args.filetypes)
    logger.info("Found %s %s files in %s", len(input_files), args.filetypes, input_dir)
    if (len(input_files) == 0):
        logger.warning("No input files found in %s. Exiting.", input_dir)
        sys.exit()

    execute(input_files, output_dir, args.threshold, args.continuous_drive, args.min_stack_size, args.disable_cache, args.dry_run)

def execute(input_files, output_dir, threshold_sec, continuous_drive, min_stack_size, disable_cache, dry_run):
    if (len(input_files) == 0):
        logger.warning("No input files")
        return

    metadatas = read_files(input_files, disable_cache)
    stacks = focus_stack.search(metadatas, threshold_sec, continuous_drive, min_stack_size)
    logger.info("Found %s stacks:\n> %s", len(stacks), "\n> ".join([focus_stack.get_stack_label(s) for s in stacks]))
    verify_evs(stacks)
    copy_stacks(input_files, output_dir, stacks, dry_run)

def read_files(input_files, disable_cache):
    metadatas = []
    if (disable_cache):
        logger.warning("Cache disabled - reading metadatas may take several seconds.")
        metadatas = read_metadatas(input_files)
    else:
        metadatas = with_cache(input_files, read_metadatas)
    return metadatas

def verify_evs(stacks):
    for s in stacks:
        consistent_evs = focus_stack.verify_consistent_ev(s)
        if (consistent_evs == False):
            logger.warning("*** Stack %s has inconsistent EVs ***", focus_stack.get_stack_label(s))

def copy_stacks(input_files, output_dir, stacks, dry_run):
    def get_abs_stack_file_path(stack) :
        files = [f for f in input_files if get_file_name(stack) in f]
        assert len(files) == 1
        return files[0]

    for s in stacks:
        copy_stack(s, get_abs_stack_file_path, focus_stack.get_stack_label, output_dir, dry_run)

if __name__ == "__main__":
    main()
