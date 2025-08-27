"""
obstacles.py
Lógica modular para obstáculos en Snake Game.
"""
import random

import pygame

from src.snake.system.settings import COLUMNS, GRID_SIZE, OBSTACLE_COLOR, OBSTACLE_COUNT, ROWS


class ObstacleManager:
    """Maneja la generación y colisión de obstáculos en el juego."""
    def __init__(self, grid_size=GRID_SIZE, grid_width=COLUMNS, grid_height=ROWS, count=OBSTACLE_COUNT):
        self.grid_size = grid_size
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.count = count
        self.obstacles = []

    def generate_obstacles(self, snake_positions, food_position):
        """Genera obstáculos en posiciones aleatorias, evitando la posición de la serpiente y la comida."""
        self.obstacles = []
        attempts = 0
        while len(self.obstacles) < self.count and attempts < self.count * 10:
            pos = (
                random.randint(0, self.grid_width - 1),
                random.randint(0, self.grid_height - 1)
            )
            if (
                pos not in self.obstacles and
                pos not in snake_positions and
                pos != food_position
            ):
                self.obstacles.append(pos)
            attempts += 1

    def draw(self, surface):
        """Dibuja los obstáculos en la superficie del juego."""
        for pos in self.obstacles:
            rect = pygame.Rect(pos[0] * self.grid_size, pos[1] * self.grid_size, self.grid_size, self.grid_size)
            pygame.draw.rect(surface, OBSTACLE_COLOR, rect)

    def collides(self, position):
        """Verifica si la posición colisiona con algún obstáculo."""
        return position in self.obstacles

    def get_obstacles(self):
        """Devuelve una lista de todas las posiciones de los obstáculos."""
        return list(self.obstacles)
