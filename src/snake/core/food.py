"""A module for the food and power-up items in the game."""
# food.py

import random
from src.snake.system import utils

class Food:

    """Food class for the game, which can respawn at random positions."""

    def __init__(self, occupied, obstacles=None):
        self.obstacles = obstacles or []
        self.pos = None
        self.respawn(occupied)

    def respawn(self, occupied):
        """Respawn the food at a random free cell."""
        pos = utils.random_free_cell(occupied, extra_forbidden=self.obstacles)
        self.pos = pos
        return pos

class PowerUp:

    """PowerUp class for the game, which can have different types."""

    TYPES = ("slow",
            "speed",
            "grow",
            "score")  # slow = reduce speed (slower), speed = faster, grow = +growth, score = bonus
    def __init__(self, occupied, obstacles=None):
        self.obstacles = obstacles or []
        self.type = random.choice(self.TYPES)
        self.pos = utils.random_free_cell(occupied, extra_forbidden=self.obstacles)
