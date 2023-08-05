"""For debugging the library.

To enable debugging you must set the environment variable ``NARRATION_DEBUG=1``
or via calling ``narration.log_to_stderr()`` at the beginning of your code.
"""
import logging
import os
import sys

from narration.constants import NARRATION_DEBUG_LOG_PREFIX

_logging_configured = False

NARRATION_DEBUG = os.environ.get("NARRATION_DEBUG", "0") == "1"


def get_debug_logger(logger_name):
    """Returns the logger to debug narration."""
    assert logger_name.startswith(NARRATION_DEBUG_LOG_PREFIX)
    _configure_debug_logging_if_not_initialized()
    return logging.getLogger(logger_name)


def log_to_stderr(level=logging.DEBUG):
    global NARRATION_DEBUG, _logging_configured
    NARRATION_DEBUG = True

    _logging_configured = False
    _configure_debug_logging_if_not_initialized(level=level)


def _configure_debug_logging_if_not_initialized(level=logging.DEBUG):
    """Do a pre configuration here at a very early stage even before
    logging.basicConfig or logging.fileConfig is called.
    """
    global _logging_configured

    if _logging_configured:
        return

    logger = logging.getLogger(NARRATION_DEBUG_LOG_PREFIX)

    if not NARRATION_DEBUG:
        logger.disabled = True
        logger.setLevel(logging.CRITICAL)
    else:
        logger.info("narration debug logging activated")
        if not logger.handlers and logger.propagate:
            formatter = logging.Formatter("[%(name)s:%(process)d] %(message)s")
            handler = logging.StreamHandler(sys.stderr)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.propagate = 0
            logger.setLevel(level)

    _logging_configured = True
