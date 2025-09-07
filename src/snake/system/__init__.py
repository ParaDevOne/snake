"""
System utilities and configuration for the Snake game.

This package handles:
- Game settings and configuration
- Audio management
- Profile management
- Score tracking and persistence
"""

from .settings import (
    WINDOW_SIZE, WIDTH, HEIGHT, GRID_SIZE, CELL_SIZE,
    FPS, SPEED, VSYNC, FONT, SETTINGS_FILE,
    POWERUP_ENABLED, POWERUP_TYPES, POWERUP_EFFECTS
)
from .audio_manager import AudioManager
from .profiles import Profiles
from .score import Score
from .utils import get_resource_path, load_json, save_json
from .video_config import VideoConfig

__all__ = [
    # Settings constants
    'WINDOW_SIZE', 'WIDTH', 'HEIGHT', 'GRID_SIZE', 'CELL_SIZE',
    'FPS', 'SPEED', 'VSYNC', 'FONT', 'SETTINGS_FILE',
    'POWERUP_ENABLED', 'POWERUP_TYPES', 'POWERUP_EFFECTS',
    # Classes
    'AudioManager',
    'Profiles',
    'Score',
    'VideoConfig',
    # Utility functions
    'get_resource_path',
    'load_json',
    'save_json'
]
