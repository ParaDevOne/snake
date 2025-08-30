"""
Sistema de logging para el juego Snake.
Proporciona funciones para registrar información, advertencias y errores.
"""
import logging
import os
import sys
from datetime import datetime

# Configuración básica del logger
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = logging.INFO

# Directorio de logs
LOG_DIR = os.path.join('Data', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Nombre del archivo de log con timestamp
LOG_FILE = os.path.join(LOG_DIR, f'snake_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

def setup_logger(name):
    """Configura y devuelve un logger con el nombre dado."""
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Evitar múltiples handlers
    if logger.handlers:
        return logger

    # Formato
    formatter = logging.Formatter(LOG_FORMAT)

    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para archivo
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

def _get_logger(name):
    return setup_logger(name)

def log_system_info(msg, *args, context='', **kwargs):
    """Registra información del sistema."""
    try:
        logger = _get_logger('system')
        if logger.isEnabledFor(logging.INFO):
            if context:
                logger.info('[%s] %s', context, msg, *args, **kwargs)
            else:
                logger.info(msg, *args, **kwargs)
    except Exception as e:
        print(f"Error en log_system_info: {e}", file=sys.stderr)

def log_debug(msg, *args, context='', **kwargs):
    """Registra un mensaje de depuración."""
    try:
        logger = _get_logger('debug')
        if logger.isEnabledFor(logging.DEBUG):
            if context:
                logger.debug('[%s] %s', context, msg, *args, **kwargs)
            else:
                logger.debug(msg, *args, **kwargs)
    except Exception as e:
        print(f"Error en log_debug: {e}", file=sys.stderr)

def log_info(msg, *args, context='', **kwargs):
    """Registra un mensaje informativo."""
    try:
        logger = _get_logger('info')
        if logger.isEnabledFor(logging.INFO):
            if context:
                logger.info('[%s] %s', context, msg, *args, **kwargs)
            else:
                logger.info(msg, *args, **kwargs)
    except Exception as e:
        print(f"Error en log_info: {e}", file=sys.stderr)

def log_warning(msg, *args, context='', **kwargs):
    """Registra una advertencia."""
    try:
        logger = _get_logger('warning')
        if logger.isEnabledFor(logging.WARNING):
            if context:
                logger.warning('[%s] %s', context, msg, *args, **kwargs)
            else:
                logger.warning(msg, *args, **kwargs)
    except Exception as e:
        print(f"Error en log_warning: {e}", file=sys.stderr)

def log_error(msg, *args, context='', **kwargs):
    """Registra un error."""
    try:
        logger = _get_logger('error')
        if logger.isEnabledFor(logging.ERROR):
            log_kwargs = {'exc_info': True, **kwargs}
            if context:
                logger.error('[%s] %s', context, msg, *args, **log_kwargs)
            else:
                logger.error(msg, *args, **log_kwargs)
    except Exception as e:
        print(f"Error en log_error: {e}", file=sys.stderr)
