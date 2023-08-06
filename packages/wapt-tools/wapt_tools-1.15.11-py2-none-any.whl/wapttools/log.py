import logging
import os


def logger(package):
    logger = logging.getLogger(package)
    logger.setLevel(logging.DEBUG)
    logfile = os.path.join(os.environ['SYSTEMROOT'], 'WAPT', 'logs', package + '.log')
    if not os.path.isdir(os.path.dirname(logfile)):
        os.makedirs(os.path.dirname(logfile))
    handler = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
