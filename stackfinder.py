import os
import sys
import logging
import argparse
import focus_stack
import config
from io_util import get_file_list, copy_stack, with_xmp_extension
from cache import with_cache
from pyexif_wrapper import read_metadatas, write_tags
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
    parser.add_argument("-t", "--filetypes", help="file extensions", default=[".cr3"])
    parser.add_argument("--threshold", help="seconds between consecutive images to consider as same stack ", default=0.5)
    parser.add_argument("--continuous-drive", help="value for MakerNotes.ContinuousDrive", default=0)
    parser.add_argument("--min-stack-size", help="least amount of images to form a stack", default=2)
    parser.add_argument("--disable-cache", help="do not write or read cached metadata", action="store_true")
    parser.add_argument("--write-xmp", help="create xmp sidecar for labeling stacks", action="store_false")
    parser.add_argument("--copy-stacks", help="copy input_files to identified stacks under output_dir", action="store_false")
    parser.add_argument("--dry-run", help="do not copy or write anything, just display results", action="store_true")
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

    execute(input_files, output_dir, args.threshold, args.continuous_drive, args.min_stack_size, args.disable_cache, args.write_xmp, args.copy_stacks, args.dry_run)

def execute(input_files, output_dir, threshold_sec, continuous_drive, min_stack_size, flag_disable_cache, flag_write_xmp, flag_copy_stacks, flag_dry_run):
    if (len(input_files) == 0):
        logger.warning("No input files")
        return

    metadatas = read_files(input_files, flag_disable_cache)
    stacks = focus_stack.search(metadatas, threshold_sec, continuous_drive, min_stack_size)
    logger.info("Found %s stacks:\n> %s", len(stacks), "\n> ".join([focus_stack.get_stack_label(s) for s in stacks]))
    verify_evs(stacks)
    if flag_write_xmp:
        write_xmp(input_files, stacks, flag_dry_run)
    if flag_copy_stacks:
        include_xmp_sidecars = flag_write_xmp
        copy_stacks(input_files, output_dir, stacks, include_xmp_sidecars, flag_dry_run)

def read_files(input_files, flag_disable_cache):
    metadatas = []
    if (flag_disable_cache):
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

def write_xmp(input_files, stacks, flag_dry_run):
    for s in stacks:
        tags_list = ["-Label=Purple", "-xmp-dc:Title=Focus stack", "-xmp-dc:Description={0}".format(focus_stack.get_stack_label(s))]
        xmp_files = [with_xmp_extension(get_abs_file_path_for_stack_item(input_files, img)) for img in s]
        if not flag_dry_run:
            write_tags(tags_list, xmp_files)
        else :
            logger.debug("(dry-run) Writing tags %s to files %s", tags_list, xmp_files)

def copy_stacks(input_files, output_dir, stacks, include_xmp_sidecars, flag_dry_run):
    def get_abs_file_path_for_stack_item_internal(metadata) :
        return get_abs_file_path_for_stack_item(input_files, metadata)

    for s in stacks:
        copy_stack(s, get_abs_file_path_for_stack_item_internal, focus_stack.get_stack_label, output_dir, include_xmp_sidecars, flag_dry_run)

def get_abs_file_path_for_stack_item(input_files, metadata):
        files = [f for f in input_files if get_file_name(metadata) in f]
        assert len(files) == 1
        return files[0]

if __name__ == "__main__":
    main()
