"""
Módulo para el estado de juego principal.
"""

import pygame

from ..core.game import Game as GameCore
from ..core.logic import GameLogic
from ..system import settings
from ..utils.logger import log_info
from .base_state import GameState

# Import MOVE_EVENT from game module
from ..core.game import MOVE_EVENT

# Initialize pygame display if not already done
if not pygame.display.get_init():
    pygame.display.init()


class GamePlayState(GameState):
    """Estado del juego principal."""

    def __init__(self, game):
        """Inicializa el estado de juego."""
        super().__init__(game)

        # Ensure screen is properly initialized
        if not hasattr(self, "screen") or self.screen is None:
            self.screen = pygame.display.set_mode(
                (settings.WIDTH, settings.HEIGHT), pygame.RESIZABLE
            )

        # Initialize game logic
        self.logic = GameLogic(load_highscore=True)

        # Initialize game core with the screen
        self.game_core = GameCore(self.screen)

        # Link the logic to the game core
        if hasattr(self.game_core, "logic"):
            self.game_core.logic = self.logic
            
        # Initialize audio
        if hasattr(self.game_core, 'audio') and not self.game_core.music_playing:
            if settings.MUSIC_ENABLED and hasattr(settings, 'AUDIO_CONFIG'):
                try:
                    self.game_core.audio.play_music(
                        settings.AUDIO_CONFIG['music']['music_game'], 
                        loop=True
                    )
                    self.game_core.music_playing = True
                except Exception as e:
                    log_info(f"Error playing music: {e}", context="GAME")

        log_info("Estado de juego principal inicializado", context="GAME")

    def handle_events(self, event):
        """Maneja los eventos de entrada."""
        # Handle MOVE_EVENT for snake movement
        if event.type == MOVE_EVENT and hasattr(self, 'game_core'):
            try:
                self.game_core.handle_move()
            except Exception as e:
                log_info(f"Error handling move: {e}", context="GAME")
        
        # Check if game is over and handle input
        game_over = hasattr(self, 'game_core') and hasattr(self.game_core, 'logic') and self.game_core.logic.game_over
                
        # Handle keyboard input
        if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
            if game_over:
                if event.key == pygame.K_r:  # R key restarts the game
                    self.next_state = GamePlayState(self.game)
                else:  # Any other key returns to main menu
                    from .menu import MainMenu
                    self.next_state = MainMenu(self.game)
                    # Stop game music before going to menu
                    if hasattr(self, 'game_core') and hasattr(self.game_core, 'audio'):
                        self.game_core.audio.stop_music()
                self.running = False
            elif event.key == pygame.K_ESCAPE:  # pylint: disable=no-member
                from .menu import MainMenu
                # Stop game music before going to menu
                if hasattr(self, 'game_core') and hasattr(self.game_core, 'audio'):
                    self.game_core.audio.stop_music()
                self.next_state = MainMenu(self.game)
                self.running = False
            elif event.key == pygame.K_p:  # pylint: disable=no-member
                self.game_core.logic.toggle_pause()
            elif event.key == pygame.K_UP:  # pylint: disable=no-member
                self._change_direction((0, -1))
            elif event.key == pygame.K_DOWN:  # pylint: disable=no-member
                self._change_direction((0, 1))
            elif event.key == pygame.K_LEFT:  # pylint: disable=no-member
                self._change_direction((-1, 0))
            elif event.key == pygame.K_RIGHT:  # pylint: disable=no-member
                self._change_direction((1, 0))

    def _change_direction(self, direction):
        """Helper method to safely change snake direction.

        Args:
            direction: Tuple representing the new direction (dx, dy)
        """
        try:
            if (
                hasattr(self.game_core, "logic")
                and hasattr(self.game_core.logic, "snake")
                and self.game_core.logic.snake
            ):
                # Get current direction safely
                current_direction = getattr(
                    self.game_core.logic.snake, "direction", (1, 0)
                )
                # Prevent 180-degree turns
                if (current_direction[0] * -1, current_direction[1] * -1) != direction:
                    setattr(self.game_core.logic.snake, "direction", direction)
        except Exception as e:
            log_info(f"Error changing direction: {e}", context="GAME")

    def update(self, dt):
        """Actualiza la lógica del juego."""
        try:
            # Ensure game core and logic are properly initialized
            if not hasattr(self, "game_core") or not hasattr(self.game_core, "logic"):
                self.game_core = GameCore(self.screen)
                if not hasattr(self, "logic"):
                    self.logic = GameLogic(load_highscore=True)
                self.game_core.logic = self.logic

            # Update game logic
            self.game_core.update()

            # Check if game is over - the core game will handle the visual effects
            # and we'll just wait for the player to press a key to return to menu
            if (
                hasattr(self.game_core, "logic") 
                and hasattr(self.game_core.logic, "game_over")
                and self.game_core.logic.game_over
            ):
                # The core game will show game over effects
                # We'll handle the key press to return to menu in handle_events
                pass

        except Exception as e:
            log_info(f"Error in update: {e}", context="GAME")
            # If there's an error, go back to main menu
            from .menu import MainMenu

            self.next_state = MainMenu(self.game)
            self.running = False

    def draw(self):
        """Dibuja el juego en la pantalla."""
        try:
            # Fill with black background
            self.screen.fill((0, 0, 0))

            # Make sure game_core is initialized before rendering
            if hasattr(self, "game_core") and self.game_core is not None:
                self.game_core.render()
            else:
                # If game_core is not available, show a message
                font = pygame.font.Font(None, 36)
                text = font.render("Inicializando juego...", True, (255, 255, 255))
                text_rect = text.get_rect(
                    center=(settings.WIDTH // 2, settings.HEIGHT // 2)
                )
                self.screen.blit(text, text_rect)
        except Exception as e:
            log_info(f"Error in draw: {e}", context="GAME")

    def cleanup(self):
        """Limpia los recursos del estado de juego."""
        # Don't stop music here, let the next state handle it
        log_info("Limpiando recursos del juego principal", context="GAME")
        # Stop any playing music
        if hasattr(self, 'game_core') and hasattr(self.game_core, 'audio'):
            try:
                self.game_core.audio.stop_music()
            except Exception as e:
                log_info(f"Error stopping music: {e}", context="GAME")
