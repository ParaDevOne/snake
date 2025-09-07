"""
User Interface components for the Snake game.

This package contains all UI-related components:
- Visual effects and animations
- Menu system
- Game UI components
- Score display
"""

from .base_state import BaseState
from .visual_effects import VisualEffects, ParticleSystem, AnimationManager
from .menu import Menu, MainMenu
from .options_menu import OptionsMenu
from .game_play import GamePlay
from .components import Button, Label, Panel

__all__ = [
    # Base classes
    'BaseState',
    # Visual effects
    'VisualEffects',
    'ParticleSystem',
    'AnimationManager',
    # Menu system
    'Menu',
    'MainMenu',
    'OptionsMenu',
    # Game UI
    'GamePlay',
    # UI Components
    'Button',
    'Label',
    'Panel'
]
