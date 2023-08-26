from exiftool import ExifToolHelper
from datetime import datetime
from exiftool import ExifToolHelper
import logging
logger = logging.getLogger('main')

def read_metadatas(file_list):
    with ExifToolHelper() as et:
        start_time = datetime.now()
        logger.debug("Begin ExifToolHelper get_metadata for %s files", len(file_list))
        metadatas = et.get_metadata(file_list)
        end_time = datetime.now()
        logger.debug("Done. Elapsed time: %s", end_time - start_time)
        return metadatas

def write_tags(tags_list, file_list):
    """
    https://github.com/sylikc/pyexiftool/blob/master/docs/source/examples.rst
    For example
    Command line: exiftool -XMPToolKit -Subject rose.jpg
    ExifToolHelper: execute("-XMPToolKit", "-Subject", "rose.jpg")

    Second example:
    exiftool -P -DateTimeOriginal="2021:01:02 03:04:05" -MakerNotes= "spaces in filename.jpg"
    execute(*["-P", "-DateTimeOriginal=2021:01:02 03:04:05", "-MakerNotes=", "spaces in filename.jpg"])
    """
    with ExifToolHelper() as et:
        start_time = datetime.now()
        logger.debug("Begin ExifToolHelper execute for writing tags %s for %s files", tags_list, len(file_list))
        metadatas = et.execute(*tags_list, *file_list)
        end_time = datetime.now()
        logger.debug("Done. Elapsed time: %s", end_time - start_time)
        return metadatas