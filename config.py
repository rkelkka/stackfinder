
from datetime import timedelta

FILE_EXTS = ['.cr3']
FOCUS_STACK = {
    "TIMESTAMP_THRESHOLD": timedelta(seconds=0.5),
    "CONTINUOUS_DRIVE": 0,
    "MIN_STACK_SIZE": 2,
}