from datetime import datetime

def get_date(metadata):
    date_format = '%Y:%m:%d %H:%M:%S.%f'
    return datetime.strptime(metadata["MakerNotes:TimeStamp"], date_format)

def get_source_file(metadata):
    # Includes relative path
    return metadata["SourceFile"]

def get_file_name(metadata):
    return metadata["File:FileName"]

# Bracketed images have single drive mode (0)
# This can be used to differentiate bracketed shots
# from other high speed bursts.
SINGLE_DRIVE_MODE = 0
def get_drive_mode(metadata):
    return metadata["MakerNotes:ContinuousDrive"]

def get_ev(metadata):
    return metadata["MakerNotes:MeasuredEV"]