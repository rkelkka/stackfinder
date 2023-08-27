import pickle
import hashlib
import json
import logging
import os
logger = logging.getLogger('main')

CACHE_DIR_REL_TO_WD = '.cache'
def _ensure_cache_dir_exists():
    if not os.path.exists(CACHE_DIR_REL_TO_WD):
        os.makedirs(CACHE_DIR_REL_TO_WD)

def _digest(list):
    bytez = pickle.dumps(list)
    list_hash = hashlib.md5(bytez)
    return list_hash.hexdigest()

def _get_cache_file_path(input_files):
    return os.path.join(CACHE_DIR_REL_TO_WD, _digest(input_files) + ".json")

def _write(path, data):
    logger.debug("Writing cached metadata: %s", path)
    _ensure_cache_dir_exists()
    with open(path, "w+") as fp:
        json.dump(data, fp)

def _read(path):
    logger.debug("Reading cached metadata: %s", path)
    if os.path.isfile(path):
        with open(path, "r") as fp:
            return json.load(fp)
    else:
        None

def with_cache(input_files, reader_fn):
    cache_file_path = _get_cache_file_path(input_files)
    cached = _read(cache_file_path)
    if (cached):
        logger.info("Found cached metadata: %s", cache_file_path)
        return cached
    else:
        logger.info("Cached metadata not found, reading metadata from files. This can take sevaral seconds for large number of images.")
        data = reader_fn(input_files)
        logger.info("Read done, writing cached metadata: %s", cache_file_path)
        _write(cache_file_path, data)
        return data