import logging
import sys


def configure_logger() -> logging.Logger:
    logger = logging.getLogger("dbrocket")
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.INFO)
    return logger


logger = configure_logger()
