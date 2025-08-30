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
    """Registra información del sistema.
    
    Args:
        msg: El mensaje a registrar
        *args: Argumentos para formatear en el mensaje
        context: Contexto opcional para el mensaje
        **kwargs: Argumentos adicionales para el logger
    """
    try:
        logger = _get_logger('system')
        if logger.isEnabledFor(logging.INFO):
            if context:
                # Si hay contexto, lo añadimos al mensaje
                formatted_msg = f'[{context}] {msg}'
                logger.info(formatted_msg, *args, **kwargs)
            else:
                logger.info(msg, *args, **kwargs)
    except Exception as e:
        print(f"Error on log_system_info: {e}", file=sys.stderr)

def log_debug(msg, *args, context='', **kwargs):
    """Registra un mensaje de depuración.
    
    Args:
        msg: El mensaje a registrar
        *args: Argumentos para formatear en el mensaje
        context: Contexto opcional para el mensaje
        **kwargs: Argumentos adicionales para el logger
    """
    try:
        logger = _get_logger('debug')
        if logger.isEnabledFor(logging.DEBUG):
            if context:
                # Si hay contexto, lo añadimos al mensaje
                formatted_msg = f'[{context}] {msg}'
                logger.debug(formatted_msg, *args, **kwargs)
            else:
                logger.debug(msg, *args, **kwargs)
    except Exception as e:
        print(f"Error on log_debug: {e}", file=sys.stderr)

def log_info(msg, *args, context='', **kwargs):
    """Registra un mensaje informativo.
    
    Args:
        msg: El mensaje a registrar
        *args: Argumentos para formatear en el mensaje
        context: Contexto opcional para el mensaje
        **kwargs: Argumentos adicionales para el logger
    """
    try:
        logger = _get_logger('info')
        if logger.isEnabledFor(logging.INFO):
            if context:
                # Si hay contexto, lo añadimos al mensaje
                formatted_msg = f'[{context}] {msg}'
                logger.info(formatted_msg, *args, **kwargs)
            else:
                logger.info(msg, *args, **kwargs)
    except Exception as e:
        print(f"Error on log_info: {e}", file=sys.stderr)

def log_warning(msg, *args, context='', **kwargs):
    """Registra una advertencia.
    
    Args:
        msg: El mensaje a registrar
        *args: Argumentos para formatear en el mensaje
        context: Contexto opcional para el mensaje
        **kwargs: Argumentos adicionales para el logger
    """
    try:
        logger = _get_logger('warning')
        if logger.isEnabledFor(logging.WARNING):
            if context:
                # Si hay contexto, lo añadimos al mensaje
                formatted_msg = f'[{context}] {msg}'
                logger.warning(formatted_msg, *args, **kwargs)
            else:
                logger.warning(msg, *args, **kwargs)
    except Exception as e:
        print(f"Error on log_warning: {e}", file=sys.stderr)

def log_error(msg, *args, context='', **kwargs):
    """Registra un error.
    
    Args:
        msg: El mensaje de error a registrar
        *args: Argumentos para formatear en el mensaje
        context: Contexto opcional para el mensaje
        **kwargs: Argumentos adicionales para el logger
    """
    try:
        logger = _get_logger('error')
        if logger.isEnabledFor(logging.ERROR):
            # Asegurarse de que no sobrescribimos exc_info si ya está en kwargs
            log_kwargs = {'exc_info': True, **kwargs}
            if context:
                # Si hay contexto, lo añadimos al mensaje
                formatted_msg = f'[{context}] {msg}'
                logger.error(formatted_msg, *args, **log_kwargs)
            else:
                logger.error(msg, *args, **log_kwargs)
    except Exception as e:
        print(f"Error on log_error: {e}", file=sys.stderr)
