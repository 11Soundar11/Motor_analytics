"""
Logger module for Motor Insurance Claims & Policy Analytics Pipeline.

Provides centralized logging configuration and utility functions to record
pipeline execution milestones, data validation, cleaning operations, and errors.
"""

import os
import logging

_LOGGER = None


def setup_logger(log_file: str = "logs/pipeline.log", level: int = logging.INFO) -> logging.Logger:
    """
    Sets up and configures the centralized pipeline logger.

    Args:
        log_file: Relative or absolute file path to the log file.
        level: Logging level (e.g. logging.INFO, logging.DEBUG).

    Returns:
        logging.Logger instance configured with file and console handlers.
    """
    global _LOGGER
    if _LOGGER is not None:
        return _LOGGER

    # Ensure log directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("motor_insurance_analytics")
    logger.setLevel(level)

    if not logger.handlers:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    _LOGGER = logger
    return _LOGGER


def get_logger() -> logging.Logger:
    """Returns the existing logger or initializes a default one."""
    global _LOGGER
    if _LOGGER is None:
        return setup_logger()
    return _LOGGER


def log_pipeline_step(message: str) -> None:
    """
    Logs an informational milestone or step in the data pipeline.

    Args:
        message: The message describing the pipeline step.
    """
    logger = get_logger()
    logger.info(message)


def log_error(message: str) -> None:
    """
    Logs an error event in the data pipeline.

    Args:
        message: The error message or exception details.
    """
    logger = get_logger()
    logger.error(message)
