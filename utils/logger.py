import logging

from os import path, makedirs
from datetime import datetime


def get_logger(name):
    """
    Create and return logger object.
    """

    # Create logs folder path
    logs_folder = path.join(
        path.dirname(__file__),
        "..",
        "logs"
    )

    # Create logs folder if not present
    makedirs(logs_folder, exist_ok=True)

    # Create timestamp
    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    # Create log file name
    log_file = path.join(
        logs_folder,
        f"test_log_{timestamp}.log"
    )

    # Create logger
    logger = logging.getLogger(name)

    # Prevent duplicate logs
    if not logger.handlers:

        # Set logger level
        logger.setLevel(logging.DEBUG)

        # Create log format
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        # ===================================================== #
        # Console Handler
        # ===================================================== #

        # Print logs in terminal
        console_handler = logging.StreamHandler()

        # Show INFO and above in console
        console_handler.setLevel(logging.INFO)

        # Apply format
        console_handler.setFormatter(formatter)

        # ===================================================== #
        # File Handler
        # ===================================================== #

        # Save logs in file
        file_handler = logging.FileHandler(log_file)

        # Save DEBUG and above in file
        file_handler.setLevel(logging.DEBUG)

        # Apply format
        file_handler.setFormatter(formatter)

        # ===================================================== #
        # Add handlers to logger
        # ===================================================== #

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    # Return logger object
    return logger