"""Game core module - Main game controller."""

import pygame

from src.snake.core.logic import GameLogic
from src.snake.system.audio_manager import AudioManager
from src.snake.ui.visual_effects import VisualEffects

# Event for snake movement
MOVE_EVENT = pygame.USEREVENT + 1


class Game:
    """Core game controller."""

    def __init__(self, screen):
        """Initialize the game controller.

        Args:
            screen: Pygame surface for rendering
        """
        self.screen = screen
        self.logic = None
        self.effects = VisualEffects(screen)
        self.audio = AudioManager()

        # Set up movement timer
        pygame.time.set_timer(MOVE_EVENT, 150)  # Initial delay

    def update(self):
        """Update game state."""
        if not self.logic:
            return

        # Update effects
        self.effects.update()

        # Handle game over effects
        if self.logic.game_over:
            self.effects.show_game_over()
            if self.audio:
                self.audio.play_game_over()

    def handle_move(self):
        """Handle snake movement."""
        if not self.logic:
            return

        if not self.logic.game_over and not self.logic.paused:
            events = self.logic.handle_move()

            # Handle events
            if events.get("ate_food"):
                if self.audio:
                    self.audio.play_food()
                self.effects.show_food_effect(self.logic.snake.head())

            if events.get("picked_powerup"):
                if self.audio:
                    self.audio.play_powerup()
                self.effects.show_powerup_effect(self.logic.snake.head())

            if events.get("status") in ["wall", "self", "obstacle"]:
                if self.audio:
                    self.audio.play_game_over()
                self.effects.show_game_over()
