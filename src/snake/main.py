"""
Punto de entrada principal del juego Snake.

Este módulo inicializa el juego y maneja el bucle principal.
"""

# Standard library imports
import os
import sys
import traceback

# Third-party imports
# pylint: disable=no-name-in-module, no-member
import pygame  # type: ignore
from pygame.locals import FULLSCREEN, QUIT, RESIZABLE  # type: ignore

# Local application imports
# Añadir el directorio src al path para importaciones absolutas
from src.snake.ui.menu import MainMenu
from src.snake.utils.config import config
from src.snake.utils.logger import log_error, log_info, setup_logger

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


class SnakeGame:
    """Clase principal del juego Snake."""

    def __init__(self):
        """Inicializa el juego."""
        self.running = True
        self.current_state = None
        self.screen = None
        self.clock = None
        self.audio = None
        
        # Initialize pygame and display
        self._init_pygame()
        self._init_display()
        
        # Initialize audio
        self._init_audio()
        
        # Start with main menu
        self.change_state(MainMenu(self))

    def _init_display(self):
        """Inicializa la pantalla del juego."""
        # Obtener configuración con valores por defecto
        width = int(config.get('WINDOW', 'WIDTH') or 800)
        height = int(config.get('WINDOW', 'HEIGHT') or 600)
        title = str(config.get('WINDOW', 'TITLE') or 'Snake Game')
        
        log_info(f"Inicializando pantalla: {width}x{height} - {title}", context="GAME")

        # Configurar flags de pantalla
        flags = RESIZABLE  # type: ignore
        if config.get('WINDOW', 'FULLSCREEN'):
            flags |= FULLSCREEN  # type: ignore

        # Inicializar pantalla
        self.screen = pygame.display.set_mode((width, height), flags)  # type: ignore
        pygame.display.set_caption(title)  # type: ignore
        log_info("Pantalla inicializada correctamente", context="GAME")

    def _init_audio(self):
        """Inicializa el sistema de audio."""
        try:
            from src.snake.system.audio_manager import AudioManager
            self.audio = AudioManager()
            log_info("Sistema de audio inicializado correctamente", context="GAME")
        except Exception as e:
            log_error(f"Error al inicializar el sistema de audio: {e}", context="GAME")
            self.audio = None

    def _setup_screen(self):
        """Configura la pantalla del juego. Método mantenido por compatibilidad."""
        # Este método parece ser redundante con _init_display
        # Se mantiene por compatibilidad pero delega en _init_display
        self._init_display()

    def change_state(self, new_state):
        """Cambia el estado actual del juego."""
        if self.current_state is not None:
            self.current_state.cleanup()

        # Check if new_state is a class (needs instantiation) or an instance
        if isinstance(new_state, type):
            self.current_state = new_state(self)
            log_info(f"Cambiando a estado: {new_state.__name__}")
        else:
            # It's already an instance
            self.current_state = new_state
            log_info(f"Cambiando a estado: {type(new_state).__name__}")

    def run(self):
        """Bucle principal del juego."""
        log_info("Iniciando bucle principal del juego", context="GAME")
        try:
            while self.running and self.current_state is not None:
                # Handle events
                for event in pygame.event.get():  # type: ignore
                    if event.type == QUIT:  # type: ignore
                        self.running = False
                    elif hasattr(self.current_state, 'handle_events'):
                        self.current_state.handle_events(event)

                # Update game logic
                if self.clock:
                    dt = self.clock.tick(60) / 1000.0  # Delta time in seconds
                    if hasattr(self.current_state, 'update'):
                        self.current_state.update(dt)

                    # Render
                    if hasattr(self.current_state, 'draw'):
                        self.current_state.draw()
                        pygame.display.flip()  # type: ignore
                
                # Handle state transitions
                if hasattr(self.current_state, 'running') and not self.current_state.running:
                    if hasattr(self.current_state, 'next_state') and self.current_state.next_state is not None:
                        next_state = self.current_state.next_state
                        self.current_state.cleanup()
                        self.current_state = next_state
                    else:
                        self.running = False

        except Exception as e:
            log_error(f"Error en el bucle principal: {e}")
            log_error(traceback.format_exc())
            raise
        finally:
            self.cleanup()

    def cleanup(self):
        """Limpia los recursos del juego."""
        if self.current_state is not None:
            self.current_state.cleanup()
        if pygame.get_init():  # type: ignore
            pygame.quit()  # type: ignore

    def _init_pygame(self):
        """Inicializa los módulos de Pygame."""
        pygame.init()  # type: ignore
        pygame.mixer.init()  # type: ignore
        self.clock = pygame.time.Clock()  # type: ignore

def run():
    """Función principal para iniciar el juego."""
    # Configurar logging
    logger = setup_logger('snake')
    logger.info("Iniciando Snake Game")
    logger.info("Python version: %s", sys.version)

    try:
        # Crear e iniciar el juego
        game = SnakeGame()
        game.run()
    except Exception as e:
        logger.error("Error al iniciar el juego: %s", str(e))
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    run()
