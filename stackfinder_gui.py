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

about_desc = """Finds images which form a focus stack / bracking series and copies each stack to ouput directories.

Based on
 - PyExifTool - A Python wrapper for Phil Harvey's ExifTool (https://smarnach.github.io/pyexiftool/)
 - ExifTool by Phil Harvey (https://exiftool.org/)
 - Icon by <a href="https://freeicons.io/profile/5790">ColourCreatype</a> on <a href="https://freeicons.io">freeicons.io</a>
"""

menu_about = {
    'type': 'AboutDialog',
    'menuTitle': 'About',
    'name': 'Stackfinder GUI',
    'description': about_desc,
    'version': '0.0.1',
    'copyright': '2023',
    'website': 'https://github.com/rkelkka/stackfinder',
    'developer': 'https://github.com/rkelkka',
    'license': 'MIT',
}

# https://stackoverflow.com/questions/58470789/merging-py-file-and-txt-files-into-exe-file-using-pyinstaller/58474133#58474133
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

@Gooey(advanced=True, default_size=(1000, 700), program_name="Stackfinder GUI", menu=[{'name': 'Help', 'items': [menu_about]}], image_dir=resource_path('icons'))
def main():
    logger.info("Stackfinder GUI started.")
    conf = config.read()

    input_dir = conf.get("IO", "input_dir", fallback=os.getcwd())
    # fallback works only if the option is completely missing, not if it has empty value
    if not input_dir:
        input_dir = os.getcwd()
    # Output dir is intentionally not filled as default to argparser as my default use case is to use input_dir + subdir.
    #output_dir = conf.get("IO", "output_dir", fallback=os.path.join(input_dir, 'focus_stacks'))

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
    parser.add_argument("-o", "--output", metavar="Optional output dir (defaults to input_dir/focus_stacks)", widget="DirChooser")
    parser.add_argument("-t", "--file_extensions", metavar="File extensions", nargs='+', widget="Listbox", default=file_extensions, choices=[".cr3", ".jpg"])
    parser.add_argument("--threshold", metavar="Seconds between consecutive images", default=threshold, widget="DecimalField")
    parser.add_argument("--continuous-drive", metavar="MakerNotes.ContinuousDrive", default=continuous_drive, widget="Dropdown", choices=['0', '1', '2', '3', '4', '5'])
    parser.add_argument("--min-stack-size", metavar="Min stack size", default=min_stack_size, widget="IntegerField")
    parser.add_argument("--write-xmp", metavar="Write stack info to XMP sidecars", action="store_true", widget="CheckBox", gooey_options={'initial_value': write_xmp})
    parser.add_argument("--copy-stacks", metavar="Copy stacks to output dir", action="store_true", widget="CheckBox", gooey_options={'initial_value': copy_stacks})
    parser.add_argument("--disable-cache", metavar="Disable cache, slower", action="store_true", widget="CheckBox", gooey_options={'initial_value': disable_cache})
    parser.add_argument("--dry-run", metavar="Dry run", action="store_true", widget="CheckBox", gooey_options={'initial_value': dry_run})

    args = parser.parse_args()
    for arg, value in vars(args).items():
        logging.info("  Argument %s: %r", arg, value)
    input_dir = os.path.abspath(args.input)
    if (args.output is None):
        # Default to input_dir/focus_stacks.
        output_dir = os.path.join(input_dir, 'focus_stacks')
    else:
        # However, if output is explicitly selected, use that without any additions.
        output_dir = os.path.abspath(args.output)
    logger.info("Using input_dir: %s", input_dir)
    logger.info("Using output_dir: %s", output_dir)

    input_files = get_file_list(input_dir, args.file_extensions)
    logger.info("Found %s %s files in %s", len(input_files), args.file_extensions, input_dir)
    logger.debug(" > %s", input_files)
    if (len(input_files) == 0):
        logger.warning("No input files found in %s", input_dir)
    else:
        execute(input_files, output_dir, args.threshold, args.continuous_drive, args.min_stack_size, args.disable_cache, args.write_xmp, args.copy_stacks, args.dry_run)

    config.set_val(conf, "IO", "input_dir", input_dir)
    config.set_val(conf, "IO", "output_dir", args.output) # store output_dir only when explicitly supplied
    config.set_val(conf, "IO", "file_extensions", args.file_extensions)
    config.set_val(conf, "FOCUS_STACK", "timestamp_threshold_sec", args.threshold)
    config.set_val(conf, "FOCUS_STACK", "continuous_drive", args.continuous_drive)
    config.set_val(conf, "FOCUS_STACK", "min_stack_size", args.min_stack_size)
    config.set_val(conf, "IO", "write_xmp", args.write_xmp)
    config.set_val(conf, "IO", "copy_stacks", args.copy_stacks)
    config.set_val(conf, "IO", "disable_cache", args.disable_cache)
    config.set_val(conf, "IO", "dry_run", args.dry_run)
    config.write(conf)
    logger.info("Done")


if __name__ == "__main__":
    main()
