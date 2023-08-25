import os
from datetime import timedelta
import logging
from cr3_exif import get_date, get_file_name, get_drive_mode, get_ev
logger = logging.getLogger('main')


def _are_within_threshold(dt_a, dt_b, threshold):
    return dt_b - dt_a < threshold

def _timestamps_within_threshold(metadata_a, metadata_b, threshold):
    return _are_within_threshold(get_date(metadata_a), get_date(metadata_b), threshold)

def _create_timestamp_threshold_evaluator(threshold):
    def time_threshold_evaluator(stack, candidate):
        last = stack[-1]
        if (_timestamps_within_threshold(last, candidate, threshold)):
            return True
        return False
    return time_threshold_evaluator

def _split_by_time_threshold(metadatas, threshold):
    logger.debug("Splitting by consecutive shot timestamp threshold of %s", threshold)
    return _split_by_generic(
        sorted(metadatas, key=lambda metadata: get_date(metadata)),
        [_create_timestamp_threshold_evaluator(threshold)]
    )

def _should_add_to_stack(stack, candidate, evaluators):
    all_ok = True
    for evaluator in evaluators:
        if (evaluator(stack, candidate) == False):
            all_ok = False
            break
    return all_ok

def _split_by_generic(metadatas, evaluators):
    stacks = []
    curr_stack = []
    curr_stack.append(metadatas[0])
    stacks.append(curr_stack)
    for curr in metadatas[1:]:
        if (_should_add_to_stack(curr_stack, curr, evaluators)):
            curr_stack.append(curr)
        else:
            curr_stack = []
            curr_stack.append(curr)
            stacks.append(curr_stack)
    return stacks


def _strip_file_ending(fname):
    return fname.rsplit('.', 1)[0]

def get_stack_label(stack):
    displayble_date_format = "%Y-%m-%d_%H-%M-%S.%f"
    start_date_str = get_date(stack[0]).strftime(displayble_date_format)[:-4]
    start_img_name = _strip_file_ending(get_file_name(stack[0]))
    end_img_name = _strip_file_ending(get_file_name(stack[-1]))
    stack_size_str = str(len(stack)).zfill(3)
    return "{0}__{1}-{2}__{3}".format(start_date_str, start_img_name, end_img_name, stack_size_str)

# Ideally all shots within single focus bracketing series should have similar exposure.
# If EV differs much within a stack it is either errornously interpreted as a single
# focus bracketing series or the series might be ruined due to large EV deviations.
def verify_consistent_ev(stack):
    return all(ev == get_ev(stack[0]) for ev in list(map(get_ev, stack)))

def search(metadatas, threshold_sec, continuous_drive, min_stack_size):
    logger.debug("Begin search_stacks, count %s", len(metadatas))
    threshold = timedelta(seconds=float(threshold_sec))
    min_stack_size = int(min_stack_size)
    continuous_drive = int(continuous_drive)

    stacks = _split_by_time_threshold(metadatas, threshold)
    logger.debug("Found %s potential stacks", len(stacks))

    stacks = [s for s in stacks if len(s) >= min_stack_size]
    logger.debug("  with at least %s images: %s", min_stack_size, len(stacks))

    stacks = [s for s in stacks if all(dm == continuous_drive for dm in list(map(get_drive_mode, s)))]
    logger.debug("  with '%s' drive mode: %s", continuous_drive, len(stacks))
    return stacks
