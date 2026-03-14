"""
Logging configuration module.

Sets up application-wide logging to both file and console.
Log file is stored in the 'logs/' directory, which is created
automatically if it does not exist.
"""

import logging
import os


LOG_DIR: str = "logs"
LOG_FILE: str = os.path.join(LOG_DIR, "trading_bot.log")

_logger_initialized: bool = False


def setup_logging() -> logging.Logger:
    """Configure and return the application logger.

    Creates the 'logs/' directory if it does not exist.
    Sets up both a file handler and a console handler with
    a unified format including timestamp, level, and message.

    Returns:
        logging.Logger: Configured logger instance for the trading bot.
    """
    global _logger_initialized

    logger = logging.getLogger("trading_bot")

    if _logger_initialized:
        return logger

    logger.setLevel(logging.DEBUG)

    # Create logs directory if it does not exist
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Log format: timestamp - level - message
    log_format = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler — logs everything to file
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)

    # Console handler — logs INFO and above to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    _logger_initialized = True

    return logger
