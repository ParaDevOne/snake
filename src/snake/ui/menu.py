"""
Módulo para el menú principal del juego Snake.
"""

import os
import sys

import pygame

from src.snake.system import settings
from src.snake.utils.config import config
from src.snake.utils.logger import log_debug, log_info

from .base_state import GameState

# Import OptionsMenu inside the method where it's needed to avoid circular imports
# from .options_menu import OptionsMenu
# from .game_play import GamePlayState

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


class MainMenu(GameState):
    """Estado del menú principal del juego."""

    def __init__(self, game):
        super().__init__(game)
        self.buttons = [
            {"text": "Jugar", "action": "play"},
            {"text": "Opciones", "action": "options"},
            {"text": "Salir", "action": "quit"},
        ]
        self.selected = 0
        font_path = config.get("FONT", "Data/assets/font.ttf")
        self.font = pygame.font.Font(font_path, 48)
        self.small_font = pygame.font.Font(font_path, 36)
        self.title_font = pygame.font.Font(font_path, 72)

        # Initialize audio
        self.audio = None
        if hasattr(game, "audio"):
            self.audio = game.audio
        elif hasattr(game, "current_state") and hasattr(game.current_state, "audio"):
            self.audio = game.current_state.audio

        # Always stop any currently playing music first to avoid overlap
        if hasattr(self, 'audio') and self.audio:
            try:
                self.audio.stop_music()
            except Exception as e:
                log_info(f"Error stopping previous music: {e}", context="MENU")

        # Play menu music if audio is enabled
        if self.audio and settings.MUSIC_ENABLED and hasattr(settings, 'AUDIO_CONFIG'):
            try:
                self.audio.play_music(
                    settings.AUDIO_CONFIG["music"]["music_menu"], 
                    loop=True
                )
                self.music_playing = True
            except Exception as e:
                log_info(f"Error playing menu music: {e}", context="MENU")

        log_info("Menú principal inicializado", context="MENU")

    def handle_events(self, event):
        """Maneja un evento de entrada.

        Args:
            event: El evento de Pygame a manejar.
        """
        if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
            needs_redraw = False
            if event.key == pygame.K_UP:  # pylint: disable=no-member
                self.selected = (self.selected - 1) % len(self.buttons)
                log_debug(
                    f"Botón seleccionado: {self.buttons[self.selected]['text']}",
                    context="MENU",
                )
                needs_redraw = True
            elif event.key == pygame.K_DOWN:  # pylint: disable=no-member
                self.selected = (self.selected + 1) % len(self.buttons)
                log_debug(
                    f"Botón seleccionado: {self.buttons[self.selected]['text']}",
                    context="MENU",
                )
                needs_redraw = True
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):  # pylint: disable=no-member
                self._handle_button_press()
                needs_redraw = True
            elif event.key == pygame.K_ESCAPE:  # pylint: disable=no-member
                self.running = False
                self.game.running = False

            if needs_redraw and hasattr(self, "draw"):
                self.draw()
                pygame.display.flip()

    def _handle_button_press(self):
        """Maneja la pulsación de un botón del menú."""
        action = self.buttons[self.selected]["action"]
        log_info(f"Botón presionado: {action}", context="MENU")

        try:
            if action == "play":
                # Import locally to avoid circular imports
                from .game_play import GamePlayState

                self.next_state = GamePlayState(self.game)
                log_info("Cambiando a estado: GamePlayState")
            elif action == "options":
                # Import locally to avoid circular imports
                from .options_menu import OptionsMenu

                self.next_state = OptionsMenu(self.game)
                log_info("Cambiando a estado: OptionsMenu")
            elif action == "quit":
                log_info("Saliendo del juego...", context="MENU")
                self.game.running = False
                return

            # Solo cambiar el estado si next_state se estableció correctamente
            if self.next_state is not None:
                self.running = False
            else:
                log_info(
                    f"Error: No se pudo cambiar al estado {action}", context="MENU"
                )

        except ImportError as e:
            log_info(f"Error al cambiar de estado: {str(e)}", context="MENU")
            import traceback

            log_info(traceback.format_exc(), context="MENU")

    def update(self, dt):
        # Actualizaciones del menú (si son necesarias)
        pass

    def cleanup(self):
        """Limpia los recursos del menú."""
        log_info("Limpiando recursos del menú principal", context="MENU")
        # Don't stop music here, let the next state handle it

    def draw(self):
        """Método de compatibilidad que llama a render."""
        self.render(self.screen)

    def render(self, screen):
        """Renderiza el menú en la pantalla."""
        # Fondo
        screen.fill(config.get("COLORS", "BACKGROUND", (0, 0, 0)))

        # Get window dimensions with fallbacks
        window_width = config.get("WINDOW", "WIDTH", 800)
        window_height = config.get("WINDOW", "HEIGHT", 600)

        # Ensure we have valid numbers
        window_width = 800 if window_width is None else int(window_width)
        window_height = 600 if window_height is None else int(window_height)

        # Título
        title = self.title_font.render("SNAKE GAME", True, (255, 255, 255))
        title_rect = title.get_rect(center=(window_width // 2, 100))
        screen.blit(title, title_rect)

        # Versión
        version = self.small_font.render("v1.8.0", True, (150, 150, 150))
        version_rect = version.get_rect(
            bottomright=(
                window_width - 20,
                window_height - 20,
            )
        )
        screen.blit(version, version_rect)

        # Botones
        for i, button in enumerate(self.buttons):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(button["text"], True, color)
            text_rect = text.get_rect(center=(window_width // 2, 300 + i * 70))
            screen.blit(text, text_rect)

            # Dibujar indicador de selección
            if i == self.selected:
                pygame.draw.rect(
                    screen,
                    (255, 255, 0),
                    (text_rect.left - 30, text_rect.centery - 15, 20, 30),
                    2,
                )
