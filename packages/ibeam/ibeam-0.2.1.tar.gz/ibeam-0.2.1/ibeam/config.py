import logging
import os
import sys
from pathlib import Path

initialized = False


def initialize():
    global initialized
    if initialized: return
    initialized = True

    logger = logging.getLogger('ibeam')
    # logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)s|%(levelname)-.1s| %(message)s'))
    logger.addHandler(stream_handler)

    _this_filedir = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, str(Path(_this_filedir).parent))
