import os
import sys
import logging
import config
from io_util import get_file_list
from gooey import Gooey, GooeyParser
import config
from stackfinder import execute

logger = logging.getLogger('main')

@Gooey(advanced=True, default_size=(1600, 600))
def main():
    conf = config.read()

    input_dir = conf["IO"]["input_dir"]
    if input_dir == None:
        input_dir = "<select>"
    output_dir = conf["IO"]["output_dir"]

    file_extensions = conf["IO"]["file_extensions"]
    threshold = conf["FOCUS_STACK"]["timestamp_threshold_sec"]
    continuous_drive = conf["FOCUS_STACK"]["continuous_drive"]
    min_stack_size = conf["FOCUS_STACK"]["min_stack_size"]

    #Might also use MultiFileChooser with, gooey_options={'wildcard': "Canon RAW (*.cr3)|*.cr3"}
    parser = GooeyParser(description="My Cool GUI Program!")
    parser.add_argument("-i", "--input", help="Input dir", required=True, widget="DirChooser", default=input_dir, gooey_options={"default_path": input_dir})
    parser.add_argument("-o", "--output", help="Output dir (defaults to input directory)", widget="DirChooser")
    parser.add_argument("-t", "--filetypes", help="File extensions", default=file_extensions)
    parser.add_argument("--threshold", help="Seconds between consecutive images", default=threshold, widget="DecimalField")
    parser.add_argument("--continuous-drive", help="MakerNotes.ContinuousDrive", default=continuous_drive, widget="Dropdown", choices=['0', '1', '2', '3', '4', '5'])
    parser.add_argument("--min-stack-size", help="Min stack size", default=min_stack_size, widget="IntegerField")
    # NOTE: store_true / store_false seem to work differently than with argparser.
    parser.add_argument("--write-xmp", help="Write stack info to XMP sidecars", action="store_true", widget="CheckBox", default=True)
    parser.add_argument("--copy-stacks", help="Copy stacks to output dir", action="store_true", widget="CheckBox", default=True)
    parser.add_argument("--disable-cache", help="Disable cache, slower", action="store_true", widget="CheckBox", default=False)
    parser.add_argument("--dry-run", help="Dry run", widget="CheckBox", action="store_true", default=False)
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

    conf["IO"]["input_dir"] = input_dir
    conf["IO"]["output_dir"] = output_dir
    conf["IO"]["file_extensions"] = args.filetypes
    conf["FOCUS_STACK"]["timestamp_threshold_sec"] = args.threshold
    conf["FOCUS_STACK"]["continuous_drive"] = args.continuous_drive
    conf["FOCUS_STACK"]["min_stack_size"] = args.min_stack_size
    config.write(conf)
    logger.info("Done")


if __name__ == "__main__":
    main()
