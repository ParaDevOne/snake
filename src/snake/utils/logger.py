"""
Logging system for the Snake game.
Provides centralized logging functionality with different levels and contexts.
"""

import logging
import os
import sys
from datetime import datetime
from typing import Optional

from src.snake.system.settings import LOG_LEVEL

# Singleton instance
_logger_instance: Optional[logging.Logger] = None


# Custom formatting
class SnakeFormatter(logging.Formatter):
    """Custom formatter for the Snake game logger."""

    def format(self, record):
        """Format the log record with timestamp and context."""
        # Add context if available
        context = getattr(record, "context", "GAME")
        record.context = f"[{context}]"

        # Add timestamp
        record.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        return super().format(record)


def setup_logger(name: str = "snake", level: Optional[str] = None) -> logging.Logger:
    """Set up and configure the logger.

    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR)

    Returns:
        Configured logger instance
    """
    global _logger_instance

    if _logger_instance:
        return _logger_instance

    # Create logger
    logger = logging.getLogger(name)
    level = level or LOG_LEVEL
    logger.setLevel(getattr(logging, level.upper()))

    # Create formatters and handlers
    console_format = "%(timestamp)s %(context)s %(levelname)s: %(message)s"
    file_format = "%(timestamp)s %(context)s %(levelname)s: %(message)s"

    formatter = SnakeFormatter(console_format)
    file_formatter = SnakeFormatter(file_format)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    try:
        log_dir = os.path.join("Data", "logs")
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(
            log_dir, f"snake_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Could not set up file logging: {e}")

    _logger_instance = logger
    return logger


def get_logger() -> logging.Logger:
    """Get the configured logger instance.

    Returns:
        Logger instance
    """
    global _logger_instance
    if not _logger_instance:
        _logger_instance = setup_logger()
    return _logger_instance


# Convenience functions
def log_info(message: str, context: str = "GAME"):
    """Log an info message.

    Args:
        message: Message to log
        context: Logging context
    """
    logger = get_logger()
    logger.info(message, extra={"context": context})


def log_error(message: str, context: str = "GAME"):
    """Log an error message.

    Args:
        message: Message to log
        context: Logging context
    """
    logger = get_logger()
    logger.error(message, extra={"context": context})


def log_warning(message: str, context: str = "GAME"):
    """Log a warning message.

    Args:
        message: Message to log
        context: Logging context
    """
    logger = get_logger()
    logger.warning(message, extra={"context": context})


def log_debug(message: str, context: str = "GAME"):
    """Log a debug message.

    Args:
        message: Message to log
        context: Logging context
    """
    logger = get_logger()
    logger.debug(message, extra={"context": context})


def log_game_event(event: str, details: Optional[str] = None, context: str = "GAME"):
    """Log a game event with optional details.

    Args:
        event: Event description
        details: Additional event details
        context: Logging context
    """
    message = event
    if details:
        message = f"{event} - {details}"
    log_info(message, context)
