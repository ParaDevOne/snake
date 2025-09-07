"""Food module - Handles food and power-up spawning."""

import random
from typing import List, Optional, Tuple


class Food:
    """Represents food items in the game."""

    def __init__(
        self,
        occupied_positions: List[Tuple[int, int]],
        obstacles: List[Tuple[int, int]],
        pos: Optional[Tuple[int, int]] = None,
    ):
        """Initialize a food item.

        Args:
            occupied_positions: List of positions that are occupied (snake body, etc.)
            obstacles: List of obstacle positions
            pos: Optional specific position for the food
        """
        self.pos = pos
        self.obstacles = obstacles
        if not pos:
            self.respawn(occupied_positions)

    def respawn(self, occupied_positions: List[Tuple[int, int]]):
        """Move food to a new random position.

        Args:
            occupied_positions: List of positions that are occupied
        """
        from src.snake.system.settings import COLUMNS, ROWS

        # Find all available positions
        available = []
        for x in range(COLUMNS):
            for y in range(ROWS):
                pos = (x, y)
                if pos not in occupied_positions and pos not in self.obstacles:
                    available.append(pos)

        if available:
            self.pos = random.choice(available)
        else:
            self.pos = None  # No available positions


class PowerUp(Food):
    """Represents a power-up item in the game."""

    def __init__(
        self,
        occupied_positions: List[Tuple[int, int]],
        obstacles: List[Tuple[int, int]],
        power_type: str,
    ):
        """Initialize a power-up.

        Args:
            occupied_positions: List of positions that are occupied
            obstacles: List of obstacle positions
            power_type: Type of power-up ('speed', 'grow', etc.)
        """
        super().__init__(occupied_positions, obstacles)
        self.type = power_type
