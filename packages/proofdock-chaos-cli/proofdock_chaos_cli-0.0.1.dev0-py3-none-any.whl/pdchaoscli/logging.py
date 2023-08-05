# -*- coding: utf-8 -*-
import logging

import logzero
from logzero import LogFormatter, setup_default_logger, ForegroundColors


__all__ = ["configure_logger"]


def configure_logger(verbose: bool = False, log_file: str = None, logger_name: str = "pdchaoscli"):
    """
    Configure the proofdocks cli logger.
    """
    log_level = logging.INFO

    # we define colors ourselves as critical is missing in default ones
    colors = {
        logging.DEBUG: ForegroundColors.CYAN,
        logging.INFO: ForegroundColors.GREEN,
        logging.WARNING: ForegroundColors.YELLOW,
        logging.ERROR: ForegroundColors.RED,
        logging.CRITICAL: ForegroundColors.RED
    }
    fmt = "%(color)s[%(asctime)s %(levelname)s]%(end_color)s %(message)s"
    if verbose:
        log_level = logging.DEBUG
        fmt = "%(color)s[%(asctime)s %(levelname)s] "\
              "[%(module)s:%(lineno)d]%(end_color)s %(message)s"

    formatter = LogFormatter(
        fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S", colors=colors)

    # sadly, no other way to specify the name of the default logger publicly
    LOGZERO_DEFAULT_LOGGER = logger_name  # noqa: F841
    logger = setup_default_logger(level=log_level, formatter=formatter)

    if log_file:
        # always everything as strings in the log file
        logger.setLevel(logging.DEBUG)
        fmt = "%(color)s[%(asctime)s %(levelname)s] "\
              "[%(module)s:%(lineno)d]%(end_color)s %(message)s"
        formatter = LogFormatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S",
                                 colors=colors)
        logzero.logfile(log_file, formatter=formatter, mode='a',
                        loglevel=logging.DEBUG)
