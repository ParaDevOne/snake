"""
Utility functions and helpers for the Snake game.

This package provides:
- Logging functionality
- Configuration management
- File and resource utilities
"""

from .logger import Logger, setup_logger, log_info, log_error, log_warning, log_debug
from .config import Config, load_config, save_config

__all__ = [
    'Logger',
    'setup_logger',
    'log_info',
    'log_error',
    'log_warning',
    'log_debug',
    'Config',
    'load_config',
    'save_config'
]
