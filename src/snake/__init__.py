"""
Paquete principal del juego Snake.

Este paquete contiene toda la lógica y los componentes necesarios para ejecutar el juego Snake.
"""

__version__ = "1.8.1"

from .core.game import Game
# Importaciones principales para facilitar el acceso a los componentes clave
from .main import run
from .ui.menu import MainMenu
from .ui.options_menu import OptionsMenu
from .utils.config import config
from .utils.logger import (log_debug, log_error, log_info, log_warning,
                           setup_logger)

__all__ = [
    'run',
    'Game',
    'MainMenu',
    'OptionsMenu',
    'config',
    'setup_logger',
    'log_info',
    'log_error',
    'log_warning',
    'log_debug'
]
