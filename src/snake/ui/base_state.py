"""
Clase base para los estados del juego (menús, juego, game over, etc.)
"""

from abc import ABC, abstractmethod

import pygame


class GameState(ABC):
    """Clase abstracta para los estados del juego."""

    def __init__(self, game):
        """Inicializa el estado del juego.

        Args:
            game: Instancia del juego principal
        """
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.running = True
        self.next_state = None
        self.font = pygame.font.Font(None, 36)

    @abstractmethod
    def handle_events(self, event):
        """Maneja un evento de entrada.
        
        Args:
            event: El evento de Pygame a manejar.
        """
        if event.type == pygame.QUIT:  # pylint: disable=no-member
            self.running = False

    @abstractmethod
    def update(self, dt):
        """Actualiza la lógica del estado.

        Args:
            dt: Tiempo transcurrido desde la última actualización en segundos
        """

    @abstractmethod
    def draw(self):
        """Dibuja el estado en la pantalla."""

    def change_state(self, new_state):
        """Cambia a un nuevo estado.

        Args:
            new_state: Clase del nuevo estado (no instancia)
        """
        self.next_state = new_state
        self.running = False

    def run(self):
        """Ejecuta el bucle principal del estado."""
        self.running = True
        self.next_state = None

        while self.running:
            dt = self.clock.tick(60) / 1000.0  # Convertir a segundos
            
            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # pylint: disable=no-member
                    self.running = False
                    self.game.running = False
                else:
                    self.handle_events(event)
            
            # Actualizar y dibujar
            self.update(dt)
            self.draw()
            pygame.display.flip()

        return self.next_state
