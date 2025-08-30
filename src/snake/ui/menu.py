"""
Módulo para el menú principal del juego Snake.
"""
import pygame
import os
import sys

# Añadir el directorio src al path para importaciones absolutas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ..ui.base_state import GameState
from src.snake.utils.config import config
from src.snake.utils.logger import log_info, log_debug

class MainMenu(GameState):
    """Estado del menú principal del juego."""
    
    def __init__(self, game):
        super().__init__(game)
        self.buttons = [
            {"text": "Jugar", "action": "play"},
            {"text": "Opciones", "action": "options"},
            {"text": "Salir", "action": "quit"}
        ]
        self.selected = 0
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        log_info("Menú principal inicializado", "MENU")
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.buttons)
                    log_debug(f"Botón seleccionado: {self.buttons[self.selected]['text']}", "MENU")
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.buttons)
                    log_debug(f"Botón seleccionado: {self.buttons[self.selected]['text']}", "MENU")
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self._handle_button_press()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.game.running = False
    
    def _handle_button_press(self):
        """Maneja la pulsación de un botón del menú."""
        action = self.buttons[self.selected]["action"]
        log_info(f"Botón presionado: {action}", "MENU")
        
        if action == "play":
            from ..core.game import GameState as GamePlayState
            self.change_state(GamePlayState)
        elif action == "options":
            from .options_menu import OptionsMenu
            self.change_state(OptionsMenu)
        elif action == "quit":
            self.running = False
            self.game.running = False
    
    def update(self, dt):
        # Actualizaciones del menú (si son necesarias)
        pass
    
    def draw(self):
        # Fondo
        self.screen.fill(config.get("COLORS", "BACKGROUND", (0, 0, 0)))
        
        # Título
        title = self.title_font.render("SNAKE GAME", True, (255, 255, 255))
        title_rect = title.get_rect(center=(config.get("WINDOW", "WIDTH", 800) // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Versión
        version = self.small_font.render("v1.8.0", True, (150, 150, 150))
        version_rect = version.get_rect(bottomright=(config.get("WINDOW", "WIDTH", 800) - 20, 
                                                   config.get("WINDOW", "HEIGHT", 600) - 20))
        self.screen.blit(version, version_rect)
        
        # Botones
        for i, button in enumerate(self.buttons):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(button["text"], True, color)
            text_rect = text.get_rect(center=(config.get("WINDOW", "WIDTH", 800) // 2, 
                                           300 + i * 70))
            self.screen.blit(text, text_rect)
            
            # Dibujar indicador de selección
            if i == self.selected:
                pygame.draw.rect(self.screen, (255, 255, 0), 
                               (text_rect.left - 30, text_rect.centery - 15, 20, 30), 2)
