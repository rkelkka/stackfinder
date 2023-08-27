import os
import sys
import logging
import config
from io_util import get_file_list
from gooey import Gooey, GooeyParser
import config
from stackfinder import execute
import ast

logger = logging.getLogger('main')

@Gooey(advanced=True, default_size=(1000, 700))
def main():
    conf = config.read()

    input_dir = conf.get("IO", "input_dir", fallback=os.getcwd())
    # fallback works only if the option is completely missgin, not if it has empty value
    if not input_dir:
        input_dir = os.getcwd()
    output_dir = conf.get("IO", "output_dir", fallback=input_dir)

    # Convert a string that looks like a list into a real list
    file_extensions = ast.literal_eval(conf.get("IO", "file_extensions", fallback="['.cr3']"))
    threshold = conf.getfloat("FOCUS_STACK", "timestamp_threshold_sec", fallback=0.5)
    continuous_drive = conf.getint("FOCUS_STACK", "continuous_drive", fallback=0)
    min_stack_size = conf.getint("FOCUS_STACK", "min_stack_size", fallback=2)
    write_xmp = conf.getboolean("IO","write_xmp", fallback=True)
    copy_stacks = conf.getboolean("IO","copy_stacks", fallback=True)
    disable_cache = conf.getboolean("IO","disable_cache", fallback=False)
    dry_run = conf.getboolean("IO","dry_run", fallback=False)

    #Might also use MultiFileChooser with, gooey_options={'wildcard': "Canon RAW (*.cr3)|*.cr3"}
    parser = GooeyParser(description="My Cool GUI Program!")
    parser.add_argument("-i", "--input", metavar="Input dir", required=True, widget="DirChooser", default=input_dir, gooey_options={"default_path": input_dir})
    parser.add_argument("-o", "--output", metavar="Output dir (defaults to input directory)", widget="DirChooser")
    parser.add_argument("-t", "--file_extensions", metavar="File extensions", nargs='+', widget="Listbox", default=file_extensions, choices=[".cr3", ".jpg"])
    parser.add_argument("--threshold", metavar="Seconds between consecutive images", default=threshold, widget="DecimalField")
    parser.add_argument("--continuous-drive", metavar="MakerNotes.ContinuousDrive", default=continuous_drive, widget="Dropdown", choices=['0', '1', '2', '3', '4', '5'])
    parser.add_argument("--min-stack-size", metavar="Min stack size", default=min_stack_size, widget="IntegerField")
    parser.add_argument("--write-xmp", metavar="Write stack info to XMP sidecars", action="store_true", widget="CheckBox", gooey_options={'initial_value': write_xmp})
    parser.add_argument("--copy-stacks", metavar="Copy stacks to output dir", action="store_true", widget="CheckBox", gooey_options={'initial_value': copy_stacks})
    parser.add_argument("--disable-cache", metavar="Disable cache, slower", action="store_true", widget="CheckBox", gooey_options={'initial_value': disable_cache})
    parser.add_argument("--dry-run", metavar="Dry run", action="store_true", widget="CheckBox", gooey_options={'initial_value': dry_run})

    args = parser.parse_args()
    logger.debug("XMP WRITE %s, is it string %s", write_xmp, isinstance(write_xmp, str))
    logger.debug("ARGS XMP WRITE %s", args.write_xmp)
    input_dir = os.path.abspath(args.input)
    if (args.output is None):
        output_dir = input_dir
    else:
        output_dir = os.path.abspath(args.output)

    # It was late at night. Maybe default / initial_values for gooey were not working right when returning back to settings.
    file_extensions = args.file_extensions
    threshold = args.threshold
    continuous_drive = args.continuous_drive
    min_stack_size = args.min_stack_size
    write_xmp = args.write_xmp
    copy_stacks = args.copy_stacks
    disable_cache = args.disable_cache
    dry_run = args.dry_run

    logger.debug("Using input dir: %s", input_dir)
    logger.debug("Using output dir: %s", output_dir)

    input_files = get_file_list(input_dir, args.file_extensions)
    logger.info("Found %s %s files in %s", len(input_files), args.file_extensions, input_dir)
    logger.debug(" > %s", input_files)
    if (len(input_files) == 0):
        logger.warning("No input files found in %s", input_dir)
    else:
        execute(input_files, output_dir, threshold, continuous_drive, min_stack_size, disable_cache, write_xmp, copy_stacks, dry_run)

    config.set_val(conf, "IO", "input_dir", input_dir)
    config.set_val(conf, "IO", "output_dir", output_dir)
    config.set_val(conf, "IO", "file_extensions", file_extensions)
    config.set_val(conf, "FOCUS_STACK", "timestamp_threshold_sec", threshold)
    config.set_val(conf, "FOCUS_STACK", "continuous_drive", continuous_drive)
    config.set_val(conf, "FOCUS_STACK", "min_stack_size", min_stack_size)
    config.set_val(conf, "IO", "write_xmp", write_xmp)
    config.set_val(conf, "IO", "copy_stacks", copy_stacks)
    config.set_val(conf, "IO", "disable_cache", disable_cache)
    config.set_val(conf, "IO", "dry_run", dry_run)
    config.write(conf)
    logger.info("Done")


if __name__ == "__main__":
    main()
