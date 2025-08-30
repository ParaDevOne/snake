"""
Punto de entrada principal del juego Snake.

Este módulo inicializa el juego y maneja el bucle principal.
"""

import os
import sys
import traceback
import pygame

# Añadir el directorio src al path para importaciones absolutas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.snake.ui.menu import MainMenu
from src.snake.utils.config import config
from src.snake.utils.logger import setup_logger, log_info, log_error

class SnakeGame:
    """Clase principal del juego Snake."""
    
    def __init__(self):
        """Inicializa el juego."""
        self.running = True
        self.screen = None
        self.clock = None
        self.current_state = None
        
        # Inicializar pygame
        pygame.init()
        pygame.mixer.init()
        
        # Configurar la pantalla
        self._setup_screen()
        
        # Configurar el reloj
        self.clock = pygame.time.Clock()
        
        # Establecer el estado inicial
        self.change_state(MainMenu)
    
    def _setup_screen(self):
        """Configura la ventana del juego."""
        width = config.get("WINDOW", "WIDTH", 800)
        height = config.get("WINDOW", "HEIGHT", 600)
        fullscreen = config.get("WINDOW", "FULLSCREEN", False)
        
        flags = pygame.RESIZABLE
        if fullscreen:
            flags |= pygame.FULLSCREEN
            
        self.screen = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption(config.get("WINDOW", "TITLE", "Snake Game"))
    
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
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
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
        pygame.quit()

def run():
    """Función principal para iniciar el juego."""
    # Configurar logging
    setup_logger()
    log_info("Iniciando Snake Game")
    log_info(f"Python version: {sys.version}")
    
    try:
        # Crear e iniciar el juego
        game = SnakeGame()
        game.run()
    except Exception as e:
        log_error(f"Error al iniciar el juego: {e}")
        log_error(traceback.format_exc())
        raise

if __name__ == "__main__":
    run()
