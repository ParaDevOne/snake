"""A module for utility functions."""
# utils.py

import json
import os
import random
import sys
from src.snake.system import settings
from src.snake.utils.logger import (
    log_info,
    log_error,
    log_warning,
    log_debug,
    log_game_event,
)

# Configurar encoding UTF-8 para Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore
    except (ImportError, AttributeError):
        pass  # Si falla, continuar sin UTF-8


def random_free_cell(occupied, extra_forbidden=None):
    """Devuelve una celda libre aleatoria que no esté ocupada."""
    occupied_set = set(occupied)
    extra = set(extra_forbidden or [])
    free = [
        (x, y)
        for x in range(settings.COLUMNS)
        for y in range(settings.ROWS)
        if (x, y) not in occupied_set and (x, y) not in extra
    ]
    return random.choice(free) if free else None


def load_json(path, default):
    """Carga un archivo JSON y devuelve su contenido o un valor por defecto."""
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except (OSError, json.JSONDecodeError, UnicodeDecodeError) as e:
        log_error(f"Error cargando archivo JSON: {e}")
    return default


def save_json(path, obj):
    """Guarda un objeto en un archivo JSON."""
    try:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f)
    except (OSError, TypeError, ValueError, UnicodeEncodeError) as e:
        log_error(f"No se pudo salvar: {e}")


def save_settings():
    """Guarda la configuración actual del juego."""
    try:
        config = {
            "COLUMNS": settings.COLUMNS,
            "ROWS": settings.ROWS,
            "CELL_SIZE": settings.CELL_SIZE,
            "SPEED": settings.SPEED,
            "SOUND_VOLUME": settings.SOUND_VOLUME,
            "MUSIC_VOLUME": settings.MUSIC_VOLUME,
            "FULLSCREEN": settings.FULLSCREEN,
            "VSYNC": settings.VSYNC,
            "SHOW_FPS": settings.SHOW_FPS,
            "SHOW_GRID": settings.SHOW_GRID,
            "OBSTACLES_ENABLED": getattr(settings, "OBSTACLES_ENABLED", False),
            "DIFFICULTY": getattr(settings, "DIFFICULTY", "normal"),
        }
        save_json(settings.SETTINGS_FILE, config)
        log_info("Configuración guardada correctamente")
    except ImportError as e:
        log_error(f"Error guardando configuración: {e}")
