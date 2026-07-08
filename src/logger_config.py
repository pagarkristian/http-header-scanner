"""
Application logging setup.

Errors and key events are written to a log file so past runs can be
reviewed later, without cluttering the CLI output that Rich renders.
This is separate from the CLI's success/error panels: the panels are
for the user watching the screen right now, the log file is a
permanent record for debugging afterwards.
"""

import logging
from pathlib import Path


LOGGER_NAME = "http_header_scanner"


def setup_logger(logs_dir="logs", log_level="INFO"):
    """
    Configure and return the application's shared logger.

    Args:
        logs_dir (str): Directory where the log file is written.
        log_level (str): Logging level name (e.g. "INFO", "DEBUG").

    Returns:
        logging.Logger: Configured logger instance.
    """

    logger = logging.getLogger(LOGGER_NAME)

    # A batch scan calls this once per target. Without this guard, every
    # call would attach another file handler, and every log line would
    # be written to the file multiple times.
    if logger.handlers:
        return logger

    logger.setLevel(log_level)

    log_path = Path(logs_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(log_path / "scanner.log", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def get_logger():
    """
    Get the application's shared logger. Assumes setup_logger() has
    already been called once at startup.

    Returns:
        logging.Logger: The application logger.
    """

    return logging.getLogger(LOGGER_NAME)
