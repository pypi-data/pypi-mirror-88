import logging
import sys
from .version import versionChecker

log = logging.getLogger()


def commands(downloader=None):
    """ Default main function for WAPT setup.py
    """

    logging_config = logging.StreamHandler(sys.stdout)
    logging_config.setFormatter(logging.Formatter('[%(asctime)s - %(levelname)8s] %(message)s'))
    log.addHandler(logging_config)
    log.setLevel(logging.INFO)

    if len(sys.argv) == 1:
        if downloader is not None:
            downloader()
    else:
        if sys.argv[1] == 'version-check':
            versionChecker()
