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

def log_system_info(message):
    """Registra información del sistema."""
    logger = setup_logger('system')
    logger.info(f"[SYSTEM] {message}")

def log_debug(message, context=''):
    """Registra un mensaje de depuración."""
    logger = setup_logger('debug')
    if context:
        logger.debug(f"[{context}] {message}")
    else:
        logger.debug(message)

def log_info(message, context=''):
    """Registra un mensaje informativo."""
    logger = setup_logger('info')
    if context:
        logger.info(f"[{context}] {message}")
    else:
        logger.info(message)

def log_warning(message, context=''):
    """Registra una advertencia."""
    logger = setup_logger('warning')
    if context:
        logger.warning(f"[{context}] {message}")
    else:
        logger.warning(message)

def log_error(message, context=''):
    """Registra un error."""
    logger = setup_logger('error')
    if context:
        logger.error(f"[{context}] {message}", exc_info=True)
    else:
        logger.error(message, exc_info=True)
