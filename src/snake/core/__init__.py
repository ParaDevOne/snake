"""
Core components for the Snake game.

This package contains the fundamental game mechanics and logic components:
- Game: Main game controller
- Snake: Snake movement and collision logic
- Food: Food spawning and collection
- Obstacles: Obstacle generation and management
"""

from .game import Game
from .snake import Snake
from .food import Food
from .obstacles import Obstacles
from .logic import calculate_next_position, check_collision

__all__ = [
    'Game',
    'Snake',
    'Food',
    'Obstacles',
    'calculate_next_position',
    'check_collision'
]
