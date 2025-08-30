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
from pygame.locals import (  # type: ignore
    RESIZABLE,
    FULLSCREEN,
    QUIT,
)

# Local application imports
# Añadir el directorio src al path para importaciones absolutas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.snake.ui.menu import MainMenu  # noqa: E402
from src.snake.utils.config import config  # noqa: E402
from src.snake.utils.logger import setup_logger, log_info, log_error  # noqa: E402

class SnakeGame:
    """Clase principal del juego Snake."""

    def __init__(self):
        """Inicializa el juego."""
        self.running = True
        self.current_state = None
        self.screen = None
        self.clock = None
        self._init_pygame()
        self._init_display()
        self.change_state(MainMenu(self))

    def _init_display(self):
        """Inicializa la pantalla del juego."""
        # Obtener configuración con valores por defecto
        width = int(config.get('WINDOW', 'WIDTH') or 800)
        height = int(config.get('WINDOW', 'HEIGHT') or 600)
        title = str(config.get('WINDOW', 'TITLE') or 'Snake Game')

        # Configurar flags de pantalla
        flags = RESIZABLE  # type: ignore
        if config.get('WINDOW', 'FULLSCREEN'):
            flags |= FULLSCREEN  # type: ignore

        # Inicializar pantalla
        self.screen = pygame.display.set_mode((width, height), flags)  # type: ignore
        pygame.display.set_caption(title)  # type: ignore

    def _setup_screen(self):
        """Configura la pantalla del juego. Método mantenido por compatibilidad."""
        # Este método parece ser redundante con _init_display
        # Se mantiene por compatibilidad pero delega en _init_display
        self._init_display()

    def change_state(self, new_state):
        """Cambia el estado actual del juego."""
        if self.current_state is not None:
            self.current_state.cleanup()

        self.current_state = new_state(self)
        log_info(f"Cambiando a estado: {new_state.__name__}")

    def run(self):
        """Bucle principal del juego."""
        try:
            while self.running and self.current_state is not None:
                # Manejar eventos
                for event in pygame.event.get():  # type: ignore
                    if event.type == QUIT:  # type: ignore
                        self.running = False
                    if hasattr(self.current_state, 'handle_event'):
                        self.current_state.handle_event(event)

                # Actualizar lógica
                if self.clock:
                    dt = self.clock.tick(60) / 1000.0  # Delta time en segundos
                    if hasattr(self.current_state, 'update'):
                        self.current_state.update(dt)

                    # Renderizar
                    if hasattr(self.current_state, 'render'):
                        self.current_state.render(self.screen)
                        pygame.display.flip()

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
