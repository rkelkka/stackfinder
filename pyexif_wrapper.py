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